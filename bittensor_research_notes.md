# Bittensor Subnet Launch Research Notes

## 1. Overview
Bittensor subnets are decentralized incentive mechanisms that reward participants for providing specific commodities (e.g., data, computing, AI models).

## 2. Launch Process
1.  **Local Testing**: Use `subtensor` to run a local chain for development.
2.  **Wallet Creation**: Use `btcli wallet create` to create owner, miner, and validator wallets.
3.  **Registration**:
    *   **Testnet**: `btcli subnet create --network test`
    *   **Mainnet**: `btcli subnet create` (requires dynamic TAO burn cost).
4.  **Starting**: Subnets are inactive by default. Start emission with `btcli subnet start --netuid <id>`.
5.  **Immunity**: New subnets have a 4-month immunity period from deregistration.

## 3. Python SDK (`bittensor`)
*   **Core Components**: `Subtensor`, `Metagraph`, `Wallet`, `Neuron`.
*   **Miner/Validator Implementation**: Requires implementing a class that inherits from `bittensor.Neuron` or using provided templates.
*   **Weight Setting**: Validators must submit weights to the chain to determine reward distribution.

## 4. Cybersecurity Considerations
*   **Private Key Safety**: Coldkeys should remain offline; use hotkeys for active operations.
*   **Validator Security**: Validators are high-value targets. Use firewalls, secure RPC connections, and monitor for unauthorized weight changes.
*   **MEV Protection**: Use MEV Shield to protect transactions from front-running.
*   **Software Integrity**: Only install software from official sources.
*   **Consensus Attacks**: Monitor for stake concentration and collusion among validators.

## 5. Taostats Insights
*   **Subnet Identity**: Can be set and updated via `btcli s get-identity`.
*   **Immune Owner Neurons**: Owners can have up to 10 immune neurons (default 1).
*   **Registration Costs**: Dynamic and can be checked via `btcli subnet burn-cost`.
