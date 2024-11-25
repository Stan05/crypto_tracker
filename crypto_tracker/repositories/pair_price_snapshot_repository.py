# crypto_tracker/repositories/pair_price_snapshot_repository.py

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func
from .base_repository import BaseRepository
from ..models import PairPriceSnapshotORM, PairPriceSnapshot, Symbol
from typing import List
from datetime import datetime

class PairPriceSnapshotRepository(BaseRepository):

    def get_price_snapshot(self, symbols) -> PairPriceSnapshot:
        price_snapshot: PairPriceSnapshot = self.session.query(PairPriceSnapshotORM).filter_by(symbol=symbols).first()
        
        if price_snapshot:
            return price_snapshot.map_to_model()
        return None
    
    def get_price_snapshots(self) -> List[PairPriceSnapshot]:
        query_results: List[PairPriceSnapshotORM] = self.session.query(PairPriceSnapshotORM).all()
        price_snapshots: List[PairPriceSnapshot] = []
        for row in query_results:
            price_snapshots.append(row.map_to_model())
        return price_snapshots


    def get_last_updated_on(self, symbol: Symbol) -> datetime:
        # Query the updated_on column and get the first result
        result = self.session.query(
            PairPriceSnapshotORM.updated_on
        ).filter_by(
            symbol=symbol.with_separator()
        ).first()

        # If result is not None, return the first (and only) element of the tuple, which is updated_on
        return result[0] if result else None  # Return None if no result is found
        
    def upsert_price_snapshot(self, price_snapshot: PairPriceSnapshot):
        stmt = insert(
                PairPriceSnapshotORM
            ).values(
                price_snapshot.map_to_orm()
            ).on_conflict_do_update(
                constraint=PairPriceSnapshotORM.symbol_unique_constrant_name(),
                set_={
                    PairPriceSnapshotORM.current_price: price_snapshot.current_price,
                    PairPriceSnapshotORM.updated_on: price_snapshot.updated_on
                }
        )
    
        self.session.execute(stmt)
        self.commit()
    