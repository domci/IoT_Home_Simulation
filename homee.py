# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 12:23:28 2018

@author: dominik.cichon
"""









"""

Run script with:

    nohup python3 homee.py &


"""











import schedule
import urllib3
import datetime
import time
from random import randint








###########################################################################
# Define Webhooks
###########################################################################


http = urllib3.PoolManager()

webhook_url = keys=json.loads(open('keys.json').read())

### webhooks:

bathroom_on_wh = 'bathroom_on_wh'
bathroom_off_wh = 'bathroom_off_wh'

radio_on_wh = 'radio_on_wh'
radio_off_wh = 'radio_off_wh'

tv_on_wh = 'tv_on_wh'
tv_off_wh = 'tv_off_wh'

blinds_up_wh = 'blinds_up_wh'
blinds_down_wh = 'blinds_down_wh'

lights_off = 'lights_off'

bedroom_on_wh = 'bedroom_on_wh'
bedroom_off_wh = 'bedroom_off_wh'

home_simulation_started = 'home_simulation_started'
home_simulation_ended = 'home_simulation_ended'







def home_simulation():
    http.request('GET', webhook_url + home_simulation_started)
    while True:
        now = datetime.datetime.now().replace(second = 0, microsecond=0)
        # MORNINGS:
        if now.time() == datetime.time(7, randint(11, 50)):
            # Rollos hoch
            http.request('GET', webhook_url + blinds_up_wh)
            # ca. 2,5 Min Warten
            time.sleep(randint(150, 300))
            # Badezimmerlicht an
            http.request('GET', webhook_url + bathroom_on_wh)
            # Radio an
            http.request('GET', webhook_url + radio_on_wh)
            # ca. eine Stunde Warten
            time.sleep(randint(2500, 3600))
            # Badezimmerlicht aus
            http.request('GET', webhook_url + bathroom_on_wh)
            # ca. 2,5 Min Warten
            time.sleep(randint(150, 300))
            # Radio aus
            http.request('GET', webhook_url + radio_off_wh)
            # ca. 2,5 Min Warten
            time.sleep(randint(150, 300))

            
        if now.time() == datetime.time(9, randint(11, 50)):
            # Radio an
            http.request('GET', webhook_url + radio_on_wh)
            # ca. 3 eine Stunde Warten
            time.sleep(randint(10000, 12000))
            # Radio aus
            http.request('GET', webhook_url + radio_off_wh)
            # ca. 2,5 Min Warten
            time.sleep(randint(150, 300))

            
        if now.time() == datetime.time(19, randint(40, 59)):
            # Fernseher an
            http.request('GET', webhook_url + tv_on_wh)
            # ca. eine Stunde Warten
            time.sleep(randint(11000, 12000))
            # Fernseher aus
            http.request('GET', webhook_url + tv_off_wh)
            # ein paar Sekunden Warten
            time.sleep(randint(10, 30))
            # Bad Licht an
            http.request('GET', webhook_url + bathroom_on_wh)
            # ca 10 Min warten
            time.sleep(randint(500, 900))
            # Bad Licht aus
            http.request('GET', webhook_url + bathroom_off_wh)
            # ein paar Sekunden Warten
            time.sleep(3)
            # Schlafzimmer Licht aus
            http.request('GET', webhook_url + bedroom_on_wh)
            # ca 10 Min warten
            time.sleep(randint(500, 900))
            # Schlafzimmer Licht aus
            http.request('GET', webhook_url + bedroom_off_wh)
            time.sleep(3600)
            http.request('GET', webhook_url + home_simulation_ended)
            return




schedule.every().day.at("14:32").do(home_simulation)


try:
    while True:
        schedule.run_pending()
        time.sleep(5) # wait a bit
except KeyboardInterrupt:
    http.request('GET', webhook_url + home_simulation_ended)
    print('Keyboard Interrupt!')
    
    
    