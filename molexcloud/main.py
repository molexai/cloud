import os
from time import sleep, time
from molexcloud.ai.autonomous import Autonomous

start_time = time()  # Record the start time

while True:
    # Check for AI requests
    Autonomous.check()
    if time() - start_time >= 2:
        print("molexAI Cloud: Checking for received responses...\n")
        Autonomous.received()  # Check for received responses every minute
        os.system("cls")  # Clear the console
        start_time = time()
    sleep(0.5)