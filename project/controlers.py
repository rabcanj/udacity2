from app import app
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base
from flask import render_template, request, redirect, url_for, session
from .models import Category, Item, Base
from .fboauth import facebook, get_facebook_oauth_token
import flask_oauthlib


def get_connection(db_engine='sqlite:///catalog.sqlite'):
    engine = db.create_engine(db_engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return engine.connect(), session, engine

def checklogin():
    try:
        me = facebook.get('/me?fields=name,email')
    except flask_oauthlib.client.OAuthException:
        return render_template('nlog.html')
    return me

@app.route('/create_database')
def create_database():
    # Create database and fill it with basic data
    connection, session, engine = get_connection()
    Base.metadata.create_all(engine)
    session.add(Category(name='CPUs'))
    session.add(Category(name='Mother Boards'))
    session.add(Category(name='Graphic Cards'))
    session.add(Category(name='HDD/SSD disks'))
    session.add(Category(name='Monitors'))
    session.commit()
    return('done')


@app.route('/index')
@facebook.authorized_handler
def index(resp):
    connection, session,engine = get_connection()
    categories = session.query(Category).all()
    items = session.query(Item).\
        order_by(Item.created_date.desc()).all()
    try:
        me = facebook.get('/me?fields=name,email')
    except:
        return render_template('index.html',
            categories=categories,
            items=items,
            user={}
        )
    return render_template('index.html',
        categories=categories,
        user=me.data,
        items=items
    )


@app.route('/add_item')
@facebook.authorized_handler
def add_item_form(resp):
    connection, session,engine = get_connection()
    categories = session.query(Category).all()
    try:
        me = facebook.get('/me?fields=name,email')
        return render_template('add_item_form.html',categories=categories,user=me.data)
    except flask_oauthlib.client.OAuthException:
        return render_template('nlog.html')


@app.route('/update_item')
@facebook.authorized_handler
def update_item_form(resp):
    connection, session,engine = get_connection()
    categories = session.query(Category).all()
    try:
        me = facebook.get('/me?fields=name,email')
        data = request.args.to_dict()
        item = session.query(Item).filter(Item.user_email==me.data['email'],Item.id==data['id']).first()
        return render_template('add_item_form.html',categories=categories,user=me.data)
    except flask_oauthlib.client.OAuthException:
        return render_template('nlog.html')
    return render_template('nlog.html')


@app.route('/item', methods = ['POST'])
def post_item():
    connection, session,engine = get_connection()
    # POST creates new item
    if request.method == 'POST':
        me = checklogin()
        data = request.form.to_dict()
        category=session.query(Category).filter(Category.name==data['category_name']).first()
        new_item = Item(name=data['name'], description=data['description'],category_id=category.id,user_email=me.data['email'])
        session.add(new_item)
        session.commit()
        return redirect(url_for('index'))


@app.route('/item', methods = ['GET'])
def get_item():
    connection, session,engine = get_connection()
    if request.method == 'GET':
        # filter according to **data
        data = request.args.to_dict()
        query = session.query(Item)
        for attr,value in data.items():
            query = query.filter( getattr(Item,attr)==value )
        items = query.all()
        categories = session.query(Category).all()
        try:
            me = checklogin()
            return render_template('index.html',
                categories=categories,
                user=me.data,
                items=items
            )
        except:
            return render_template('index.html',
                categories=categories,
                user={},
                items=items
            )


@app.route('/desc', methods = ['GET'])
def get_desc():
    connection, session,engine = get_connection()
    if request.method == 'GET':
        # filter according to **data
        data = request.args.to_dict()
        query = session.query(Item)
        for attr,value in data.items():
            query = query.filter( getattr(Item,attr)==value )
        items = query.all()
        try:
            me = checklogin()
            return render_template('description.html',
                user=me.data,
                items=items
            )
        except:
            return render_template('description.html',
                user={},
                items=items
            )

@app.route('/item', methods = ['PUT'])
def put_item():
    connection, session,engine = get_connection()
    # POST creates new item
    if request.method == 'PUT':
        me = checklogin()
        data = request.form.to_dict()
        category=session.query(Category).filter(Category.name==data['category_name']).first()
        new_item = Item(name=data['name'], description=data['description'],category_id=category.id,user_email=me.data['email'])
        session.add(new_item)
        session.commit()
        return redirect(url_for('index'))
