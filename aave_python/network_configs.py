from .models import ReserveToken

import requests


"""----------------------------------- NETWORK CONFIG & ABI REFERENCE DATACLASSES ----------------------------------"""
class KovanConfig:
    def __init__(self, kovan_rpc_url: str):
        self.net_name = "Kovan"
        self.chain_id = 42
        self.lending_pool_addresses_provider = '0x88757f2f99175387aB4C6a4b3067c77A695b0349'
        self.protocol_data_provider = '0x3c73A5E5785cAC854D468F727c606C07488a29D6'
        self.weth_token = '0xd0a1e359811322d97991e03f863a0c30c2cf029c'
        # https://aave.github.io/aave-addresses/kovan.json
        # Aave uses their own testnet tokens to ensure they are good
        # find the most up to date in the above
        self.rpc_url = kovan_rpc_url
        self.aave_tokenlist_url = "https://aave.github.io/aave-addresses/kovan.json"
        self.aave_tokens = [ReserveToken(**token_data) for token_data in self.fetch_aave_tokens()]

    def fetch_aave_tokens(self) -> dict:
        try:
            return requests.get(self.aave_tokenlist_url).json()['proto']
        except:
            raise ConnectionError("Could not fetch Aave tokenlist for the Kovan network from URL: "
                                  "https://aave.github.io/aave-addresses/kovan.json")


class MainnetConfig:
    def __init__(self, mainnet_rpc_url: str):
        self.net_name = "Mainnet"
        self.chain_id = 1337
        self.lending_pool_addresses_provider = '0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5'
        self.protocol_data_provider = '0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d'
        self.weth_token = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
        # For mainnet, the link token is the same as the aave token
        self.link_token = '0x514910771af9ca656af840dff83e8264ecf986ca'
        # self.aave_link_token = '0x514910771af9ca656af840dff83e8264ecf986ca'
        self.rpc_url = mainnet_rpc_url
        self.aave_tokenlist_url = "https://aave.github.io/aave-addresses/mainnet.json"
        self.aave_tokens = [ReserveToken(**token_data) for token_data in self.fetch_aave_tokens()]

    def fetch_aave_tokens(self) -> dict:
        try:
            return requests.get(self.aave_tokenlist_url).json()['proto']
        except:
            raise ConnectionError("Could not fetch Aave tokenlist for the Mainnet network from URL: "
                                  "https://aave.github.io/aave-addresses/mainnet.json")