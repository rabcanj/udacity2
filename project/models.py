from app import app
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'USERS'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    def __repr__(self):
        return f'User {self.name}'

class Category(Base):
    __tablename__ = 'CATEGORY'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    item = relationship("Item")

    def __repr__(self):
        return f'{self.name}'

class Item(Base):
    __tablename__ = 'ITEM'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey('CATEGORY.id'))
    description = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'{self.name}'
