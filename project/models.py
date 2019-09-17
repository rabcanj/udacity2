from app import app
import sqlalchemy as db
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


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

    def __repr__(self):
        return f'{self.name}'

class Item(Base):
    __tablename__ = 'ITEM'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    Category = Column(Integer)
    description = Column(String)

    def __repr__(self):
        return f'User {self.name}: {self.description}'
