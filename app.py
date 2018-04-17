from flask import Flask, render_template, request
from dbclient import arangodb_client
import json

app = Flask(__name__)


@app.route('/')
def map():
    return render_template('map.html', data=json.dumps([]), stops=get_all_stops())


@app.route('/', methods=['POST'])
def map_search_post():
    origin = request.form['origin']
    target = request.form['target']

    client = arangodb_client()
    bus_path = client.get_shortest_bus_path(origin, target)

    if bus_path:
        coordinates = list()
        for coordinate_point in bus_path:
            print(coordinate_point)
            coordinates.append({'lat': coordinate_point['stop']['lat'], 'lon': coordinate_point['stop']['lon'], 'bus_line':coordinate_point['bus_line']})

        return render_template('map.html', data=json.dumps(coordinates), trip_time=0, stops=get_all_stops())

    return render_template('map.html', data=json.dumps([]), airports=get_all_stops())


def get_all_stops():
    return arangodb_client().get_all_stops()


app.run(host='0.0.0.0', port=8081, threaded=True)
