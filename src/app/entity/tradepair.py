from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass(kw_only=True)
class TradePairEntity:
    txid: Optional[str] = None
    txid_url: Optional[str] = None
    coin_id: Optional[int] = None
    base_coin_amount: float
    coin_amount: float
    min_amount_out: float
    current_price: float
    execution_price: float
    price_impact: float
    fee: Optional[bool] = None
    platform_fee: float
    platform_fee_ui: Optional[bool] = None
    base_currency: str
    quote_currency: str
    holders: Optional[int] = 2
    is_pump_fun: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # is_jupiter: Optional[bool] = None
