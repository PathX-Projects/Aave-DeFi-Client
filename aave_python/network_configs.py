from .models import ReserveToken

import requests


"""----------------------------------- NETWORK CONFIG & ABI REFERENCE CLASSES ----------------------------------"""
class MainnetConfig:
    def __init__(self, mainnet_rpc_url: str):
        """Config for the Ethereum mainnet"""
        self.net_name = "Mainnet"
        self.chain_id = 1
        self.lending_pool_addresses_provider = '0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5'
        self.protocol_data_provider = '0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d'
        self.weth_token = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
        self.rpc_url = mainnet_rpc_url
        self.aave_tokenlist_url = "https://aave.github.io/aave-addresses/mainnet.json"
        self.aave_tokens = [ReserveToken(**token_data) for token_data in self.fetch_aave_tokens()]
        # self.aave_tokens: list[ReserveToken] = []  # Starts as empty list

    def fetch_aave_tokens(self) -> dict:
        try:
            # r =
            return requests.get(self.aave_tokenlist_url).json()['proto']
        except:
            raise ConnectionError("Could not fetch Aave tokenlist for the Mainnet network from URL: "
                                  "https://aave.github.io/aave-addresses/mainnet.json")
            
class GoerliConfig:
    def __init__(self, goerli_rpc_url: str) -> None:
        """Config for the Görli testnet"""
        self.net_name = "Görli"
        self.chain_id = 5
        self.lending_pool_addresses_provider = '0x5E52dEc931FFb32f609681B8438A51c675cc232d'
        self.protocol_data_provider = '0x927F584d4321C1dCcBf5e2902368124b02419a1E'
        self.weth_token = '0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6'
        self.rpc_url = goerli_rpc_url
        self.aave_tokens: list[ReserveToken] = []  # Starts as empty list, to be populated by AaveClient
        
        # NEED TO FIGURE OUT IF THERE'S A TOKEN ADDRESS LIST FOR GÖRLI, SIMILAR TO THE ONE FOR MAINNET & KOVAN,
        # IF NOT, CAN CALL THE GET_RESERVE_TOKENS() METHOD ON THE LENDING POOL ADDRESSES PROVIDER CONTRACT


# KOVAN HAS BEEN DEPRECATED AND REPLACED WITH GOERLI TESTNET
# class KovanConfig:
#     def __init__(self, kovan_rpc_url: str):
#         self.net_name = "Kovan"
#         self.chain_id = 42
#         self.lending_pool_addresses_provider = '0x88757f2f99175387aB4C6a4b3067c77A695b0349'
#         self.protocol_data_provider = '0x3c73A5E5785cAC854D468F727c606C07488a29D6'
#         self.weth_token = '0xd0a1e359811322d97991e03f863a0c30c2cf029c'
#         self.rpc_url = kovan_rpc_url
#         self.aave_tokenlist_url = "https://aave.github.io/aave-addresses/kovan.json"
#         self.aave_tokens = [ReserveToken(**token_data) for token_data in self.fetch_aave_tokens()]

#     def fetch_aave_tokens(self) -> dict:
#         try:
#             return requests.get(self.aave_tokenlist_url).json()['proto']
#         except:
#             raise ConnectionError("Could not fetch Aave tokenlist for the Kovan network from URL: "
#                                   "https://aave.github.io/aave-addresses/kovan.json")