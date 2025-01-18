from crypto_tracker.models import Transaction, DexIdType, ChainIdType
from crypto_tracker.services.transactions.transaction_extractor import TransactionExtractor


class VirtualBaseScanExtractor(TransactionExtractor):

    def __init__(self):
        super().__init__()

    def can_extract(self, dex_id: DexIdType, chain_id: ChainIdType) -> bool:
        return dex_id == DexIdType.VIRTUALS and chain_id == ChainIdType.BASE

    def extract(self, txn_hash: str) -> Transaction:
        # TODO: Add strategy pattern here, for virtuals we can scrape base scan buy txn:0xbd69c2f14897ead5af6e4944beccf1f54b85891099c002f950ddec719a2c2602 ,sell txn: 0x7e3789c9bb172c9450c133e7dd9be7acbdd8b5bde80fca02ba44af0d7e5702fb
        raise Exception