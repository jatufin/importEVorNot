from flask import Flask
from flask_cors import CORS

# TODO: In production CORS should be restricted to the frontend server
app = Flask(__name__)
CORS(app)

import routes

