from flask import *
import time
import stays2
import random
import json
import os

app = Flask(__name__)
fun =stays2.Function()

@app.route('/')
def first():
	return render_template('index.html')

@app.route('/thing')
def thing():
    def get_thing_values():
       while True:
           thing_state = {
             'temperature': fun.get_t(),
             'humidity': fun.get_h(),
             'co':fun.get_co(),
             'vib':fun.get_vib()
            }
	    #print thing_state
            # Send the thing state as a JSON object.
           yield('data: {0}\n\n'.format(json.dumps(thing_state)))
            # Wait a second and repeat.
           time.sleep(1.0)
    return Response(get_thing_values(), mimetype='text/event-stream')

@app.route("/sos/<int:state>", methods=['POST'])
def sos(state):
	if state == 1:
                os.system('python sos_room1.py')

                print("SOS")
                return("sos")
	elif (state == 2):
                os.system('python sos_room2.py')

	else:
		return ('Unknown State', 400)
	return('',204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
