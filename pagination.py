"""Pagination sample for Microsoft Graph."""
# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
# See LICENSE in the project root for license information.
import os

import bottle
import graphrest

import config


MSGRAPH = graphrest.GraphSession(client_id=config.CLIENT_ID,
                                 client_secret=config.CLIENT_SECRET,
                                 redirect_uri=config.REDIRECT_URI,
                                 scopes=['User.Read', 'Mail.Read'])

bottle.TEMPLATE_PATH = ['./static/templates']


@bottle.route('/')
@bottle.view('homepage.html')
def homepage():
    """Render the home page."""
    return {'title': 'Pagination Basics'}


@bottle.route('/login')
def login():
    """Prompt user to authenticate."""
    endpoint = MSGRAPH.api_endpoint('me/messages')
    MSGRAPH.login(login_redirect=f'/pagination?endpoint={endpoint}')


@bottle.route('/login/authorized')
def authorized():
    """Handler for the application's Redirect URI."""
    MSGRAPH.redirect_uri_handler()


@bottle.route('/pagination')
@bottle.view('pagination.html')
def pagination():
    """Example of paginated response from Microsoft Graph."""
    endpoint = bottle.request.query.endpoint
    graphdata = MSGRAPH.get(endpoint).json()
    return {'graphdata': graphdata}


@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    """Handler for static files, used with the development server."""
    root_folder = os.path.abspath(os.path.dirname(__file__))
    return bottle.static_file(filepath, root=os.path.join(root_folder, 'static'))


if __name__ == '__main__':
    bottle.run(app=bottle.app(), server='wsgiref', host='localhost', port=5000)
