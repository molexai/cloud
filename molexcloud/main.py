import sys
import os
from time import sleep, time

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from molexcloud.ai.autonomous import Autonomous

start_time = time()  # Record the start time

while True:
    # Check for AI requests
    Autonomous.check()
    if time() - start_time >= 60:  # Check for received responses every minute
        os.system("cls")  # Clear the console
        print("molexAI Cloud: Checking for received responses...\n")
        Autonomous.received()  # Check for received responses every minute
        start_time = time()
    sleep(0.5)