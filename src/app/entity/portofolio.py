from dataclasses import dataclass
from .tradepair import TradePairEntity
from .coin_info import CoinInfoEntity
from typing import Optional, Union
from datetime import datetime
from src.app.services.database import DatabaseManager


@dataclass(kw_only=True)
class PortofolioEntity:
    trade_pair: Optional[TradePairEntity | None] = None
    coin_info: Optional[CoinInfoEntity | None] = None
    amount: Optional[float] = 0
    bought_at: Optional[float] = 0
    sold_at: Optional[float | None] = None
    profit: Optional[float | None] = None
    in_hold: Optional[bought_at] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    buy_type: Optional[bool] = True

    def __post_init__(self):
        if self.trade_pair:
            self.amount = self.trade_pair.coin_amount
            self.bought_at = self.trade_pair.execution_price

            if self.buy_type == True:
                self.in_hold = True
            else:
                self.in_hold = False
