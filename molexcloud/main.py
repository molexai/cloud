from time import sleep, time
from ai.autonomous import Autonomous

start_time = time()  # Record the start time

while True:
    Autonomous.check()
    Autonomous.received()
    sleep(0.5)
