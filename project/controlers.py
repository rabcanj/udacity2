from app import app
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base
from flask import render_template, request, redirect, url_for, session
from .models import Category, Item, Base
from flask_oauthlib.client import OAuth, OAuthException

oauth = OAuth()

facebook = oauth.remote_app(
    'facebook',
    consumer_key='960930254299463',
    consumer_secret='5779e0bd681e37816ed0a8420a517fd6',
    request_token_params={'scope': 'email', "auth_type": "reauthenticate"},
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)



@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/logout')
def logout():
    session['oauth_token'] = None
    return redirect(url_for('index'))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied'

    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me?fields=name,email')
    # session['me'] = (me.data)
    print(me.data)
    return redirect(url_for('index'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

def get_connection(db_engine='sqlite:///catalog.sqlite'):
    engine = db.create_engine(db_engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return engine.connect(), session, engine


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
    recent_items = session.query(Item).\
        order_by(Item.created_date)
    try:
        me = facebook.get('/me?fields=name,email')
    except:
        return render_template('index.html',
            categories=categories,
            recent_items=recent_items,
            user={}
        )
    return render_template('index.html',
        categories=categories,
        user=me.data,
        recent_items=recent_items
    )


@app.route('/category', methods = ['GET', 'POST', 'DELETE'])
def crud_category():
    connection, session,engine = get_connection()
    if request.method == 'POST':
        new_category = Category(**request.json)
        session.add(new_category)
        session.commit()
        return "i"
