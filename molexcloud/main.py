import shutil
import sys
import os
from time import sleep, time

import requests

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from molexcloud.ai.autonomous import Autonomous

start_time = time()  # Record the start time

# Download mlxai.exe
if not os.path.exists("mlxai.exe"):
    mlxai_url = "https://github.com/molexai/cloud/raw/main/molexcloud/ai/mlxai.exe"
    local_path = os.path.abspath("mlxai.exe")
    response = requests.get(mlxai_url, stream=True)

    if response.status_code == 200:
        with open(local_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    else:
        print(f"Failed to download mlxai.exe: {response.status_code}")

while True:
    # Check for AI requests
    Autonomous.check()
    if time() - start_time >= 300:  # Check for received responses every minute
        os.system("cls" if os.name == "nt" else "clear")
        print("molexAI Cloud: Checking for received responses...\n")
        Autonomous.received()  # Check for received responses every minute
        start_time = time()
    sleep(0.5)