from flask import Flask
from flask import render_template
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
    return render_template('map.html', mymap=mymap)


app.run(host='0.0.0.0', port=8081, threaded=True)
