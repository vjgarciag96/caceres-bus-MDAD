from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map
from dbclient import arangodb_client
from datetime import datetime
import json

app = Flask(__name__)
GoogleMaps(app, key='AIzaSyBo6E0nwsf0ijiCQZJBsq8Rs7Ptt4Na6l4')


@app.route('/')
def map():
    return render_template('map.html', airports=get_all_airports())


@app.route('/', methods=['POST'])
def map_search_post():
    date = request.form['date']
    origin = request.form['origin']
    target = request.form['target']

    # parse date into day and month
    datetime_object = datetime.strptime(date, '%Y-%m-%d')

    client = arangodb_client()
    flightroute = client.get_best_flight(origin, target, datetime_object.day, datetime_object.month)

    if flightroute:
        flightroute = flightroute[0]
        time = flightroute['time']
        msg = 'Tiempo estimado de viaje: ' + str(time) + 'm'
        coordinates = list()
        for flight in flightroute['flight']['vertices']:
            coordinates.append({'lat': flight['lat'], 'long': flight['long']})
            # coordinates -> lista de lat, long para la línea, time -> tiempo del vuelo mételo donde sea
        for coordinate in coordinates:
            print(coordinate)

        return render_template('map.html', data = json.dumps(coordinates), airports=get_all_airports())

    else:
        msg = 'No hay combinación posible para realizar el vuelo :('

    print(msg)
    return json.dumps(msg)


def get_all_airports():
    return sorted(arangodb_client().get_all_airports(), key=lambda student: student['name'])


def create_map_from_flights_coordinates(coordinates):
    markers = list()
    for coordinate in coordinates:
        marker = {'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                  'lat': str(coordinate['lat']),
                  'lng': str(coordinate['long'])}
        markers.append(marker)

    mymap = Map(
        identifier="sndmap",
        lat=46.77411111,
        lng=-100.7467222,
        markers=markers)

    return mymap


app.run(host='0.0.0.0', port=8081, threaded=True)
