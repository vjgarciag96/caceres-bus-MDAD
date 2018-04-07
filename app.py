from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)
GoogleMaps(app, key='AIzaSyBo6E0nwsf0ijiCQZJBsq8Rs7Ptt4Na6l4')


@app.route('/')
def map():
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )

    airports = [{'name': 'Malta', 'id': 'M75'}, {'name': 'Bismarck Municipal', 'id': 'BIS'}];
    return render_template('map.html', mymap=mymap, airports=airports)


@app.route('/', methods=['POST'])
def map_search_post():
    date = request.form['date']
    origin = request.form['origin']
    target = request.form['target']
    print("origen = " + str(origin))
    print("destino = " + str(target))
    print("date = " + str(date))


app.run(host='0.0.0.0', port=8081, threaded=True)
