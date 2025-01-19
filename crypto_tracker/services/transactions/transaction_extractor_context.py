from crypto_tracker.configs.logger import Logger
from crypto_tracker.models import DexIdType, ChainIdType, Transaction
from crypto_tracker.services.transactions.extractors.uniswap_base_extractor import UniswapBaseExtractor
from crypto_tracker.services.transactions.extractors.virtual_base_scan_extractor import VirtualBaseScanExtractor
from crypto_tracker.services.transactions.transaction_extractor import TransactionExtractor


class TransactionExtractorContext:
    def __init__(self):
        self._strategies:[TransactionExtractor] = [
            UniswapBaseExtractor(),
            VirtualBaseScanExtractor()
        ]
        self.logger = Logger()

    def extract(self, txn_hash:str, dex_id: DexIdType, chain_id:ChainIdType) -> Transaction:
        for strategy in self._strategies:
            if strategy.can_extract(dex_id, chain_id):
                return strategy.extract(txn_hash)

        self.logger.error(f"Could not find extractor for {dex_id} on {chain_id}")
        raise Exception
