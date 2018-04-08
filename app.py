from flask import Flask, render_template, request
from dbclient import arangodb_client
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def map():
    return render_template('map.html', data=json.dumps([]), airports=get_all_airports())

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
        flight_time = 'Tiempo estimado de viaje: ' + str(time) + 'm'
        coordinates = list()
        for flight in flightroute['flight']['vertices']:
            coordinates.append({'lat': flight['lat'], 'long': flight['long']})
        for coordinate in coordinates:
            print(coordinate)

        return render_template('map.html', data = json.dumps(coordinates), flight_time=flight_time, airports=get_all_airports())

    else:
        flight_time = 'No hay combinación posible para realizar el vuelo :('

    return render_template('map.html', flight_time=flight_time,
                           airports=get_all_airports())


def get_all_airports():
    return sorted(arangodb_client().get_all_airports(), key=lambda student: student['name'])

app.run(host='0.0.0.0', port=8081, threaded=True)
