#!/usr/bin/env python

#This is different from AIY Kit's actions
#Copying and Pasting AIY Kit's actions commands will not work


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from gmusicapi import Mobileclient
from googletrans import Translator
from pushbullet import Pushbullet
from gtts import gTTS
import requests
import os
import os.path
import RPi.GPIO as GPIO
import time
import re
import subprocess
import aftership
import feedparser
import json
import urllib.request
import pafy


#YouTube API Constants
DEVELOPER_KEY = 'AIzaSyA5d8foEYGXF2C9jlPYhbXHg-6gFQzdBXk'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Number of entities in 'var' and 'PINS' should be the same
var = ('bedroom lights', 'bedroom fan', 'bedroom device')#Add whatever names you want. This is case is insensitive
gpio = (12,13,21)#GPIOS for 'var'. Add other GPIOs that you want

#Number of station names and station links should be the same
stnname=('Radio 1', 'Radio 2', 'Radio 3', 'Radio 5')#Add more stations if you want
stnlink=('http://www.radiofeeds.co.uk/bbcradio2.pls', 'http://www.radiofeeds.co.uk/bbc6music.pls', 'http://c5icy.prod.playlists.ihrhls.com/1469_icy', 'http://playerservices.streamtheworld.com/api/livestream-redirect/ARNCITY.mp3')

#IP Address of ESP
ip='192.168.43.62'

#Declaration of ESP names
devname=('Device one', 'Device to', 'Device three')
devid=('/Device1', '/Device2', '/Device3')

for pin in gpio:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

#Servo pin declaration
GPIO.setup(27, GPIO.OUT)
pwm=GPIO.PWM(27, 50)
pwm.start(0)

#Stopbutton
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#Led Indicatorx
GPIO.setup(25, GPIO.OUT)
led=GPIO.PWM(25,1)
led.start(0)

playshell = None




#RSS feed URLS
worldnews = "http://feeds.bbci.co.uk/news/world/rss.xml"
technews = "http://feeds.bbci.co.uk/news/technology/rss.xml"
topnews = "http://feeds.bbci.co.uk/news/rss.xml"
sportsnews = "http://feeds.feedburner.com/ndtvsports-latest"
quote = "http://feeds.feedburner.com/brainyquote/QUOTEBR"

##Speech and translator declarations
ttsfilename="/tmp/say.mp3"
translator = Translator()
language='en'

#Function to manage mpv start volume
def mpvvolmgr():
    if os.path.isfile("/home/pi/.mediavolume.json"):
        with open('/home/pi/.mediavolume.json', 'r') as vol:
            oldvollevel = json.load(vol)
        print(oldvollevel)
        startvol=oldvollevel
    else:
        startvol=50
    return startvol



#Text to speech converter with translation
def say(words):
    #words= translator.translate(words, dest=language)
    #words=words.text
    #words=words.replace("Text, ",'',1)
    words=words.strip()
    print(words)
    tts = gTTS(text=words, lang='en-us')
    tts.save(ttsfilename)
    os.system("mpg123 "+ttsfilename)
    os.remove(ttsfilename)


#Radio Station Streaming
def radio(phrase):
    for num, name in enumerate(stnname):
        if name.lower() in phrase:
            startingvol=mpvvolmgr()
            station=stnlink[num]
            print (station)
            say("Tuning into " + name)
            os.system('mpv --really-quiet --volume='+str(startingvol)+' '+station+' &')

#ESP6266 Devcies control
def ESP(phrase):
    for num, name in enumerate(devname):
        if name.lower() in phrase:
            dev=devid[num]
            if (' on' in phrase) and ('off' not in phrase):
                ctrl='=ON'
                say("Turning On " + name)
            elif 'off' in phrase:
                ctrl='=OFF'
                say("Turning Off " + name)
            ss = 'http://'+ip+dev+ctrl
            os.system('wget '+ss)
            dev=dev.strip('/')
            print(dev)
            fil = dev+ctrl
            os.remove(fil)

def stop():
    pkill = subprocess.Popen(["/usr/bin/pkill","mpv"],stdin=subprocess.PIPE)

#RSS Feed Reader
def feed(phrase):
    if 'world news' in phrase:
        URL=worldnews
    elif 'top news' in phrase:
        URL=topnews
    elif 'sports news' in phrase:
        URL=sportsnews
    elif 'tech news' in phrase:
        URL=technews
    elif 'my feed' in phrase:
        URL=quote
    numfeeds=10
    feed=feedparser.parse(URL)
    feedlength=len(feed['entries'])
    print(feedlength)
    if feedlength<numfeeds:
        numfeeds=feedlength
    title=feed['feed']['title']
    say(title)
    #To stop the feed, press and hold stop button
    while GPIO.input(23):
        for x in range(0,numfeeds):
            content=feed['entries'][x]['title']
            print(content)
            say(content)
            summary=feed['entries'][x]['summary']
            print(summary)
            say(summary)
            if not GPIO.input(23):
              break
        if x == numfeeds-1:
            break
        else:
            continue



#GPIO Device Control
def Action(phrase):
    if 'shut down' in phrase:
        say('Shutting down Raspberry Pi')
        time.sleep(10)
        os.system("sudo shutdown -h now")
        #subprocess.call(["shutdown -h now"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if 'servo' in phrase:
        for s in re.findall(r'\b\d+\b', phrase):
            SetAngle(int(s))
    if 'zero' in phrase:
        SetAngle(0)
    else:
        for num, name in enumerate(var):
            if name.lower() in phrase:
                pinout=gpio[num]
                if 'on' in phrase:
                    GPIO.output(pinout, 1)
                    say("Turning On " + name)
                elif 'off' in phrase:
                    GPIO.output(pinout, 0)
                    say("Turning Off " + name)


stat = 0
def conauto(person):
    global stat
    if (person >= 1) and (stat==0):
         GPIO.output(12, 1)
         GPIO.output(13, 1)
         say("Turning On Classroom Lights and Fan")
         stat = 1
    elif (person == 0) and (stat==1):
         GPIO.output(12, 0)
         GPIO.output(13, 0)
         #say("Turning Off Classroom Lights and Fan")
         stat = 0

def fisat(phrase):
    if 'about' in phrase:
       say('Federal Institute of Science And Technology is a private self financing Engineering College, established and run by the Federal Bank Officers Association Educational Society. It is one of the top private Engineering Colleges in Kerala. It is located at Mookannoor, near Angamaly in Ernakulam District Kerala. I was made by the project omega group of the Electronics and Communication engineering department.')
