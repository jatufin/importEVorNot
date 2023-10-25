from flask import Flask, send_from_directory
from flask_cors import CORS

# TODO: In production CORS should be restricted to the frontend server
app = Flask(__name__, static_folder='./frontend/build', static_url_path='/')
CORS(app)

import routes

if __name__ == '__main__':
    app.run()