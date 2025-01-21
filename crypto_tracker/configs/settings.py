from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from wireup import service


@service
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    binance_api_key: str = Field(alias="binance_api_key")
    binance_api_secret: str = Field(alias="binance_api_secret")
    binance_tld: str = Field(alias="binance_tld")

    db_uri: str = Field(alias="db_uri")

    alchemy_base_url: str = Field(alias="alchemy_base_url")
    subgraph_api_key: str = Field(alias="subgraph_api_key")
    graph_uniswap_v3_url: str = Field(alias="graph_uniswap_v3_url")
    uniswap_pooled_tokens: str = Field(alias="uniswap_pooled_tokens")
