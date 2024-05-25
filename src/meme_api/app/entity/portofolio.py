from dataclasses import dataclass
from .tradepair import TradePairEntity
from .coin_info import CoinInfoEntity
from typing import Optional
from datetime import datetime
from meme_api.database.orm import Portfolio


@dataclass(kw_only=True)
class PortofolioEntity:
    amount: Optional[float] = 0
    bought_at: Optional[float] = 0
    sold_at: Optional[float | None] = None
    profit: Optional[float | None] = None
    in_hold: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    trade_pair: Optional[TradePairEntity | None] = None
    coin_info: Optional[CoinInfoEntity | None] = None

    buy_type: Optional[bool] = True

    def __post_init__(self):
        if self.trade_pair:
            self.amount = self.trade_pair.amount_out
            self.bought_at = self.trade_pair.execution_price

            if self.buy_type == True:
                self.in_hold = True
            else:
                self.in_hold = False

    def db_entity(self, coin_db=None):
        return Portfolio(
            trade_pair=self.trade_pair.db_entity(coin_db),
            coin=coin_db,
            amount=self.amount,
            bought_at=self.bought_at,
            sold_at=self.sold_at,
            profit=self.profit,
            in_hold=self.in_hold,
        )
