from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from src.database.database_configuration import Base


def default_datetime():
    return datetime.now()


class CoinInfo(Base):
    __tablename__ = "coin_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, unique=True, nullable=False)
    mint_address = Column(String(300), unique=True)
    name = Column(String(250))
    symbol = Column(String(250))
    creator = Column(String(250), nullable=True)
    cap = Column(Float)
    dev_percentage = Column(Float, nullable=True)
    created_at = Column(DateTime, default=default_datetime)
    updated_at = Column(DateTime, default=default_datetime)


class TradePair(Base):
    __tablename__ = "trade_pair"
    id = Column(Integer, primary_key=True, autoincrement=True)
    base_currency = Column(String(300))
    quote_currency = Column(String(300))
    amount_in = Column(Float)
    amount_out = Column(Float)
    min_amount_out = Column(Float, nullable=True)

    current_price = Column(Float, nullable=True)
    execution_price = Column(Float, nullable=True)
    price_impact = Column(Float, nullable=True)

    fee = Column(Float)
    platform_fee = Column(Float)
    platform_fee_ui = Column(Float)

    holders = Column(Integer(), nullable=True, default=2)
    traded = Column(Boolean, default=False)
    is_pump_fun = Column(Boolean, default=True)

    txid = Column(Text(2500), nullable=False)
    txid_url = Column(Text(2500))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    coin_id = Column(Integer, ForeignKey("coin_info.id"), nullable=False)
    coin = relationship("CoinInfo", foreign_keys=[coin_id])


class Portfolio(Base):
    __tablename__ = "portfolio"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float)
    bought_at = Column(Float)
    sold_at = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    in_hold = Column(Boolean, default=False)
    profit = Column(Float, nullable=True)

    trade_pair_id = Column(Integer, ForeignKey("trade_pair.id"), nullable=True)
    trade_pair = relationship("TradePair", foreign_keys=[trade_pair_id], lazy="joined")

    coin_id = Column(Integer, ForeignKey("coin_info.id"), nullable=True)
    coin = relationship("CoinInfo", foreign_keys=[coin_id], lazy="joined")


class Configurations(Base):
    __tablename__ = "configurations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    solana_wallet_address = Column(String(300), nullable=False)
    current_holders = Column(Integer, default=2)
    amount_to_buy = Column(Float, nullable=False, default=0.05)
    buy_slippage_rate = Column(Float, nullable=False, default=10)
    sell_slippage_rate = Column(Float, nullable=False, default=10)
    expected_profit = Column(Float, nullable=False, default=2)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    market_cap_min = Column(Float, nullable=False, default=4750)
    market_cap_max = Column(Float, nullable=False, default=10000)

    first_wait_seconds = Column(Integer, default=60)
    second_wait_seconds = Column(Integer, default=30)
    third_wait_seconds = Column(Integer, default=15)

    priority_fee_buy = Column(Integer, default=0)
    priority_fee_sell = Column(Integer, default=0)

    dev_percentage_min = Column(Float, default=0)
    dev_percentage_max = Column(Float, nullable=False)
