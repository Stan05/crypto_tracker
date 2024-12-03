# crypto_tracker/services/wallet_service.py
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field
from sqlalchemy.testing.config import ident
from sqlalchemy.util import symbol

from crypto_tracker.database import Database
from crypto_tracker.logger import Logger
from crypto_tracker.models import ChainIdType, DexIdType, TradeType, TransactionResponseType, TransactionStatusType
from crypto_tracker.repositories.models.base import TradeORM, TokenORM, PairORM, WalletORM, TransactionORM
from crypto_tracker.services.pair_service import PairService
from crypto_tracker.services.token_service import TokenService
from crypto_tracker.services.trade_service import TradeService
from crypto_tracker.web3.graph_protocol.uniswap_v3 import GrtUniswapSwapV3Connector, GraphResponse

"""
class Token(BaseModel):
    id: str
    name: str
    symbol: str

class Pool(BaseModel):
    id: str
    base_token_price: str = Field(alias="token0Price")
    quote_token_price: str = Field(alias="token1Price")

class Swap(BaseModel):
    base_token_amount: float = Field(alias="amount0")
    quote_token_amount: float = Field(alias="amount1")
    amountUSD: float
    origin: str
    base_token: Token = Field(alias="token0")
    quote_token: Token = Field(alias="token1")
    timestamp: datetime
    pool: Pool

class Transaction(BaseModel):
    id: str
    swaps: List[Swap]

class TransactionData(BaseModel):
    transaction: Transaction

class GraphResponse(BaseModel):
    data: TransactionData
"""
class TransactionService:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()
        self.token_service = TokenService()
        self.pair_service = PairService()
        self.trade_service = TradeService()
        self.uniswap = GrtUniswapSwapV3Connector()

    def add_txn_if_not_exist(self, txn: TransactionORM) -> TransactionORM:
        existing_txn = self.db.transaction_repo.get_txn_by_hash(txn.hash)
        if not existing_txn:
            self.logger.info(f'Trade {txn.hash} does not exist creating it')
            return self.db.transaction_repo.create(txn)
        return existing_txn

    def query_txn(self, txn_hash:str, chain_id:ChainIdType, dex_id: DexIdType):
        if chain_id is not ChainIdType.BASE:
            raise Exception(f'Querying chain {chain_id} is not supported yet')
        if dex_id is not DexIdType.UNISWAP:
            raise Exception(f'Querying dex {dex_id} is not supported yet')

        """
        1. Check if wallet is created, otherwise throw and has the ability to reprocess
        2. Check if tokens in txn are created, if not create them
        3. Check if pair in txn is created, if not create it
        4. Add the trade
        """
        try:
            parsed_data:GraphResponse = self.uniswap.fetch(variables={"transactionId": txn_hash})
        except RuntimeError as e:
            print(f"Error: {e}")
            return

        # Parse into Pydantic models

        swap = parsed_data.transaction.swaps[0]
        """parsed_data: GraphResponse = GraphResponse.model_validate_json(response)"""
        txn: TransactionORM = self.add_txn_if_not_exist(TransactionORM(
            hash=parsed_data.transaction.id,
            payload=parsed_data.model_dump(mode='json'),
            type=TransactionResponseType.GRT_UNISWAP_V3_BASE.name,
            status=TransactionStatusType.PENDING.name
        ))

        if txn.status == TransactionStatusType.PROCESSED:
            self.logger.info(f'Transaction {parsed_data.transaction.id} is already processed')
            return

        try:
            wallet: WalletORM = self.db.wallet_repo.get_wallet_by_address_and_chain(swap.origin, chain_id)
            if not wallet:
                raise Exception(f'Wallet {swap.origin} for txn {parsed_data.transaction.id} is not created on {chain_id.name}')

            base_token: TokenORM = self.token_service.add_token_if_not_exists(TokenORM(
                name=swap.base_token.name,
                symbol=swap.base_token.symbol,
                address=swap.base_token.id,
            ))
            quote_token: TokenORM = self.token_service.add_token_if_not_exists(TokenORM(
                name=swap.quote_token.name,
                symbol=swap.quote_token.symbol,
                address=swap.quote_token.id,
            ))

            pair: PairORM = self.pair_service.add_pair_if_not_exists(PairORM(
                symbol=base_token.symbol + "/" + quote_token.symbol,
                base_token_id=base_token.id,
                quote_token_id=quote_token.id,
                chain_id=chain_id.name,
                dex_id=dex_id.name,
                pair_address=swap.pool.id,
            ))
            if pair.base_token_id == base_token.id and swap.base_token_amount < 0:
                # Buy using base_token
                quantity = abs(swap.base_token_amount)
                native_price = abs(swap.quote_token_amount / swap.base_token_amount)
                usd_price = abs(swap.amountUSD / quantity)

                self.logger.info(f"Detected {TradeType.BUY} trade for pair {pair.symbol} (using base_token)")
                self.logger.info(
                    f'Creating it with quantity {quantity}, native price {native_price} and usd price {usd_price} '
                )
                self.trade_service.add_trade_if_not_exist(TradeORM(
                    pair_id=pair.id,
                    trade_type=TradeType.BUY.name,
                    native_price=native_price,
                    usd_price=usd_price,
                    quantity=quantity,
                    trade_timestamp=swap.timestamp,
                    wallet=wallet.id,
                    txn_id=txn.id
                ))

            elif pair.base_token_id == quote_token.id and swap.quote_token_amount < 0:
                # Buy using quote_token
                quantity = abs(swap.quote_token_amount)
                native_price = abs(swap.base_token_amount / swap.quote_token_amount)
                usd_price = abs(swap.amountUSD / quantity)

                self.logger.info(f"Detected {TradeType.BUY} trade for pair {pair.symbol} (using quote_token)")
                self.logger.info(
                    f'Creating it with quantity {quantity}, native price {native_price} and usd price {usd_price} '
                )
                self.trade_service.add_trade_if_not_exist(TradeORM(
                    pair_id=pair.id,
                    trade_type=TradeType.BUY.name,
                    native_price=native_price,
                    usd_price=usd_price,
                    quantity=quantity,
                    trade_timestamp=swap.timestamp,
                    wallet=wallet.id,
                    txn_id=txn.id
                ))

            elif pair.base_token_id == base_token.id and swap.base_token_amount > 0:
                # Sell using base_token
                quantity = abs(swap.base_token_amount)
                native_price = abs(swap.quote_token_amount / swap.base_token_amount)
                usd_price = abs(swap.amountUSD / quantity)

                self.logger.info(f"Detected {TradeType.SELL} trade for pair {pair.symbol} (using base_token)")
                self.logger.info(
                    f'Creating it with quantity {quantity}, native price {native_price} and usd price {usd_price} '
                )
                self.trade_service.add_trade_if_not_exist(TradeORM(
                    pair_id=pair.id,
                    trade_type=TradeType.SELL.name,
                    native_price=native_price,
                    usd_price=usd_price,
                    quantity=quantity,
                    trade_timestamp=swap.timestamp,
                    wallet=wallet.id,
                    txn_id=txn.id
                ))

            elif pair.base_token_id == quote_token.id and swap.quote_token_amount > 0:
                # Sell using quote_token
                quantity = abs(swap.quote_token_amount)
                native_price = abs(swap.base_token_amount / swap.quote_token_amount)
                usd_price = abs(swap.amountUSD / quantity)

                self.logger.info(f"Detected {TradeType.SELL} trade for pair {pair.symbol} (using quote_token)")
                self.logger.info(
                    f'Creating it with quantity {quantity}, native price {native_price} and usd price {usd_price} '
                )
                self.trade_service.add_trade_if_not_exist(TradeORM(
                    pair_id=pair.id,
                    trade_type=TradeType.SELL.name,
                    native_price=native_price,
                    usd_price=usd_price,
                    quantity=quantity,
                    trade_timestamp=swap.timestamp,
                    wallet=wallet.id,
                    txn_id=txn.id
                ))

            else:
                self.logger.warning(f"Unrecognized trade scenario for pair {pair.symbol} in transaction {txn.id}")
                raise Exception

            """
            if (pair.base_token_id == base_token.id and swap.base_token_amount < 0)\
                    or (pair.base_token_id == quote_token.id and swap.base_token_amount > 0):
                \"""if swap.base_token_amount > 0 and swap.quote_token_amount < 0:\"""
                # BUY Trade
                quantity = abs(swap.quote_token_amount)
                native_price = abs(swap.base_token_amount / swap.quote_token_amount)
                usd_price = abs(swap.amountUSD / quantity)

                self.logger.info(f"Detected {TradeType.BUY} trade for pair {pair.symbol}")
                self.logger.info(f'Creating it with quantity {quantity}, native price {native_price} and usd price {usd_price} ')
                self.trade_service.add_trade_if_not_exist(TradeORM(
                    pair_id=pair.id,
                    trade_type=TradeType.BUY.name,
                    native_price=native_price,
                    usd_price=usd_price,
                    quantity=quantity,
                    trade_timestamp=swap.timestamp,
                    wallet=wallet.id,
                    txn_id=txn.id
                ))
            else:
                \"""elif swap.base_token_amount < 0 and swap.quote_token_amount > 0:\"""
                # SELL Trade
                quantity = abs(swap.quote_token_amount)
                native_price = abs(swap.base_token_amount / swap.quote_token_amount)
                usd_price = abs(swap.amountUSD / quantity)

                self.logger.info(f"Detected {TradeType.SELL} trade for pair {pair.symbol}")
                self.logger.info(f'Creating it with quantity {quantity}, native price {native_price} and usd price {usd_price} ')
                self.trade_service.add_trade_if_not_exist(TradeORM(
                    pair_id=pair.id,
                    trade_type=TradeType.SELL.name,
                    native_price=native_price,
                    usd_price=usd_price,
                    quantity=quantity,
                    trade_timestamp=swap.timestamp,
                    wallet=wallet.id,
                    txn_id=txn.id
                ))
                """
        except Exception as e:
            self.logger.error(f"Failed to process transaction {parsed_data.data.transaction.id}: {e}")
            self.db.transaction_repo.update_status_by_id(txn.id, TransactionStatusType.FAILED)

        self.db.transaction_repo.update_status_by_id(txn.id, TransactionStatusType.PROCESSED)

    def mock_response_buy(self):
        response = """
        {
          "data": {
            "transaction": {
              "id": "0xb3f0a97f49edc53726f2b4c07c7730771885724b4af07e583064c5c5054bb2e7",
              "swaps": [
                {
                  "amount0": "0.003227603176913894",
                  "amount1": "-7669.789730553592407534",
                  "amountUSD": "9.995527343271135206049652860090665",
                  "origin": "0xbb594fbf1303d4e83341b68525f6b1656a9c2e14",
                  "pool": {
                    "id": "0x2007255830b907533fd615a038e2735840c0003f",
                    "token0Price": "0.0000004318306349360963725169934214798846",
                    "token1Price": "2315722.691022101940963549158533624"
                  },
                  "timestamp": "1731707751",
                  "token0": {
                    "id": "0x4200000000000000000000000000000000000006",
                    "name": "Wrapped Ether",
                    "symbol": "WETH"
                  },
                  "token1": {
                    "id": "0x8216e8143902a8fe0b676006bc25eb23829c123d",
                    "name": "wow",
                    "symbol": "wow"
                  }
                },
                {
                  "amount0": "-0.003227603176913894",
                  "amount1": "10",
                  "amountUSD": "9.995527343271135206049652860090665",
                  "origin": "0xbb594fbf1303d4e83341b68525f6b1656a9c2e14",
                  "pool": {
                    "id": "0xd0b53d9277642d899df5c87a3966a349a798f224",
                    "token0Price": "0.0002706553831586670875082187822557868",
                    "token1Price": "3694.73530631299917590602597545136"
                  },
                  "timestamp": "1731707751",
                  "token0": {
                    "id": "0x4200000000000000000000000000000000000006",
                    "name": "Wrapped Ether",
                    "symbol": "WETH"
                  },
                  "token1": {
                    "id": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
                    "name": "USD Coin",
                    "symbol": "USDC"
                  }
                }
              ]
            }
          }
        }"""
        return response

    def mock_response_sell(self):
        return """
        {
          "data": {
            "transaction": {
              "id": "0x5da30b21ce36139207fe04c32c740d6f14de3057bd6153fbf1580e507e567522",
              "swaps": [
                {
                  "amount0": "-0.003332215207333547",
                  "amount1": "3825",
                  "amountUSD": "11.83452649684081472335942030314523",
                  "origin": "0xbb594fbf1303d4e83341b68525f6b1656a9c2e14",
                  "pool": {
                    "id": "0x2007255830b907533fd615a038e2735840c0003f",
                    "token0Price": "0.0000006839853979514953273847750090088938",
                    "token1Price": "1462019.515321458336085322766343544"
                  },
                  "timestamp": "1732721729",
                  "token0": {
                    "id": "0x4200000000000000000000000000000000000006",
                    "name": "Wrapped Ether",
                    "symbol": "WETH"
                  },
                  "token1": {
                    "id": "0x8216e8143902a8fe0b676006bc25eb23829c123d",
                    "name": "wow",
                    "symbol": "wow"
                  }
                },
                {
                  "amount0": "0.003332215207333547",
                  "amount1": "-11.834853",
                  "amountUSD": "11.83452649684081472335942030314523",
                  "origin": "0xbb594fbf1303d4e83341b68525f6b1656a9c2e14",
                  "pool": {
                    "id": "0xd0b53d9277642d899df5c87a3966a349a798f224",
                    "token0Price": "0.0002713726836514599318435478394354495",
                    "token1Price": "3684.969270099268504691617433744658"
                  },
                  "timestamp": "1732721729",
                  "token0": {
                    "id": "0x4200000000000000000000000000000000000006",
                    "name": "Wrapped Ether",
                    "symbol": "WETH"
                  },
                  "token1": {
                    "id": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
                    "name": "USD Coin",
                    "symbol": "USDC"
                  }
                }
              ]
            }
          }
        }
        """
    def graphql_request(self):
        return """
        {
          transaction(
            id: "0xb3f0a97f49edc53726f2b4c07c7730771885724b4af07e583064c5c5054bb2e7"
          ) {
            id
            swaps {
              amount0
              amount1
              amountUSD
              token0 {
                id
                name
                symbol
              }
              token1 {
                id
                symbol
                name
              }
              origin
              timestamp
              pool {
                id
                token0Price
                token1Price
              }
            }
          }
        }
        """