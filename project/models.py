from app import app
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = 'CATEGORY'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def get_dict(self):
        return {
            'id':self.id,
            'name':self.name
        }

    def __repr__(self):
        return f'{self.name}'

class Item(Base):
    __tablename__ = 'ITEM'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey('CATEGORY.id'))
    category = relationship("Category", backref='Item')
    description = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    user_email = Column(String)

    def __repr__(self):
        return f'{self.name} ({self.category_id})'

    def get_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'description':self.description,
            'name':self.name,
            'created_date':self.created_date,
            'user_email':self.user_email
        }
