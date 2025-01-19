# crypto_tracker/services/transaction_service.py
from wireup import service

from crypto_tracker.database import Database
from crypto_tracker.configs.logger import Logger
from crypto_tracker.models import ChainIdType, DexIdType, TradeType, TransactionResponseType, TransactionStatusType, \
    Transaction
from crypto_tracker.repositories.models.base import TradeORM, TokenORM, PairORM, WalletORM, TransactionORM
from crypto_tracker.services.pair_service import PairService
from crypto_tracker.services.token_service import TokenService
from crypto_tracker.services.trade_service import TradeService
from crypto_tracker.services.transactions.transaction_extractor_context import TransactionExtractorContext

@service
class TransactionService:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()
        self.token_service = TokenService()
        self.pair_service = PairService()
        self.trade_service = TradeService()
        self.transaction_extractor_context = TransactionExtractorContext()

    def add_txn_if_not_exist(self, txn: TransactionORM) -> TransactionORM:
        existing_txn = self.db.transaction_repo.get_txn_by_hash(txn.hash)
        if not existing_txn:
            self.logger.info(f'Trade {txn.hash} does not exist creating it')
            return self.db.transaction_repo.create(txn)
        return existing_txn

    def process_transaction(self, txn_hash:str, chain_id:ChainIdType, dex_id: DexIdType):
        """
        1. Check if wallet is created, otherwise throw and has the ability to reprocess
        2. Check if tokens in txn are created, if not create them
        3. Check if pair in txn is created, if not create it
        4. Add the trade
        """
        transaction: Transaction = self.transaction_extractor_context.extract(txn_hash, dex_id, chain_id)

        txn: TransactionORM = self.add_txn_if_not_exist(TransactionORM(
            hash=transaction.id,
            payload=transaction.payload,
            type=TransactionResponseType.GRT_UNISWAP_V3_BASE.name,
            status=TransactionStatusType.PENDING.name
        ))

        if txn.status == TransactionStatusType.PROCESSED:
            self.logger.info(f'Transaction {transaction.id} is already processed')
            return

        try:
            swap = transaction.swap
            wallet: WalletORM = self.db.wallet_repo.get_wallet_by_address_and_chain(swap.origin, chain_id)
            if not wallet:
                raise Exception(f'Wallet {swap.origin} for txn {transaction.id} is not created on {chain_id.name}')

            base_token: TokenORM = self.token_service.add_token_if_not_exists(TokenORM(
                name=swap.base_token.name,
                symbol=swap.base_token.symbol,
                address=swap.base_token.address,
            ))
            quote_token: TokenORM = self.token_service.add_token_if_not_exists(TokenORM(
                name=swap.quote_token.name,
                symbol=swap.quote_token.symbol,
                address=swap.quote_token.address,
            ))

            pair: PairORM = self.pair_service.add_pair_if_not_exists(PairORM(
                symbol=base_token.symbol + "/" + quote_token.symbol,
                base_token_id=base_token.id,
                quote_token_id=quote_token.id,
                chain_id=chain_id.name,
                dex_id=dex_id.name,
                pair_address=swap.pool_id,
            ))

            native_price, quantity, usd_price = self.__calculate_trade_props(pair, swap, txn)
            self.logger.info(f"Detected {swap.trade_type} trade for pair {pair.symbol}")
            self.logger.info(
                f'Creating it with quantity {quantity}, native price {native_price} and usd price {usd_price} '
            )
            self.trade_service.add_trade_if_not_exist(TradeORM(
                pair_id=pair.id,
                trade_type=swap.trade_type.name,
                native_price=native_price,
                usd_price=usd_price,
                quantity=quantity,
                trade_timestamp=swap.timestamp,
                wallet=wallet.id,
                txn_id=txn.id
            ))

        except Exception as e:
            self.logger.error(f"Failed to process transaction {transaction.id}: {e}")
            self.db.transaction_repo.update_status_by_id(txn.id, TransactionStatusType.FAILED)

        self.db.transaction_repo.update_status_by_id(txn.id, TransactionStatusType.PROCESSED)

    def __calculate_trade_props(self, pair, swap, txn):
        if swap.trade_type == TradeType.BUY:
            quantity = abs(swap.base_token_amount)
            native_price = abs(swap.quote_token_amount / swap.base_token_amount)
            usd_price = abs(swap.amount_USD / quantity)
        elif swap.trade_type == TradeType.SELL:
            quantity = abs(swap.base_token_amount)
            native_price = abs(swap.quote_token_amount / swap.base_token_amount)
            usd_price = abs(swap.amount_USD / quantity)
        else:
            self.logger.error(f"Unrecognized trade scenario for pair {pair.symbol} in transaction {txn.id}")
            raise Exception
        return native_price, quantity, usd_price

