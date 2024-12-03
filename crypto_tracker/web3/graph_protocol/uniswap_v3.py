from datetime import datetime
from typing import List, Type
from pydantic import BaseModel, Field

from crypto_tracker.config import Config
from crypto_tracker.web3.graph_protocol.connector import GraphProtocolConnector


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

class GraphResponse(BaseModel):
    transaction: Transaction

class GrtUniswapSwapV3Connector(GraphProtocolConnector[GraphResponse]):
    def __init__(self):
        self.config = Config()
        super().__init__(graphql_endpoint=self.config.GRAPH_UNISWAP_V3_URL)

    def get_query(self) -> str:
        return """
                query getTransaction($transactionId: ID!) {
                  transaction(id: $transactionId) {
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
                        name
                        symbol
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

    def get_response_model(self) -> Type[GraphResponse]:
        return GraphResponse
