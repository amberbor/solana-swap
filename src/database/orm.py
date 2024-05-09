from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from src.database.database_configuration import Base



def default_datetime():
    return datetime.now()

class CoinInfo(Base):
    __tablename__ = 'coin_info'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, unique=True, nullable=False)
    mint_address = Column(String(300), unique=True)
    name = Column(String(250))
    symbol = Column(String(250))
    creator = Column(String(250), nullable=True)
    cap = Column(Float)
    dev_percentage = Column(Float, default=0)
    bought = Column(Float)
    created_at = Column(DateTime, default=default_datetime)

class TradePair(Base):
    __tablename__ = 'trade_pair'
    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey('coin_info.id'), nullable=False)
    base_coin_amount = Column(Float)
    coin_amount = Column(Float)
    min_amount_out = Column(Float, nullable=True)
    current_price = Column(Float, nullable=True)
    execution_price = Column(Float, nullable=True)
    price_impact = Column(Float, nullable=True)
    is_pump_fun = Column(Boolean, default=True)
    platform_fee = Column(Float)
    base_currency = Column(String(250))
    quote_currency = Column(String(250))

class Portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True)
    txid = Column(String, unique=True, nullable=False)
    txid_url = Column(String(500), unique=True)
    trade_pair_id = Column(Integer, ForeignKey('trade_pair.id'), nullable=False)
    amount = Column(Float, nullable=False)
    base_amount = Column(Float)

class Configurations(Base):
    __tablename__ = 'configurations'
    id = Column(Integer, primary_key=True)
    dev_percentage_min = Column(Float, default=0)
    dev_percentage_max = Column(Float, nullable=False)
    current_holders = Column(Integer, default=2)
    capital_coin = Column(Float, nullable=False, default=5000)
    amount_to_buy = Column(Float, nullable=False, default=0.05)
    slippage_rate = Column(Float, nullable=False, default=10)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
