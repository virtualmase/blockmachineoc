import os
import json
import requests
import time
from typing import List, Dict

class ResearchAgent:
    def __init__(self, name: str, role: str, instruction: str, api_key: str):
        self.name = name
        self.role = role
        self.instruction = instruction
        self.api_key = api_key
        self.base_url = "https://api.manus.ai/v2"
        self.headers = {
            "x-manus-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        self.project_id = self._create_project()

    def _create_project(self) -> str:
        payload = {
            "name": f"{self.name} Project",
            "instruction": f"You are {self.name}, a {self.role}. {self.instruction}"
        }
        response = requests.post(f"{self.base_url}/project.create", headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()["project"]["id"]

    def run_task(self, prompt: str) -> str:
        payload = {
            "message": {"content": [{"type": "text", "text": prompt}]},
            "project_id": self.project_id,
            "title": f"{self.name} Task"
        }
        response = requests.post(f"{self.base_url}/task.create", headers=self.headers, json=payload)
        response.raise_for_status()
        task_id = response.json()["task_id"]
        
        # Polling for completion
        while True:
            time.sleep(10)
            status_response = requests.get(f"{self.base_url}/task.listMessages?task_id={task_id}&order=desc", headers=self.headers)
            status_response.raise_for_status()
            messages = status_response.json()["data"]
            
            for msg in messages:
                if msg.get("type") == "status_update" and msg.get("status_update", {}).get("agent_status") == "stopped":
                    # Get final assistant message
                    for final_msg in messages:
                        if final_msg.get("type") == "assistant_message":
                            return final_msg["assistant_message"]["content"]
            print(f"Agent {self.name} is still working...")

def main():
    api_key = os.getenv("MANUS_API_KEY")
    if not api_key:
        print("Error: MANUS_API_KEY environment variable not set.")
        return

    # Define the agents
    agents = [
        ResearchAgent(
            "Bittensor Architect",
            "Expert in Bittensor subnet design and Python SDK implementation",
            "Focus on the technical steps of launching a subnet, including Python code snippets for miners and validators.",
            api_key
        ),
        ResearchAgent(
            "Cybersecurity Expert",
            "Expert in blockchain security and threat modeling",
            "Focus on identifying potential security risks in subnet operations, private key management, and consensus integrity.",
            api_key
        ),
        ResearchAgent(
            "Economic Analyst",
            "Expert in tokenomics and incentive mechanisms",
            "Focus on the dynamic burn cost, emission schedules, and incentive design for miners and validators.",
            api_key
        )
    ]

    # Shared research context from initial findings
    with open("bittensor_research_notes.md", "r") as f:
        research_context = f.read()

    results = {}
    for agent in agents:
        print(f"Starting task for {agent.name}...")
        prompt = f"Based on the following research context, provide a detailed report from your perspective as a {agent.role}:\n\n{research_context}"
        results[agent.name] = agent.run_task(prompt)
        print(f"Completed task for {agent.name}.")

    # Compile final report
    final_report = "# Bittensor Subnet Launch: Multi-Agent Research Report\n\n"
    for name, result in results.items():
        final_report += f"## Perspective: {name}\n\n{result}\n\n"

    with open("final_research_report.md", "w") as f:
        f.write(final_report)
    print("Final report generated: final_research_report.md")

if __name__ == "__main__":
    main()
