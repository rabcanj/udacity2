from flask_oauthlib.client import OAuth, OAuthException
from app import app
from flask import render_template, request, redirect, url_for, session

oauth = OAuth()

facebook = oauth.remote_app(
    'facebook',
    consumer_key='1520760008133172',
    consumer_secret='7a173e3c11891b6e8ef0bd2536acd46c',
    request_token_params={'scope': 'email', 'auth_type': 'reauthenticate'},
    # request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)

@app.route('/getin')
def getin():
    return redirect('https://165.22.94.80.xip.io/login')


@app.route('/login/')
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
