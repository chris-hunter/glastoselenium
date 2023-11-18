#!/usr/bin/env python3

import sys
from datetime import datetime
import time
import glasto as gl
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

if sys.argv[1]:
    run_time = datetime.strptime(sys.argv[1], '%Y-%m-%d %H:%M:%S')

else:
    print("Please enter start time.")

URL = "https://glastonbury.seetickets.com/event/glastonbury-2020-ticket-deposits/worthy-farm/1450012"
URL = "https://glastonbury.seetickets.com"
s = gl.Service(gl.DRIVER_PATH)
c = gl.ScoutClient(s, linkphrase="glastonbury", verbose=False, 
    disablejs=False, incognito=True, disableimages=True, 
    headless=True)

def get_links():
    if c.establishconnection(URL):
        for link in c.getalllinks():
            print(link)
            with open('links.txt', 'a') as links_file:
                print(link, file=links_file)

        c.search(nlevels=2)

scheduler = BackgroundScheduler()
trigger = DateTrigger(run_time)
scheduler.add_job(get_links, trigger, id='get_links_job')
scheduler.start()


try:
    # This is here to simulate application activity (which keeps the main thread alive).
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()