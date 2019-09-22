from app import app
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, joinedload, exc
from sqlalchemy.ext.declarative import declarative_base
from flask import render_template, request, redirect, url_for, session
from .models import Category, Item, Base
from .fboauth import facebook, get_facebook_oauth_token
import flask_oauthlib


def get_connection(db_engine='postgresql://catalog:ovviodwa@localhost/catalog'):
    """
        creates connection to the database
        SQLLITE: sqlite:///catalog.sqlite
    """
    #db_engine = 'sqlite:///catalog.sqlite'
    engine = db.create_engine(db_engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return engine.connect(), session, engine


def checklogin():
    """
        check if user is logged
    """
    try:
        me = facebook.get('/me?fields=name,email')
    except flask_oauthlib.client.OAuthException:
        return render_template('nlog.html')
    return me


@app.route('/auth_error')
def raise_auth_error():
    """
        Raise auth error logged/unloged want to see for him forbiden content,
        If user is logged in then renders the template with his name,
        otherwise render template without user details
    """
    me = checklogin()
    try:
        return render_template('nlog.html', user=me.data)
    except AttributeError:
        return render_template('nlog.html')


@app.route('/index')
@facebook.authorized_handler
def index(resp):
    """
        render template for page index
    """
    connection, session, engine = get_connection()
    categories = session.query(Category).all()
    items = session.query(Item).\
        order_by(Item.created_date.desc()).all()
    try:
        me = facebook.get('/me?fields=name,email')
    except flask_oauthlib.client.OAuthException:
        return render_template(
            'index.html',
            categories=categories,
            items=items,
            user={},
            latest='Latest'
        )

    return render_template(
         'index.html',
         categories=categories,
         user=me.data,
         items=items,
         latest='Latest'
    )


@app.route('/add_item')
@facebook.authorized_handler
def add_item_form(resp):
    """
        redirect to form, where we create new items
    """
    connection, session, engine = get_connection()
    categories = session.query(Category).all()
    try:
        me = facebook.get('/me?fields=name,email')
        return render_template(
            'add_item_form.html',
            categories=categories,
            user=me.data
        )
    except flask_oauthlib.client.OAuthException:
        return render_template('nlog.html')


@app.route('/update_item_form')
@facebook.authorized_handler
def update_item_form(resp):
    """
        redirect to form, where we update items
    """
    connection, session, engine = get_connection()
    categories = session.query(Category).all()
    try:
        me = facebook.get('/me?fields=name,email')
        data = request.args.to_dict()
        # we do not allow to update items that does not belong to logged user
        item = session.query(Item).filter(
            Item.user_email == me.data['email'],
            Item.id == data['id']).first()
        if item:
            return render_template(
                'update_item_form.html',
                categories=categories,
                item=item,
                user=me.data
            )
    except flask_oauthlib.client.OAuthException:
        return render_template('nlog.html')
    return render_template('nlog.html', user=me.data)


@app.route('/update_item', methods=['POST'])
def update_item():
    """
        method for updating items
        form validation done by html
    """
    connection, session, engine = get_connection()
    if request.method == 'POST':
        me = checklogin()
        data = request.form.to_dict()
        category = session.query(Category).filter(
            Category.name == data['category_name']).first()
        item = session.query(Item).filter(Item.id == data['id']).first()
        item.description = data['description']
        item.name = data['name']
        item.category_id = category.id
        # session.add(new_item)
        session.commit()
        return redirect(url_for('index'))


@app.route('/delete_item/<id>')
def delete_item(id):
    """
        method for deleting items
    """
    me = checklogin()
    connection, session, engine = get_connection()
    try:
        item = session.query(Item).filter(
            Item.id == id,
            me.data['email'] == Item.user_email).first()
        session.delete(item)
        session.commit()
        return redirect(url_for('index'))
    except (exc.UnmappedInstanceError, AttributeError):
        return redirect(url_for('raise_auth_error'))


@app.route('/item', methods=['POST'])
def post_item():
    """
        method for creating new items
        form validation done by html
    """
    connection, session, engine = get_connection()
    # POST creates new item
    if request.method == 'POST':
        me = checklogin()
        data = request.form.to_dict()
        category = session.query(Category).filter(
            Category.name == data['category_name']).first()
        new_item = Item(
            name=data['name'],
            description=data['description'],
            category_id=category.id,
            user_email=me.data['email']
        )
        session.add(new_item)
        session.commit()
        return redirect(url_for('index'))


@app.route('/item', methods=['GET'])
def get_item():
    """
    render specic items and render to index.html
    """
    connection, session, engine = get_connection()
    if request.method == 'GET':
        # filter according to **data
        data = request.args.to_dict()
        query = session.query(Item)
        for attr, value in data.items():
            query = query.filter(getattr(Item, attr) == value)
        items = query.all()
        categories = session.query(Category).all()
        try:
            me = checklogin()
            return render_template(
                'index.html',
                categories=categories,
                user=me.data,
                items=items
            )
        except AttributeError:
            return render_template(
                'index.html',
                categories=categories,
                user={},
                items=items
            )


@app.route('/desc', methods=['GET'])
def get_desc():
    """
    render description template
    """
    connection, session, engine = get_connection()
    if request.method == 'GET':
        # filter according to **data
        data = request.args.to_dict()
        query = session.query(Item)
        for attr, value in data.items():
            query = query.filter(getattr(Item, attr) == value)
        items = query.all()
        try:
            me = checklogin()
            return render_template(
                'description.html',
                user=me.data,
                items=items
            )
        except AttributeError:
            return render_template(
                'description.html',
                user={},
                items=items
            )


@app.route('/json_data', methods=['GET'])
def json_data(category_id=None, item_id=None):
    """
    endpoint returns data in json for an arbitary item
    examples:
    For the whole database:
        https://localhost:8000/json_data
    For items:
        https://localhost:8000/json_data?item_id=2
    For categories:
        https://localhost:8000/json_data?category_id=2
    Combination of both
        https://localhost:8000/json_data?category_id=2&item_id=5
    """
    data = request.args.to_dict()
    category_id = data.get('category_id')
    item_id = data.get('item_id')
    res = []
    connection, session, engine = get_connection()
    if category_id:
        categories = session.query(Category).filter(
            Category.id == category_id
        ).all()
    else:
        categories = session.query(Category).all()
    for category in categories:
        category_dict = category.get_dict()
        category_dict['items'] = []
        if item_id:
            items = session.query(Item).filter(
                category.id == Item.category_id, Item.id == item_id).all()
        else:
            items = session.query(Item).filter(
                category.id == Item.category_id).all()
        for item in items:
            category_dict['items'].append(item.get_dict())
        if len(category_dict['items']) > 0 or\
                category_id or (not category_id and not item_id):
            res.append(category_dict)
    return({
        'json': res
        })
