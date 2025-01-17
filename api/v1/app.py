#!/usr/bin/python3
'''
Start the airbnb ap
'''

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False  # strict_slashes=False globally
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(error):
    '''
    Teardown
    '''
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    error = {
        "error": "Not found"
    }
    return jsonify(error), 404


if __name__ == '__main__':
    app.run(getenv('HBNB_API_HOST'), getenv('HBNB_API_PORT'), threaded=True)
