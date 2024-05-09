from dataclasses import dataclass

@dataclass(kw_only=True)
class Portofolio:
    txid : str
    txid_url : str
    trade_pair : str
    amount : float
    base_amount : float