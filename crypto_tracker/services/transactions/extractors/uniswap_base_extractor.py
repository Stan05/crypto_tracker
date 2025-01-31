from typing import Annotated

from wireup import service, Inject

from crypto_tracker.models import Transaction, DexIdType, ChainIdType
from crypto_tracker.services.transactions.transaction_extractor import TransactionExtractor
from crypto_tracker.clients.graph_protocol.uniswap_v3 import GrtUniswapSwapV3Connector

@service
class UniswapBaseExtractor(TransactionExtractor):

    def __init__(self, uniswap: Annotated[GrtUniswapSwapV3Connector, Inject()]):
        super().__init__()
        self.uniswap = uniswap

    def can_extract(self, dex_id: DexIdType, chain_id: ChainIdType) -> bool:
        return dex_id == DexIdType.UNISWAP and chain_id == ChainIdType.BASE

    def extract(self, txn_hash: str) -> Transaction:
        return self.uniswap.fetch(variables={"transactionId": txn_hash})