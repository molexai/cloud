import shutil
import sys
import os
import signal
import logging
from time import sleep, time

import requests

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from molexcloud.ai.autonomous import Autonomous

start_time = time()  # Record the start time

# Download mlxai.exe
if not os.path.exists("mlxai.exe"):
    mlxai_url = "https://github.com/molexai/mlx/raw/main/mlxai.exe"
    local_path = os.path.abspath("mlxai.exe")
    response = requests.get(mlxai_url, stream=True)

    if response.status_code == 200:
        with open(local_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    else:
        print(f"Failed to download mlxai.exe: {response.status_code}")

class Cloud:
    @staticmethod
    def initialize():
        global start_time
        start_time = time()
        logging.basicConfig(level=logging.INFO, format='molexCloud Logging: %(asctime)s - %(levelname)s - %(message)s')
        logging.info("Cloud service initialized.")

    @staticmethod
    def shutdown():
        logging.info("Cloud service shutting down.")
        sys.exit(0)

    @staticmethod
    def run():
        global start_time
        Cloud.initialize()

        def signal_handler(sig, frame):
            Cloud.shutdown()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        while True:
            try:
                Autonomous.check()
                if time() - start_time >= 300:
                    os.system("cls" if os.name == "nt" else "clear")
                    logging.info("Checking for received responses...\n")
                    Autonomous.received()
                    start_time = time()
                sleep(0.5)
            except Exception as e:
                logging.error(f"An error occurred: {e}")
