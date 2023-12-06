from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, Enum, DateTime, Boolean, String, Float

Base = declarative_base()

class Trade(Base):
    __tablename__ = 'trades'
    
    _id = Column("id", BigInteger, primary_key=True)
    side = Column(Enum("BUY", "SELL", name="side_enum"), nullable=False)
    qty = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __init__(self, side, qty, price, timestamp):
        self.side = side
        self.qty = qty
        self.price = price
        self.timestamp = timestamp