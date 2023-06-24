from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, func, String

Base = declarative_base()


class Yad2Data(Base):
    __tablename__ = 'yad_2_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=func.now())
    title = Column(String)
    description = Column(String)
    price_element = Column(Integer)
    rooms = Column(Integer)
    area = Column(Integer)
    merchant = Column(String)

    def __repr__(self):
        return f"<Property(head='{self.head}', details='{self.details}', price='{self.price}', " \
               f"rooms='{self.rooms}', size='{self.size}', merchant='{self.merchant}')>"
