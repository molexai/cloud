from time import sleep, time
from autonomous import Autonomous

start_time = time()  # Record the start time

while True:
    Autonomous.check()
    Autonomous.received()
    sleep(2)
