
import urllib2
import cookielib
from getpass import getpass
import sys
import os
from stat import *

def messs():
#message = raw_input("Enter text: ")
#number = raw_input("Enter number: ")
   message = "FIRE ALERT! Please escape from the area immediately. Use STAY-SHIELD to escape. Follow the red lights to the nearest escape"
   number = "7736259094"


   if __name__ == "__main__":    
       username = "8606197203"
       passwd = "hello"

       message = "+".join(message.split(' '))

 #logging into the sms site
       url ='http://site24.way2sms.com/Login1.action?'
       data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

 #For cookies

       cj= cookielib.CookieJar()
       opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

 #Adding header details
       opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
       usock =opener.open(url, data)
       jession_id =str(cj).split('~')[1].split(' ')[0]
       send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
       send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
       opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
       sms_sent_page = opener.open(send_sms_url,send_sms_data)

messs()
