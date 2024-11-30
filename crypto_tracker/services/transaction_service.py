# crypto_tracker/services/wallet_service.py
from typing import List

from pydantic import BaseModel, Field

from crypto_tracker.database import Database
from crypto_tracker.logger import Logger
from crypto_tracker.models import ChainIdType, DexIdType
from crypto_tracker.repositories.models.base import TradeORM, TokenORM
from crypto_tracker.services.token_service import TokenService


class Token(BaseModel):
    id: str
    name: str
    symbol: str

class Pair(BaseModel):
    id: str
    created_at_timestamp: str = Field(alias="createdAtTimestamp")
    base_token: Token = Field(alias="token0")
    base_token_price: str = Field(alias="token0Price")
    quote_token: Token = Field(alias="token1")
    quote_token_price: str = Field(alias="token1Price")

class Transaction(BaseModel):
    id: str

class Swap(BaseModel):
    base_token_in: str = Field(alias="amount0In")
    base_token_out: str = Field(alias="amount0Out")
    quote_token_in: str = Field(alias="amount1In")
    quote_token_out: str = Field(alias="amount1Out")
    amountUSD: str
    from_: str  = Field(alias="from")
    pair: Pair
    timestamp: str
    transaction: Transaction

class SwapData(BaseModel):
    swaps: List[Swap]

class GraphResponse(BaseModel):
    data: SwapData

class TransactionService:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()
        self.token_service = TokenService()

    def query_txn(self, txn_id:str, chain_id:ChainIdType, dex_id: DexIdType):
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

        response = self.mock_response()
        # Parse into Pydantic models
        parsed_data: GraphResponse = GraphResponse.model_validate_json(response)
        swap = parsed_data.data.swaps[0]

        self.token_service.add_token_if_not_exists(TokenORM(
            name=swap.pair.base_token.name,
            symbol=swap.pair.base_token.symbol,
            address=swap.pair.base_token.id,
        ))
        self.token_service.add_token_if_not_exists(TokenORM(
            name=swap.pair.quote_token.name,
            symbol=swap.pair.quote_token.symbol,
            address=swap.pair.quote_token.id,
        ))

    def mock_response(self):
        response = """{
          "data": {
            "swaps": [
              {
                "amount0In": "0",
                "amount0Out": "82350.772588191259786961",
                "amount1In": "0.00148734422928963",
                "amount1Out": "0",
                "amountUSD": "2.492510917589027955572665595974938",
                "from": "0xbb594fbf1303d4e83341b68525f6b1656a9c2e14",
                "pair": {
                  "createdAtTimestamp": "1732127479",
                  "id": "0xedb7ed285c2714521c6f9a82893f2b5608309f98",
                  "token0": {
                    "id": "0x3d02347709916802327e062fd545f579ed1d528a",
                    "name": "Vibes",
                    "symbol": "VIBES"
                  },
                  "token0Price": "79055129.56459102511546765756861757",
                  "token1": {
                    "id": "0x4200000000000000000000000000000000000006",
                    "name": "Wrapped Ether",
                    "symbol": "WETH"
                  },
                  "token1Price": "0.00000001264940055765720111665560081340741"
                },
                "timestamp": "1732212105",
                "transaction": {
                  "id": "0xd1659825b49b14fbe4e54f3afee433cd1527eeb4a97b890dd1bd4152b9cd45ba"
                }
              },
              {
                "amount0In": "0",
                "amount0Out": "0.00148734422928963",
                "amount1In": "5",
                "amount1Out": "0",
                "amountUSD": "4.992510917589027955572665595974938",
                "from": "0xbb594fbf1303d4e83341b68525f6b1656a9c2e14",
                "pair": {
                  "createdAtTimestamp": "1707842333",
                  "id": "0x88a43bbdf9d098eec7bceda4e2494615dfd9bb9c",
                  "token0": {
                    "id": "0x4200000000000000000000000000000000000006",
                    "name": "Wrapped Ether",
                    "symbol": "WETH"
                  },
                  "token0Price": "0.0002720286650024295907519199021085593",
                  "token1": {
                    "id": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
                    "name": "USD Coin",
                    "symbol": "USDC"
                  },
                  "token1Price": "3676.083180392289254890217517355092"
                },
                "timestamp": "1732212105",
                "transaction": {
                  "id": "0xd1659825b49b14fbe4e54f3afee433cd1527eeb4a97b890dd1bd4152b9cd45ba"
                }
              }
            ]
          }
        }"""
        return response

