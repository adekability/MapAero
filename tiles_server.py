from flask import Flask, send_from_directory, abort, make_response
import os
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# Define the base directory where your tiles are stored
TILE_DIR = 'tiles/'


@app.route('/tiles/<int:z>/<int:x>/<int:y>.png')
@cross_origin()
def get_tile(z, x, y):
    tile_path = os.path.join(TILE_DIR, str(z), str(x), f'{y}.png')

    if os.path.isfile(tile_path):
        response = make_response(send_from_directory(os.path.join(TILE_DIR, str(z), str(x)), f'{y}.png'))
        response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    else:
        return "Tile not found", 404


@app.errorhandler(404)
def page_not_found(e):
    return "Tile not found", 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
