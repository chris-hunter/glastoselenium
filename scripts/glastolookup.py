#!/usr/bin/env python3

import sys
import glasto as gl
from selenium.webdriver.common.by import By

URL = "https://glastonbury.seetickets.com/registration/lookup"
PHRASES_TO_CHECK = []

s = gl.Service(gl.DRIVER_PATH)
c = gl.Twenty19(s, timeout=2, refreshrate=0.01)

if c.establishconnection(URL, phrases_to_check=PHRASES_TO_CHECK):
    print("success")
    print(c.attempts)

inputs = c.client.find_elements(By.TAG_NAME, 'input')
# loop to find email input
found = False
for i in inputs:
    if 'email' in i.get_attribute('name').lower():
        i.send_keys("jon@smith.com")
        found = True

if not found:
    print("No such input.")
    c.close()
    sys.exit(1)

# loop again to find submit
for i in inputs:
    if 'submit' in i.get_attribute('type').lower():
        print("submitting...")
        i.send_keys(gl.Keys.ENTER)

# c.close()