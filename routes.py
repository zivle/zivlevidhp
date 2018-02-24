from flask import Flask
from flask import request
from flask import render_template
import GeoLocationExtractor

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/geolocations', methods=['POST'])
def myfunc():
    text = request.get_data().decode('utf-8')
    locations = GeoLocationExtractor.tag_locations_from_text(text)
    # geolocations = GeoLocationExtractor.build_geo_locations_from_list(locations)
    return locations


if __name__ == '__main__':
    app.run()
