from app import app
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from .models import Category, Item, Base
import os
from flask import redirect, url_for
def get_connection(db_engine='sqlite:///catalog.sqlite'):
    engine = db.create_engine(db_engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return engine.connect(), session, engine


@app.route('/create_database')
def create_database():
    # Create database and fill it with basic data
    connection, session, engine = get_connection()
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())
    Base.metadata.create_all(engine)
    session.add(Category(name='CPUs'))
    session.add(Category(name='Mother Boards'))
    session.add(Category(name='Graphic Cards'))
    session.add(Category(name='HDD/SSD disks'))
    session.add(Category(name='Monitors'))

    category=session.query(Category).filter(Category.name=='CPUs').first()
    new_item = Item(
        name="Intel Core i7",
        description='4 Cores, 8 Threads. Intel Optane Memory Supported',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    new_item = Item(
        name="Intel Core i5",
        description='4 Cores, 4 Threads. Intel HD graphic',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    new_item = Item(
        name="Intel Core i3",
        description='2 Cores, 2 Threads. No HPU.',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    category=session.query(Category).filter(Category.name=='Mother Boards').first()
    new_item = Item(
        name="Mother Board 1",
        description='Mother board for intel cpus',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    new_item = Item(
        name="Mother Board 2",
        description='Mother board for amd cpus',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    category=session.query(Category).filter(Category.name=='Graphic Cards').first()
    new_item = Item(
        name="NVIDIA 1060",
        description='Medium level card. Able to run new games on mid details.',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    new_item = Item(
        name="NVIDIA 1050",
        description='Entry level level card. Able to run older games.',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    new_item = Item(
        name="NVIDIA 1030",
        description='Very basic card. Good for office PC.',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    category=session.query(Category).filter(Category.name=='HDD/SSD disks').first()
    new_item = Item(
        name="100GB SSD",
        description='Low capacity, but fast.',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    new_item = Item(
        name="600GB SSD",
        description='Huge capacity, fast, reliable.',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    new_item = Item(
        name="4999GB HDD",
        description='Huge capacity, slow, loud, cheap.',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    category=session.query(Category).filter(Category.name=='Monitors').first()
    new_item = Item(
        name="ASSUS 17 LCD",
        description='Small, low quality, cheap .',
        category_id=category.id,
        user_email='rabcanj@gmail.com'
    )
    session.add(new_item)
    new_item = Item(
        name="ASSUS 27 LCD",
        description='Big, expensive, black .',
        category_id=category.id,
        user_email='notme@gmail.com'
    )
    session.add(new_item)
    session.commit()
    return redirect(url_for('index'))
