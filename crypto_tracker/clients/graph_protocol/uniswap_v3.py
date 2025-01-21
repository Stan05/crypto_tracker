from datetime import datetime
from typing import List, Type, Annotated
from pydantic import BaseModel, Field
from wireup import service, Inject

from crypto_tracker.configs.settings import Settings
from crypto_tracker.models import Transaction, Swap, Token, TradeType
from crypto_tracker.clients.graph_protocol.connector import GraphProtocolConnector


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

@service
class GrtUniswapSwapV3Connector(GraphProtocolConnector[GraphResponse, Transaction]):
    def __init__(self, settings: Annotated[Settings, Inject()]):
        self.pooled_tokens: [str] = settings.uniswap_pooled_tokens
        super().__init__(graphql_endpoint=settings.graph_uniswap_v3_url)

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
        graph_swap:GraphSwap = response.transaction.swaps[0]

        if self.pooled_tokens.__contains__(graph_swap.base_token.symbol):
            base_token = Token(
                    address = graph_swap.quote_token.id,
                    name = graph_swap.quote_token.name,
                    symbol = graph_swap.quote_token.symbol,
                )
            base_token_amount = graph_swap.quote_token_amount
            trade_type = TradeType.BUY if graph_swap.base_token_amount > 0 else TradeType.SELL
            quote_token = Token(
                address = graph_swap.base_token.id,
                name = graph_swap.base_token.name,
                symbol = graph_swap.base_token.symbol,
            )
            quote_token_amount = graph_swap.base_token_amount
        else:
            base_token = Token(
                address = graph_swap.base_token.id,
                name = graph_swap.base_token.name,
                symbol = graph_swap.base_token.symbol,
            )
            base_token_amount = graph_swap.base_token_amount
            trade_type = TradeType.BUY if graph_swap.quote_token_amount > 0 else TradeType.SELL
            quote_token = Token(
                    address = graph_swap.quote_token.id,
                    name = graph_swap.quote_token.name,
                    symbol = graph_swap.quote_token.symbol,
                )
            quote_token_amount = graph_swap.quote_token_amount

        swap: Swap = Swap(
            base_token_amount = base_token_amount,
            quote_token_amount = quote_token_amount,
            amount_USD = graph_swap.amountUSD,
            origin = graph_swap.origin,
            base_token = base_token,
            trade_type= trade_type,
            quote_token = quote_token,
            timestamp = graph_swap.timestamp,
            pool_id = graph_swap.pool.id
        )

        return Transaction(
            id=response.transaction.id,
            swap=swap,
            payload=response.model_dump(mode='json')
        )