# Aave DeFi Client for Web3.py

> NOTE: This is the beta version of the client. More docs to come...

# Overview:

The Aave DeFi Client is a Python wrapper for the core functionality on the Aave DeFi lending protocol built using only two 3rd party packages, web3 and requests. The current supported functions are [`withdraw()`](https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#withdraw), [`deposit()`](https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#deposit), [`borrow()`](https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#borrow), and [`repay()`](https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#repay).

## Setup

Please install or have installed the following:

1. Install the pip package requirements from the `requirements.txt` file
2. Make sure that you have a working RPC url for your target network. Currently the client supports the Ethereum Kovan Testnet and Mainnet. If you do not have an RPC url, you can use [Infuria.io](https://infura.io/) 

## Important Repository Information:
- The only dependencies for usage of the aave_client are the package requirements (in [`requirements.txt`](https://github.com/PathX-Projects/Aave-DeFi-Client/blob/main/requirements.txt)), and the [`aave_client.py`](https://github.com/PathX-Projects/Aave-DeFi-Client/blob/main/aave_client.py) file.
- You can find examples of the client's functionality in the [`usage_examples`](https://github.com/PathX-Projects/Aave-DeFi-Client/tree/main/usage_examples) directory.
- You can safely move the [`aave_client.py`](https://github.com/PathX-Projects/Aave-DeFi-Client/blob/main/aave_client.py) file to different directories and use it with no issues, as long as the package requirements are satisfied.

## How to Get Kovan Testnet WETH:
1. Enter your public wallet address at [ethdrop.dev](https://ethdrop.dev/) and get ETH
2. Use the [`usage_examples/get_kovan_weth.py`](https://github.com/PathX-Projects/Aave-DeFi-Client/blob/main/usage_examples/get_kovan_weth.py) script to convert your testnet ETH to ERC-20 WETH that can be deposited to Aave.
