from flask_oauthlib.client import OAuth, OAuthException
from app import app
from flask import render_template, request, redirect, url_for, session

oauth = OAuth()

facebook = oauth.remote_app(
    'facebook',
    consumer_key='960930254299463',
    consumer_secret='5779e0bd681e37816ed0a8420a517fd6',
    # request_token_params={'scope': 'email', "auth_type": "reauthenticate"},
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for(
        'facebook_authorized', next=request.args.get('next')
        or request.referrer or None, _external=True))


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
