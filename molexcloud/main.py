from time import sleep, time
from autonomous import Autonomous

start_time = time()  # Record the start time

while time() - start_time < 18000:  # Run for 10 seconds
    # Check for AI requests
    #Autonomous.check()
    #Autonomous.received()
    print(Autonomous.request("gemini-1.5-flash", "Hello, Gemini!"))


    sleep(0.5)

