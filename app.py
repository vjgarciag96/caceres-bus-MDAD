from flask import Flask, render_template, request
import requests
from dbclient import arangodb_client
import json
from endpoints import GOOGLE_DIRECTION_ENDPOINT_WITH_PARAMS
from keys import GOOGLE_DIRECTION_API_KEY

app = Flask(__name__)


@app.route('/')
def map():
    return render_template('map.html', data=json.dumps([]), stops=get_all_stops())


@app.route('/', methods=['POST'])
def map_search_post():
    time = request.form['time']
    origin = request.form['origin']
    target = request.form['target']

    print(str(time))

    client = arangodb_client()
    bus_path = client.get_shortest_bus_path(origin, target, time)

    if bus_path:
        # time = bus_route['time']
        # trip_time = 'Tiempo estimado de viaje: ' + str(time) + ' min'
        coordinates = list()
        for coordinate_point in bus_path:
            coordinates.append({'lat': coordinate_point['lat'], 'lon': coordinate_point['lon']})

        # for index in range(len(bus_path) - 1):
        #     if index + 1 <= len(bus_path) - 1:
        #         coordinates = coordinates + get_real_bus_path_coordinates_between_locations(bus_path[index],
        #                                                                                     bus_path[index + 1])

        return render_template('map.html', data=json.dumps(coordinates), trip_time=0, stops=get_all_stops())

    else:
        trip_time = 'No hay combinación posible para realizar el vuelo :('

    return render_template('map.html', data=json.dumps([]), trip_time=trip_time, airports=get_all_stops())


def get_all_stops():
    return arangodb_client().get_all_stops()


# def get_real_bus_path_coordinates_between_locations(start_location, end_location):
#     path_coordinates = list()
#
#     latlng_str = '{},{}'
#     direction = requests.get(GOOGLE_DIRECTION_ENDPOINT_WITH_PARAMS.
#                              format(latlng_str.format(start_location['lat'], start_location['lon']),
#                                     latlng_str.format(end_location['lat'], end_location['lon']),
#                                     GOOGLE_DIRECTION_API_KEY))
#     directions_dict = direction.json()
#
#     path_coordinates.append({'lat': start_location['lat'], 'lon': start_location['lon']})
#
#     for step in directions_dict['routes'][0]['legs'][0]['steps']:
#         latlng = step['end_location']
#         path_coordinates.append({'lat': latlng['lat'], 'lon': latlng['lng']})
#
#     return path_coordinates


app.run(host='0.0.0.0', port=8081, threaded=True)
