from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def map():
    return render_template('map.html')


app.run(host='0.0.0.0', port=8081, threaded=True)
