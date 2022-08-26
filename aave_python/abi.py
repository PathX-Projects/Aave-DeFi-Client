class ABIReference:
    """
    This class contains full JSON ABIs for the smart contracts being called in this client.

    Eventually, I will implement a method to call these ABIs from the etherscan API when they are needed, instead of
    utilizing this class structure which results in hundreds of redundant lines.

    Disregard all past this line, unless you need to add an ABI to implement more smart contracts.
    """
    protocol_data_provider = [
          {
            "inputs": [
              {
                "internalType": "contract ILendingPoolAddressesProvider",
                "name": "addressesProvider",
                "type": "address"
              }
            ],
            "stateMutability": "nonpayable",
            "type": "constructor"
          },
          {
            "inputs": [

            ],
            "name": "ADDRESSES_PROVIDER",
            "outputs": [
              {
                "internalType": "contract ILendingPoolAddressesProvider",
                "name": "",
                "type": "address"
              }
            ],
            "stateMutability": "view",
            "type": "function"
          },
          {
            "inputs": [

            ],
            "name": "getAllATokens",
            "outputs": [
              {
                "components": [
                  {
                    "internalType": "string",
                    "name": "symbol",
                    "type": "string"
                  },
                  {
                    "internalType": "address",
                    "name": "tokenAddress",
                    "type": "address"
                  }
                ],
                "internalType": "struct AaveProtocolDataProvider.TokenData[]",
                "name": "",
                "type": "tuple[]"
              }
            ],
            "stateMutability": "view",
            "type": "function"
          },
          {
            "inputs": [

            ],
            "name": "getAllReservesTokens",
            "outputs": [
              {
                "components": [
                  {
                    "internalType": "string",
                    "name": "symbol",
                    "type": "string"
                  },
                  {
                    "internalType": "address",
                    "name": "tokenAddress",
                    "type": "address"
                  }
                ],
                "internalType": "struct AaveProtocolDataProvider.TokenData[]",
                "name": "",
                "type": "tuple[]"
              }
            ],
            "stateMutability": "view",
            "type": "function"
          },
          {
            "inputs": [
              {
                "internalType": "address",
                "name": "asset",
                "type": "address"
              }
            ],
            "name": "getReserveConfigurationData",
            "outputs": [
              {
                "internalType": "uint256",
                "name": "decimals",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "ltv",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "liquidationThreshold",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "liquidationBonus",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "reserveFactor",
                "type": "uint256"
              },
              {
                "internalType": "bool",
                "name": "usageAsCollateralEnabled",
                "type": "bool"
              },
              {
                "internalType": "bool",
                "name": "borrowingEnabled",
                "type": "bool"
              },
              {
                "internalType": "bool",
                "name": "stableBorrowRateEnabled",
                "type": "bool"
              },
              {
                "internalType": "bool",
                "name": "isActive",
                "type": "bool"
              },
              {
                "internalType": "bool",
                "name": "isFrozen",
                "type": "bool"
              }
            ],
            "stateMutability": "view",
            "type": "function"
          },
          {
            "inputs": [
              {
                "internalType": "address",
                "name": "asset",
                "type": "address"
              }
            ],
            "name": "getReserveData",
            "outputs": [
              {
                "internalType": "uint256",
                "name": "availableLiquidity",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "totalStableDebt",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "totalVariableDebt",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "liquidityRate",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "variableBorrowRate",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "stableBorrowRate",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "averageStableBorrowRate",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "liquidityIndex",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "variableBorrowIndex",
                "type": "uint256"
              },
              {
                "internalType": "uint40",
                "name": "lastUpdateTimestamp",
                "type": "uint40"
              }
            ],
            "stateMutability": "view",
            "type": "function"
          },
          {
            "inputs": [
              {
                "internalType": "address",
                "name": "asset",
                "type": "address"
              }
            ],
            "name": "getReserveTokensAddresses",
            "outputs": [
              {
                "internalType": "address",
                "name": "aTokenAddress",
                "type": "address"
              },
              {
                "internalType": "address",
                "name": "stableDebtTokenAddress",
                "type": "address"
              },
              {
                "internalType": "address",
                "name": "variableDebtTokenAddress",
                "type": "address"
              }
            ],
            "stateMutability": "view",
            "type": "function"
          },
          {
            "inputs": [
              {
                "internalType": "address",
                "name": "asset",
                "type": "address"
              },
              {
                "internalType": "address",
                "name": "user",
                "type": "address"
              }
            ],
            "name": "getUserReserveData",
            "outputs": [
              {
                "internalType": "uint256",
                "name": "currentATokenBalance",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "currentStableDebt",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "currentVariableDebt",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "principalStableDebt",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "scaledVariableDebt",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "stableBorrowRate",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "liquidityRate",
                "type": "uint256"
              },
              {
                "internalType": "uint40",
                "name": "stableRateLastUpdated",
                "type": "uint40"
              },
              {
                "internalType": "bool",
                "name": "usageAsCollateralEnabled",
                "type": "bool"
              }
            ],
            "stateMutability": "view",
            "type": "function"
          }
        ]

    weth_abi = [
        {
            "constant": True,
            "inputs": [],
            "name": "name",
            "outputs": [{"name": "tokenName", "type": "string"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [
                {"name": "spender", "type": "address"},
                {"name": "value", "type": "uint256"},
            ],
            "name": "approve",
            "outputs": [{"name": "success", "type": "bool"}],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "totalSupply",
            "outputs": [{"name": "totalTokensIssued", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
            ],
            "name": "transferFrom",
            "outputs": [{"name": "success", "type": "bool"}],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "decimalPlaces", "type": "uint8"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [{"name": "owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "symbol",
            "outputs": [{"name": "tokenSymbol", "type": "string"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
            ],
            "name": "transfer",
            "outputs": [{"name": "success", "type": "bool"}],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [],
            "name": "deposit",
            "outputs": [],
            "payable": True,
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [
                {"name": "owner", "type": "address"},
                {"name": "spender", "type": "address"},
            ],
            "name": "allowance",
            "outputs": [{"name": "remaining", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
    ]

    price_feed_abi = [
        {
            "inputs": [],
            "name": "decimals",
            "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "description",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint80", "name": "_roundId", "type": "uint80"}],
            "name": "getRoundData",
            "outputs": [
                {"internalType": "uint80", "name": "roundId", "type": "uint80"},
                {"internalType": "int256", "name": "answer", "type": "int256"},
                {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
                {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
                {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "latestRoundData",
            "outputs": [
                {"internalType": "uint80", "name": "roundId", "type": "uint80"},
                {"internalType": "int256", "name": "answer", "type": "int256"},
                {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
                {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
                {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "version",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
    ]

    erc20_abi = [
        {
            "inputs": [
                {"internalType": "address", "name": "owner", "type": "address"},
                {"internalType": "address", "name": "spender", "type": "address"},
            ],
            "name": "allowance",
            "outputs": [
                {"internalType": "uint256", "name": "remaining", "type": "uint256"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "spender", "type": "address"},
                {"internalType": "uint256", "name": "value", "type": "uint256"},
            ],
            "name": "approve",
            "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"internalType": "uint256", "name": "balance", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "decimals",
            "outputs": [
                {"internalType": "uint8", "name": "decimalPlaces", "type": "uint8"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "spender", "type": "address"},
                {"internalType": "uint256", "name": "addedValue", "type": "uint256"},
            ],
            "name": "decreaseApproval",
            "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "spender", "type": "address"},
                {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"},
            ],
            "name": "increaseApproval",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "name",
            "outputs": [{"internalType": "string", "name": "tokenName", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "symbol",
            "outputs": [
                {"internalType": "string", "name": "tokenSymbol", "type": "string"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "totalSupply",
            "outputs": [
                {"internalType": "uint256", "name": "totalTokensIssued", "type": "uint256"}
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "to", "type": "address"},
                {"internalType": "uint256", "name": "value", "type": "uint256"},
            ],
            "name": "transfer",
            "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "to", "type": "address"},
                {"internalType": "uint256", "name": "value", "type": "uint256"},
                {"internalType": "bytes", "name": "data", "type": "bytes"},
            ],
            "name": "transferAndCall",
            "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "from", "type": "address"},
                {"internalType": "address", "name": "to", "type": "address"},
                {"internalType": "uint256", "name": "value", "type": "uint256"},
            ],
            "name": "transferFrom",
            "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ]

    lending_pool_addresses_provider_abi = [
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "bytes32",
                    "name": "id",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "bool",
                    "name": "hasProxy",
                    "type": "bool",
                },
            ],
            "name": "AddressSet",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "ConfigurationAdminUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "EmergencyAdminUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "LendingPoolCollateralManagerUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "LendingPoolConfiguratorUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "LendingPoolUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "LendingRateOracleUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "string",
                    "name": "newMarketId",
                    "type": "string",
                }
            ],
            "name": "MarketIdSet",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                }
            ],
            "name": "PriceOracleUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "bytes32",
                    "name": "id",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newAddress",
                    "type": "address",
                },
            ],
            "name": "ProxyCreated",
            "type": "event",
        },
        {
            "inputs": [{"internalType": "bytes32", "name": "id", "type": "bytes32"}],
            "name": "getAddress",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getEmergencyAdmin",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getLendingPool",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getLendingPoolCollateralManager",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getLendingPoolConfigurator",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getLendingRateOracle",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getMarketId",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getPoolAdmin",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getPriceOracle",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                {"internalType": "address", "name": "newAddress", "type": "address"},
            ],
            "name": "setAddress",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                {"internalType": "address", "name": "impl", "type": "address"},
            ],
            "name": "setAddressAsProxy",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "admin", "type": "address"}],
            "name": "setEmergencyAdmin",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "manager", "type": "address"}],
            "name": "setLendingPoolCollateralManager",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "configurator", "type": "address"}
            ],
            "name": "setLendingPoolConfiguratorImpl",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "pool", "type": "address"}],
            "name": "setLendingPoolImpl",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "lendingRateOracle", "type": "address"}
            ],
            "name": "setLendingRateOracle",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "string", "name": "marketId", "type": "string"}],
            "name": "setMarketId",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "admin", "type": "address"}],
            "name": "setPoolAdmin",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "priceOracle", "type": "address"}
            ],
            "name": "setPriceOracle",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ]

    lending_pool_abi = [
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "onBehalfOf",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "borrowRateMode",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "borrowRate",
                    "type": "uint256",
                },
                {
                    "indexed": True,
                    "internalType": "uint16",
                    "name": "referral",
                    "type": "uint16",
                },
            ],
            "name": "Borrow",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "onBehalfOf",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
                {
                    "indexed": True,
                    "internalType": "uint16",
                    "name": "referral",
                    "type": "uint16",
                },
            ],
            "name": "Deposit",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "target",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "initiator",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "asset",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "premium",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint16",
                    "name": "referralCode",
                    "type": "uint16",
                },
            ],
            "name": "FlashLoan",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "collateralAsset",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "debtAsset",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "debtToCover",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "liquidatedCollateralAmount",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "liquidator",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "bool",
                    "name": "receiveAToken",
                    "type": "bool",
                },
            ],
            "name": "LiquidationCall",
            "type": "event",
        },
        {"anonymous": False, "inputs": [], "name": "Paused", "type": "event"},
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
            ],
            "name": "RebalanceStableBorrowRate",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "repayer",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "Repay",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "liquidityRate",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "stableBorrowRate",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "variableBorrowRate",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "liquidityIndex",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "variableBorrowIndex",
                    "type": "uint256",
                },
            ],
            "name": "ReserveDataUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
            ],
            "name": "ReserveUsedAsCollateralDisabled",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
            ],
            "name": "ReserveUsedAsCollateralEnabled",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "rateMode",
                    "type": "uint256",
                },
            ],
            "name": "Swap",
            "type": "event",
        },
        {"anonymous": False, "inputs": [], "name": "Unpaused", "type": "event"},
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "reserve",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "to",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "Withdraw",
            "type": "event",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "uint256", "name": "interestRateMode", "type": "uint256"},
                {"internalType": "uint16", "name": "referralCode", "type": "uint16"},
                {"internalType": "address", "name": "onBehalfOf", "type": "address"},
            ],
            "name": "borrow",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "address", "name": "onBehalfOf", "type": "address"},
                {"internalType": "uint16", "name": "referralCode", "type": "uint16"},
            ],
            "name": "deposit",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "address", "name": "from", "type": "address"},
                {"internalType": "address", "name": "to", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "uint256", "name": "balanceFromAfter", "type": "uint256"},
                {"internalType": "uint256", "name": "balanceToBefore", "type": "uint256"},
            ],
            "name": "finalizeTransfer",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "receiverAddress", "type": "address"},
                {"internalType": "address[]", "name": "assets", "type": "address[]"},
                {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"},
                {"internalType": "uint256[]", "name": "modes", "type": "uint256[]"},
                {"internalType": "address", "name": "onBehalfOf", "type": "address"},
                {"internalType": "bytes", "name": "params", "type": "bytes"},
                {"internalType": "uint16", "name": "referralCode", "type": "uint16"},
            ],
            "name": "flashLoan",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getAddressesProvider",
            "outputs": [
                {
                    "internalType": "contract ILendingPoolAddressesProvider",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
            "name": "getConfiguration",
            "outputs": [
                {
                    "components": [
                        {"internalType": "uint256", "name": "data", "type": "uint256"}
                    ],
                    "internalType": "struct DataTypes.ReserveConfigurationMap",
                    "name": "",
                    "type": "tuple",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
            "name": "getReserveData",
            "outputs": [
                {
                    "components": [
                        {
                            "components": [
                                {
                                    "internalType": "uint256",
                                    "name": "data",
                                    "type": "uint256",
                                }
                            ],
                            "internalType": "struct DataTypes.ReserveConfigurationMap",
                            "name": "configuration",
                            "type": "tuple",
                        },
                        {
                            "internalType": "uint128",
                            "name": "liquidityIndex",
                            "type": "uint128",
                        },
                        {
                            "internalType": "uint128",
                            "name": "variableBorrowIndex",
                            "type": "uint128",
                        },
                        {
                            "internalType": "uint128",
                            "name": "currentLiquidityRate",
                            "type": "uint128",
                        },
                        {
                            "internalType": "uint128",
                            "name": "currentVariableBorrowRate",
                            "type": "uint128",
                        },
                        {
                            "internalType": "uint128",
                            "name": "currentStableBorrowRate",
                            "type": "uint128",
                        },
                        {
                            "internalType": "uint40",
                            "name": "lastUpdateTimestamp",
                            "type": "uint40",
                        },
                        {
                            "internalType": "address",
                            "name": "aTokenAddress",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "stableDebtTokenAddress",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "variableDebtTokenAddress",
                            "type": "address",
                        },
                        {
                            "internalType": "address",
                            "name": "interestRateStrategyAddress",
                            "type": "address",
                        },
                        {"internalType": "uint8", "name": "id", "type": "uint8"},
                    ],
                    "internalType": "struct DataTypes.ReserveData",
                    "name": "",
                    "type": "tuple",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
            "name": "getReserveNormalizedIncome",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
            "name": "getReserveNormalizedVariableDebt",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getReservesList",
            "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
            "name": "getUserAccountData",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "totalCollateralETH",
                    "type": "uint256",
                },
                {"internalType": "uint256", "name": "totalDebtETH", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "availableBorrowsETH",
                    "type": "uint256",
                },
                {
                    "internalType": "uint256",
                    "name": "currentLiquidationThreshold",
                    "type": "uint256",
                },
                {"internalType": "uint256", "name": "ltv", "type": "uint256"},
                {"internalType": "uint256", "name": "healthFactor", "type": "uint256"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
            "name": "getUserConfiguration",
            "outputs": [
                {
                    "components": [
                        {"internalType": "uint256", "name": "data", "type": "uint256"}
                    ],
                    "internalType": "struct DataTypes.UserConfigurationMap",
                    "name": "",
                    "type": "tuple",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "reserve", "type": "address"},
                {"internalType": "address", "name": "aTokenAddress", "type": "address"},
                {"internalType": "address", "name": "stableDebtAddress", "type": "address"},
                {
                    "internalType": "address",
                    "name": "variableDebtAddress",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "interestRateStrategyAddress",
                    "type": "address",
                },
            ],
            "name": "initReserve",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "collateralAsset", "type": "address"},
                {"internalType": "address", "name": "debtAsset", "type": "address"},
                {"internalType": "address", "name": "user", "type": "address"},
                {"internalType": "uint256", "name": "debtToCover", "type": "uint256"},
                {"internalType": "bool", "name": "receiveAToken", "type": "bool"},
            ],
            "name": "liquidationCall",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "paused",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "address", "name": "user", "type": "address"},
            ],
            "name": "rebalanceStableBorrowRate",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "uint256", "name": "rateMode", "type": "uint256"},
                {"internalType": "address", "name": "onBehalfOf", "type": "address"},
            ],
            "name": "repay",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "reserve", "type": "address"},
                {"internalType": "uint256", "name": "configuration", "type": "uint256"},
            ],
            "name": "setConfiguration",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "bool", "name": "val", "type": "bool"}],
            "name": "setPause",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "reserve", "type": "address"},
                {
                    "internalType": "address",
                    "name": "rateStrategyAddress",
                    "type": "address",
                },
            ],
            "name": "setReserveInterestRateStrategyAddress",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "bool", "name": "useAsCollateral", "type": "bool"},
            ],
            "name": "setUserUseReserveAsCollateral",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "uint256", "name": "rateMode", "type": "uint256"},
            ],
            "name": "swapBorrowRateMode",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "asset", "type": "address"},
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "address", "name": "to", "type": "address"},
            ],
            "name": "withdraw",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ]

    aave_price_oracle_abi = [
        {
            "inputs": [
                {
                    "internalType": "address[]",
                    "name": "_assets",
                    "type": "address[]"
                },
                {
                    "internalType": "address[]",
                    "name": "_sources",
                    "type": "address[]"
                },
                {
                    "internalType": "address",
                    "name": "_fallbackOracle",
                    "type": "address"
                }
            ],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "asset",
                    "type": "address"
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "source",
                    "type": "address"
                }
            ],
            "name": "AssetSourceUpdated",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "fallbackOracle",
                    "type": "address"
                }
            ],
            "name": "FallbackOracleUpdated",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "previousOwner",
                    "type": "address"
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address"
                }
            ],
            "name": "OwnershipTransferred",
            "type": "event"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "isOwner",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "owner",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [],
            "name": "renounceOwnership",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address"
                }
            ],
            "name": "transferOwnership",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {
                    "internalType": "address[]",
                    "name": "_assets",
                    "type": "address[]"
                },
                {
                    "internalType": "address[]",
                    "name": "_sources",
                    "type": "address[]"
                }
            ],
            "name": "setAssetSources",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_fallbackOracle",
                    "type": "address"
                }
            ],
            "name": "setFallbackOracle",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_asset",
                    "type": "address"
                }
            ],
            "name": "getAssetPrice",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [
                {
                    "internalType": "address[]",
                    "name": "_assets",
                    "type": "address[]"
                }
            ],
            "name": "getAssetsPrices",
            "outputs": [
                {
                    "internalType": "uint256[]",
                    "name": "",
                    "type": "uint256[]"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_asset",
                    "type": "address"
                }
            ],
            "name": "getSourceOfAsset",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "getFallbackOracle",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }
    ]

    protocol_data_provider_contract_address = "0x057835Ad21177dbdd3090bB1CAE03EaCF78Fc6d"
    protocol_data_provider = [
        {
            "inputs": [
                {
                    "internalType": "contract ILendingPoolAddressesProvider",
                    "name": "addressesProvider",
                    "type": "address"
                }
            ],
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "inputs": [],
            "name": "ADDRESSES_PROVIDER",
            "outputs": [
                {
                    "internalType": "contract ILendingPoolAddressesProvider",
                    "name": "",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getAllATokens",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "string",
                            "name": "symbol",
                            "type": "string"
                        },
                        {
                            "internalType": "address",
                            "name": "tokenAddress",
                            "type": "address"
                        }
                    ],
                    "internalType": "struct AaveProtocolDataProvider.TokenData[]",
                    "name": "",
                    "type": "tuple[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getAllReservesTokens",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "string",
                            "name": "symbol",
                            "type": "string"
                        },
                        {
                            "internalType": "address",
                            "name": "tokenAddress",
                            "type": "address"
                        }
                    ],
                    "internalType": "struct AaveProtocolDataProvider.TokenData[]",
                    "name": "",
                    "type": "tuple[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "asset",
                    "type": "address"
                }
            ],
            "name": "getReserveConfigurationData",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "decimals",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "ltv",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "liquidationThreshold",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "liquidationBonus",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "reserveFactor",
                    "type": "uint256"
                },
                {
                    "internalType": "bool",
                    "name": "usageAsCollateralEnabled",
                    "type": "bool"
                },
                {
                    "internalType": "bool",
                    "name": "borrowingEnabled",
                    "type": "bool"
                },
                {
                    "internalType": "bool",
                    "name": "stableBorrowRateEnabled",
                    "type": "bool"
                },
                {
                    "internalType": "bool",
                    "name": "isActive",
                    "type": "bool"
                },
                {
                    "internalType": "bool",
                    "name": "isFrozen",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "asset",
                    "type": "address"
                }
            ],
            "name": "getReserveData",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "availableLiquidity",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "totalStableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "totalVariableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "liquidityRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "variableBorrowRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "stableBorrowRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "averageStableBorrowRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "liquidityIndex",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "variableBorrowIndex",
                    "type": "uint256"
                },
                {
                    "internalType": "uint40",
                    "name": "lastUpdateTimestamp",
                    "type": "uint40"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "asset",
                    "type": "address"
                }
            ],
            "name": "getReserveTokensAddresses",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "aTokenAddress",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "stableDebtTokenAddress",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "variableDebtTokenAddress",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "asset",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "user",
                    "type": "address"
                }
            ],
            "name": "getUserReserveData",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "currentATokenBalance",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "currentStableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "currentVariableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "principalStableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "scaledVariableDebt",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "stableBorrowRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "liquidityRate",
                    "type": "uint256"
                },
                {
                    "internalType": "uint40",
                    "name": "stableRateLastUpdated",
                    "type": "uint40"
                },
                {
                    "internalType": "bool",
                    "name": "usageAsCollateralEnabled",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]

