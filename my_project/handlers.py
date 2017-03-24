"""Application Handlers.

Requests are redirected to handlers, which are responsible for getting
information from the URL and passing it down to the logic layer. The way
each layer talks to each other is through Response objects which defines the
type status of the data and the data itself.

Please note: the Orchard uses the term handlers over views as convention
for clarity

See:
    oto.response for more details.
"""


from flask import g
from flask import jsonify
from flask import request

from oto import response
from oto.adaptors.flask import flaskify

from my_project import config
from my_project.api import app
from my_project.logic import hello


@app.route('/', methods=['GET'])
def hello_world():
    """Hello World with an optional GET param "name"."""
    # name = request.args.get('name', '')
    # return flaskify(hello.say_hello(name))
    return flaskify(hello.say_hello())


@app.route('/all')
def fetch_all_product():
    """Hello World on /<username>.

    Args:
        username (str): the user's username.
    """
    return flaskify(hello.fetch_all_product())


@app.route('/<id>', methods=['GET'])
def fetch_product_by_id(id):
    """Hello World on /<username>.

    Args:
        username (str): the user's username.
    """
    return flaskify(hello.fetch_product_by_id(id))


@app.route('/add/<name>', methods=['GET'])
def add_product(name):
    """Hello World on /<username>.

    Args:
        username (str): the user's username.
    """
    data = name
    return flaskify(hello.add_product(data))


@app.route('/update/<id>/<name>', methods=['GET'])
def update_product(id,name):
    """Hello World on /<username>.

    Args:
        username (str): the user's username.
    """
    data = {'release_id':id,'release_name':name}
    return flaskify(hello.update_product(data))


@app.route('/delete/<id>', methods=['GET'])
def delete_product(id):
    """Hello World on /<username>.

    Args:
        username (str): the user's username.
    """
    data = id
    return flaskify(hello.delete_product(data))


@app.route(config.HEALTH_CHECK, methods=['GET'])
def health():
    """Check the health of the application."""
    return jsonify({'status': 'ok'})


@app.errorhandler(500)
def exception_handler(error):
    """Default handler when uncaught exception is raised.

    Note: Exception will also be sent to Sentry if config.SENTRY is set.

    Returns:
        flask.Response: A 500 response with JSON 'code' & 'message' payload.
    """
    message = (
        'The server encountered an internal error '
        'and was unable to complete your request.')
    g.log.exception(error)
    return flaskify(response.create_fatal_response(message))
