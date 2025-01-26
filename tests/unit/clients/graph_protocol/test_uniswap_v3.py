
import json
from unittest.mock import AsyncMock, patch

import pydantic
import pytest
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from crypto_tracker.clients.graph_protocol.uniswap_v3 import GrtUniswapSwapV3Connector
from crypto_tracker.configs.settings import Settings
from crypto_tracker.models import Transaction
from tests.utils import get_source_file_from_test_resources


@pytest.fixture
def grt_uniswap_swap_v3_connector(settings: Settings):
    return GrtUniswapSwapV3Connector(settings)

def test_get_query_return(grt_uniswap_swap_v3_connector: GrtUniswapSwapV3Connector):
    assert grt_uniswap_swap_v3_connector.get_query() == """
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
testdata = [
    ("PUBLIUS-WETH-SELL.json", "PUBLIUS-WETH-SELL.json"),
    ("PUBLIUS-WETH-BUY.json", "PUBLIUS-WETH-BUY.json"),
    ("wow-WETH-BUY-inverted-base-quote-tokens.json", "wow-WETH-BUY.json"),
    ("wow-WETH-SELL-inverted-base-quote-tokens.json", "wow-WETH-SELL.json"),
    ("ANON-WETH-BUY-inverted-swaps.json", "ANON-WETH-BUY.json")
]
@pytest.mark.parametrize("graph_response_file,expected_transaction_file", testdata)
def test_fetch_should_return_expected(settings: Settings, graph_response_file:str, expected_transaction_file: str):
    # Load the mock response from a file
    with open(get_source_file_from_test_resources(f'graph_responses/{graph_response_file}'), "r") as f:
        mock_response = json.load(f)

    # Load the expected Transaction object from a file
    with open(get_source_file_from_test_resources(f'expected_transactions/{expected_transaction_file}')) as f:
        expected_transaction = pydantic.TypeAdapter(Transaction).validate_json(f.read())

    # Patch the `__aenter__` method to mock the session and its `execute` method
    with patch.object(AIOHTTPTransport, "__init__", return_value=None), \
         patch.object(Client, "__aenter__", AsyncMock()) as mock_aenter, \
         patch.object(Client, "__aexit__", AsyncMock()):

        # Mock the session's `execute` method
        mock_session = AsyncMock()
        mock_session.execute.return_value = mock_response
        mock_aenter.return_value = mock_session

        # Initialize the connector
        grt_uniswap_swap_v3_connector = GrtUniswapSwapV3Connector(settings)

        # Call the synchronous `fetch` method
        result = grt_uniswap_swap_v3_connector.fetch({"transactionId": "123"})

        # Assertions
        assert result.payload is not None
        assert result.model_copy(update={'payload': {}}) == expected_transaction  # Compare the result with the expected Transaction object
        mock_session.execute.assert_called_once_with(
            gql(grt_uniswap_swap_v3_connector.get_query()), variable_values={"transactionId": "123"}
        )
