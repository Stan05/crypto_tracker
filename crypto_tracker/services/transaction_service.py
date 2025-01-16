# crypto_tracker/services/transaction_service.py

from crypto_tracker.database import Database
from crypto_tracker.logger import Logger
from crypto_tracker.models import ChainIdType, DexIdType, TradeType, TransactionResponseType, TransactionStatusType, \
    Transaction
from crypto_tracker.repositories.models.base import TradeORM, TokenORM, PairORM, WalletORM, TransactionORM
from crypto_tracker.scrapers.base_scan_scraper import BaseScraper
from crypto_tracker.services.pair_service import PairService
from crypto_tracker.services.token_service import TokenService
from crypto_tracker.services.trade_service import TradeService
from crypto_tracker.web3.graph_protocol.uniswap_v3 import GrtUniswapSwapV3Connector

class TransactionService:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()
        self.token_service = TokenService()
        self.pair_service = PairService()
        self.trade_service = TradeService()
        self.uniswap = GrtUniswapSwapV3Connector()
        self.base_scraper = BaseScraper()

    def add_txn_if_not_exist(self, txn: TransactionORM) -> TransactionORM:
        existing_txn = self.db.transaction_repo.get_txn_by_hash(txn.hash)
        if not existing_txn:
            self.logger.info(f'Trade {txn.hash} does not exist creating it')
            return self.db.transaction_repo.create(txn)
        return existing_txn

    def process_transaction(self, txn_hash:str, chain_id:ChainIdType, dex_id: DexIdType):
        if chain_id is not ChainIdType.BASE:
            raise Exception(f'Querying chain {chain_id} is not supported yet')
        if dex_id is not DexIdType.UNISWAP:
            raise Exception(f'Querying dex {dex_id} is not supported yet')

        """
        1. Check if wallet is created, otherwise throw and has the ability to reprocess
        2. Check if tokens in txn are created, if not create them
        3. Check if pair in txn is created, if not create it
        4. Add the trade
        """
        try:
            transaction:Transaction = self.uniswap.fetch(variables={"transactionId": txn_hash})
        except RuntimeError as e:
            print(f"Error: {e}")
            return

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
            self.logger.error(f"Failed to process transaction {transaction.data.transaction.id}: {e}")
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

    def scrape_transaction(self, txn_id: str, chain_id: ChainIdType, dex_id: DexIdType) -> int:
        result = self.base_scraper.get_transaction(txn_id)

        self.logger.info(result)
        return 1

