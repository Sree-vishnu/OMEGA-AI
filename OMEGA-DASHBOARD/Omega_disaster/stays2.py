

import time
import paho.mqtt.client as mqtt
import os
import threading
import random

import db




def on_connect(client, userdata, flags, rc):
   client.subscribe("room_one")
def on_message(client, userdata, msg):

   if msg.topic == "room_one":
       t = msg.payload
       print(t)
       gg1=t+':1'
       db.write(gg1)
       u = t.split(':')
       tem = int(u[0])
       hum = int(u[1])
       co1 = int(u[2])
       vib1 = int(u[3])
       print ('Room one',t)
       if ((tem>39) or (co1>700)):
          client.publish('leds', 'ON')
          os.system('python fireR.py')
          os.system('python fireP.py')
       if ((vib1>700)):
          client.publish('leds', 'ON')
          os.system('python earthR.py')
          os.system('python earthP.py')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)

client.loop_start()






class Function(object):

   def __init__(self):
        self._humidity = None
        self._temperature = None
        self._co = None
        self._vib = None
        self._dht_thread = threading.Thread(target=self._update_dht)
        self._dht_thread.daemon = True
        self._dht_thread.start()

   def _update_dht(self):
        while True:

           rea = db.read()
           u = rea.split(':')
           roo = u[4].rstrip('.\n')
           room = int(roo)
           if (room==1):
              tem = int(u[0])
              hum = int(u[1])
              co1 = int(u[2])
              v1 = u[3]
              vib=int(v1)
              self._humidity = tem
              self._temperature = hum
              self._co = co1
              self._vib = vib

   def get_h(self):
        return self._humidity
   def get_t(self):
        return self._temperature
   def get_co(self):
                return self._co
   def get_vib(self):
                return self._vib

print('STAY-SHEILD Started')
