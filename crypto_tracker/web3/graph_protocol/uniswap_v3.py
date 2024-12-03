from datetime import datetime
from typing import List, Type
from pydantic import BaseModel, Field

from crypto_tracker.config import Config
from crypto_tracker.models import Transaction, Swap, Token
from crypto_tracker.web3.graph_protocol.connector import GraphProtocolConnector, T


class GraphToken(BaseModel):
    id: str
    name: str
    symbol: str

class GraphPool(BaseModel):
    id: str
    base_token_price: str = Field(alias="token0Price")
    quote_token_price: str = Field(alias="token1Price")

class GraphSwap(BaseModel):
    base_token_amount: float = Field(alias="amount0")
    quote_token_amount: float = Field(alias="amount1")
    amountUSD: float
    origin: str
    base_token: GraphToken = Field(alias="token0")
    quote_token: GraphToken = Field(alias="token1")
    timestamp: datetime
    pool: GraphPool

class GraphTransaction(BaseModel):
    id: str
    swaps: List[GraphSwap]

class GraphResponse(BaseModel):
    transaction: GraphTransaction

class GrtUniswapSwapV3Connector(GraphProtocolConnector[GraphResponse, Transaction]):
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

    def get_response_model_type(self) -> Type[GraphResponse]:
        return GraphResponse

    def get_model_type(self) -> Type[Transaction]:
        return Transaction


    def transform_response(self, response: GraphResponse) -> Transaction:
        """
        Transform the GraphResponse into the internal Transaction model.

        Args:
            response (GraphResponse): The parsed GraphQL response.

        Returns:
            Transaction: The internal Transaction model instance.
        """
        swap: Swap = Swap(
            base_token_amount = response.transaction.swaps[0].base_token_amount,
            quote_token_amount = response.transaction.swaps[0].quote_token_amount,
            amount_USD = response.transaction.swaps[0].amountUSD,
            origin = response.transaction.swaps[0].origin,
            base_token = Token(
                address = response.transaction.swaps[0].base_token.id,
                name = response.transaction.swaps[0].base_token.name,
                symbol = response.transaction.swaps[0].base_token.symbol,
            ),
            quote_token = Token(
                    address = response.transaction.swaps[0].quote_token.id,
                    name = response.transaction.swaps[0].quote_token.name,
                    symbol = response.transaction.swaps[0].quote_token.symbol,
                ),
            timestamp = response.transaction.swaps[0].timestamp,
            pool_id = response.transaction.swaps[0].pool.id
        )

        return Transaction(
            id=response.transaction.id,
            swap=swap,
            payload=response.model_dump(mode='json')
        )