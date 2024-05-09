from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class TradePair:
    coin_id: Optional[int]
    base_coin_amount : float
    coin_amount : float
    min_amount_out: float
    current_price : float
    execution_price: float
    price_impact : float
    is_pump_fun : bool
    platform_fee: float
    base_currency: str
    quote_currency: str
