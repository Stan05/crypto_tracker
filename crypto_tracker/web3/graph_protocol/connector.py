import asyncio
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic, Dict, Any
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from pydantic import BaseModel

# Define a generic type for the response model
T = TypeVar("T", bound=BaseModel)

class GraphProtocolConnector(ABC, Generic[T]):
    def __init__(self, graphql_endpoint: str):
        """
        Initialize the GraphQL client with the provided endpoint.

        Args:
            graphql_endpoint (str): URL of the GraphQL API.
        """
        self.transport = AIOHTTPTransport(url=graphql_endpoint)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    @abstractmethod
    def get_query(self) -> str:
        """
        Abstract method to define the GraphQL query.
        Must be implemented by subclasses.

        Returns:
            str: The GraphQL query string.
        """
        pass

    @abstractmethod
    def get_response_model(self) -> Type[T]:
        """
        Abstract method to define the Pydantic model for parsing the response.
        Must be implemented by subclasses.

        Returns:
            Type[T]: The Pydantic model class.
        """
        pass

    async def _async_fetch(self, variables: Dict[str, Any]) -> T:
        """
        Asynchronous method to execute the query and return the parsed response.

        Args:
            variables (Dict[str, Any]): Variables for the GraphQL query.

        Returns:
            T: Parsed response as a Pydantic model instance.
        """
        query = gql(self.get_query())
        async with self.client as session:
            response = await session.execute(query, variable_values=variables)
            print(response)
            response_model = self.get_response_model()
            return response_model.model_validate(response)

    def fetch(self, variables: Dict[str, Any]) -> T:
        """
        Synchronous method to execute the query and return the parsed response.

        Args:
            variables (Dict[str, Any]): Variables for the GraphQL query.

        Returns:
            T: Parsed response as a Pydantic model instance.
        """
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self._async_fetch(variables))
        finally:
            loop.close()
