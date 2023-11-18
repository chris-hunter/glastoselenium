#!/usr/bin/env python3

import os
import time
import glasto as gl
from datetime import datetime

# incognito??
incognito = True

# disable js??
disablejs = False

# disable images for faster loading?
disableimages=True

# change cache size?
cache=4096

# try a proxy with "8.8.8.8:88"
proxy=None

# run without browser - kind of pointless but faster.
headless=False

# refresh rate - seconds
refreshrate = 0.0001

# set user-data directory
user_data_dir = "c:\\important\\chris\\coding\\python\\glastoselenium\\user_data\\1"

# try one of these URLS
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2024-deposits/worthy-farm/3500000"
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2024/worthy-farm/3500001"
DEPOSIT_20_URL = "https://glastonbury.seetickets.com/"

#PHRASES_TO_CHECK = [gl.Twenty20.REGISTRATION_PHRASE]
PHRASES_TO_CHECK = ['Enter registration details']

HOLDING_PHRASE = 'held at this page'
TRIGGER_TIME = datetime(2023, 11, 19, 9, 0)
# first is lead booker
REG_DETAILS=[
    {
        'number': "123456789", 
        'postcode': "SW1 1SQ"
    },
    {
        'number': "123456780", 
        'postcode': "SW1 1SQ"
    },
]

if len(REG_DETAILS) == 0:
    raise RuntimeError(
        "Must have at least one registration!")

if len(REG_DETAILS) > 6:
    raise RuntimeError(
        "Cannot accept more than 1 + 5 registration details!")

def attemptconnection(client, url):
    if client.establishconnection(url, phrases_to_check=PHRASES_TO_CHECK, holding_phrase=HOLDING_PHRASE, trigger_time=TRIGGER_TIME):
        print("success")
        print(client.attempts)
        try:
            gl.tofile(client.content, "reg_page_2020.html")
        except:
            pass
        if client.submit_registration(REG_DETAILS):
            print("Registration details submission success!")
            # save the html data
            try:
                gl.tofile(client.content, "reg_check_2020.html")
            except:
                pass

            try:
                # then click 'confirm' button and save html data again
                client.clickbutton('Confirm')
                gl.tofile(client.pagesource, "payment_page_2020.html")
            except:
                pass

            # we cannot go beyond this automated, 
            # since entering credit cards details automatically
            # is terribly risky.
            # instead leave the page open for us to do that
            # and save the content

            # todo: ????
            return
        else:
            print("Registration details submission failed!")

    # try again??
    # attemptconnection(client, url)

# main
s = gl.Service(gl.DRIVER_PATH)
c = gl.Twenty20(s, timeout=4, refreshrate=refreshrate, verbose=False, 
    disablejs=disablejs, incognito=incognito, disableimages=disableimages, 
    cache=cache, headless=headless, proxy=proxy, user_data_dir=user_data_dir)
attemptconnection(c, DEPOSIT_20_URL)

# backup sleep 
time.sleep(1000000) # Hack - leave it open to fill in details