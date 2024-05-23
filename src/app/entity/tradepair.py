from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from database.orm import TradePair
from app.entity import CoinInfoEntity


@dataclass(kw_only=True)
class TradePairEntity:
    base_currency: str
    quote_currency: str
    amount_in: float
    amount_out: float
    min_amount_out: float

    current_price: float
    execution_price: float
    price_impact: float

    fee: Optional[bool]
    platform_fee: float
    platform_fee_ui: Optional[bool] = None

    holders: Optional[int] = None
    traded: Optional[int] = False
    is_pump_fun: Optional[bool] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    txid: Optional[str] = None
    txid_url: Optional[str] = None

    coin: Optional[CoinInfoEntity] = None

    def db_entity(self, coin_db=None, holders=None):
        return TradePair(
            txid=self.txid,
            txid_url=self.txid_url,
            amount_in=self.amount_in,
            amount_out=self.amount_out,
            min_amount_out=self.min_amount_out,
            current_price=self.current_price,
            execution_price=self.execution_price,
            price_impact=self.price_impact,
            is_pump_fun=self.is_pump_fun,
            platform_fee=self.platform_fee,
            base_currency=self.base_currency,
            quote_currency=self.quote_currency,
            holders=self.holders,
            traded=self.traded,
            updated_at=self.updated_at,
            created_at=self.created_at,
            coin=coin_db,
        )
