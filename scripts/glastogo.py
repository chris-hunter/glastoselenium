#!/usr/bin/env python3

import os
import glasto as gl

# test on reference HTML obtained from todays resale
URL = "file:///{}/ref/Buy%20tickets%20for%20Glastonbury%202019%20-%20Glastonbury.html".format(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
PHRASES_TO_CHECK = [gl.Twenty20.REGISTRATION_PHRASE]

# first is lead booker
REG_DETAILS=[
    {
        'number': "123", 
        'postcode': "SW1 1AA"
    },
    {
        'number': "45", 
        'postcode': "SW1 1AB"
    },
    {
        'number': "67", 
        'postcode': "BA16 1AB"
    },
    {
        'number': "89", 
        'postcode': "BA12 2GB"
    }
]

if len(REG_DETAILS) == 0:
    raise RuntimeError(
        "Must have at least one registration!")

if len(REG_DETAILS) > 4:
    raise RuntimeError(
        "Cannot accept more than 1 + 3 registration details!")

try:
    from glasto._custom.driver import DRIVER_PATH
except:
    import os
    DRIVER_PATH = os.getenv("CHROMEDRIVER", '')
    if not DRIVER_PATH:
        raise RuntimeError(
            "Requires chromedriver - set the path via env variable CHROMEDRIVER")

def attemptconnection(client):
    if client.establishconnection(URL, phrases_to_check=PHRASES_TO_CHECK):
        print("success")
        print(client.attempts)
        print(client.content)
        gl.tofile(client.content, "reg_page_2020.html")
        if client.submit_registration(REG_DETAILS):
            print("Registration details submission success!")

            gl.tofile(client.pagesource, "payment_page_2020.html")
            # we cannot go beyond this automated, 
            # since entering credit cards details automatically
            # is terribly risky.
            # instead leave the page open for us to do that
            # and save the content

            # todo: ????
            return
        else:
            print("Registration details submission failed!")

    # try again
    attemptconnection(client)

# main
s = gl.Service(DRIVER_PATH)
c = gl.Twenty20(s, timeout=2, refreshrate=0.01)
attemptconnection(c)