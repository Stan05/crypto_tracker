from abc import ABC, abstractmethod

from crypto_tracker.models import DexIdType, ChainIdType, Transaction


class TransactionExtractor(ABC):
    @abstractmethod
    def can_extract(self, dex_id:DexIdType, chain_id:ChainIdType) -> bool:
        """Determine if the extractor can execute."""
        pass

    @abstractmethod
    def extract(self, txn_hash:str) -> Transaction:
        """Extract the transaction."""
        pass