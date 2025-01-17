from crypto_tracker.models import Transaction, DexIdType, ChainIdType
from crypto_tracker.services.transactions.transaction_extractor import TransactionExtractor


class VirtualBaseScanExtractor(TransactionExtractor):

    def __init__(self):
        super().__init__()

    def can_extract(self, dex_id: DexIdType, chain_id: ChainIdType) -> bool:
        return dex_id == DexIdType.VIRTUALS and chain_id == ChainIdType.BASE

    def extract(self, txn_hash: str) -> Transaction:

        raise Exception