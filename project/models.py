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
        return f'User {self.name}'

class Item(Base):
    __tablename__ = 'ITEM'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    Category = Column(Integer)
    description = Column(String)

    def __repr__(self):
        return f'User {self.name}: {self.description}'


@app.route('/create_database')
def hello_from():
    engine = db.create_engine('sqlite:///census.sqlite')
    connection = engine.connect()
    Base.metadata.create_all(engine)



    # metadata = db.MetaData()
    # census = db.Table('census', metadata, autoload=True, autoload_with=engine)
    # query = db.select([census])
    # ResultProxy = connection.execute(query)
    # ResultSet = ResultProxy.fetchall()
    # print(ResultSet[:3])
    return('done')
