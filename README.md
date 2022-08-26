# Aave DeFi Client for Web3.py

> NOTE: This is the beta version of the client. More docs to come...

# Overview:

The Aave DeFi Client is a Python wrapper for the core functionality on the Aave DeFi lending protocol built using only two 3rd party packages, web3 and requests.

Currently only the **_Ethereum mainnet_** and **_Kovan testnet_** are supported.  

## Setup

1. Ensure that you are using Python version 3.9+
2. Install the package using pip:
   ```shell
   pip install aave-python
   ```
3. Repare your HTTP providers for the Ethereum mainnet and/or Kovan testnet. 

## Usage:
- You can find examples for the client's functionality in the [usage_examples](https://github.com/PathX-Projects/Aave-DeFi-Client/tree/main/usage_examples) directory.

## How to Get Kovan Testnet WETH:
1. Enter your public wallet address at [ethdrop.dev](https://ethdrop.dev/) and get ETH
2. Use the [`usage_examples/get_kovan_weth.py`](https://github.com/PathX-Projects/Aave-DeFi-Client/blob/main/usage_examples/get_kovan_weth.py) script to convert your testnet ETH to ERC-20 WETH that can be deposited to Aave.
