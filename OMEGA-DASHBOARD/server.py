#from flask import *
#app = Flask(__name__)

#@app.route('/')
#def index():
#   return render_template('index.html')

#if __name__ == '__main__':
#   app.run(host='0.0.0.0',debug = True)

#!/usr/bin/python
from flask import Flask, render_template
#import Adafruit_DHT
app = Flask(__name__)
#ensor = Adafruit_DHT.DHT22
#pin = 4
#from os import time
@app.route("/")
def index():
   ##humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

   j = 45
   # Build up a dict of the current thing state.
   while True:
       print(j)
       templateData = {

            'temperature' : j,
            'humidity': j
            }

       j = j+1
       return render_template('index.html', **templateData)

       # Send the thing state as a JSON object.
       #yield('data: {0}\n\n'.format(json.dumps(thing_state)))
       # Wait a second and repeat.




if __name__ == "__main__":
   app.run(use_reloader=True)
