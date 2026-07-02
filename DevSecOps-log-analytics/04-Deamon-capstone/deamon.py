import logging
import argparse
import threading
import queue
from pathlib import Path
import os
import json
import time
import re
import requests

logging.basicConfig(   
			 level=logging.INFO,    
			 format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

event_q= queue.Queue()
files = []

brute_force_tracker = {}

parsed_data = {}
WEB_HOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "YOUR_WEBHOOK_URL_HERE")
STATE_FILE = "state.json"
COOLDOWN_SECONDS = 300


LOG_PATTERN = re.compile(
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})'       
    r'.*?"(?P<method>[A-Z]+)\s+'            
    r'(?P<endpoint>.*?)\s+HTTP.*?"\s+'     
    r'(?P<status>\d{3})'                
)

def total_files(file):

    for f in file.split(','):
        if Path(f).exists():
            files.append(str(f))
    
    return files

def parse_tail(file_path):
    try:
        with open(Path(file_path), "r") as f:
                f.seek(0, os.SEEK_END)

                while True:
                    line = f.readline()

                    if not line:
                        time.sleep(0.1)
                        continue

                    match = LOG_PATTERN.search(line)

                    if match:
                        event = match.groupdict()
                        logger.info(f"[*] Waiter saw: {event['status']} from {event['ip']}")
                        event_q.put(event)
                        

    except Exception as e:
        logger.error(f"Error reading file: {e}")


def is_rate_limited(ip_address):
    state = {}
    
    if Path(STATE_FILE).exists():
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            
    current_time = time.time()
    
    if ip_address in state:
        last_alert_time = state[ip_address]
        if (current_time - last_alert_time) < COOLDOWN_SECONDS:
            logger.info(f"[-] Rate limited: Already alerted about {ip_address} recently.")
            return True            

    state[ip_address] = current_time
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
        
    return False 


def send_webhook_alert(alert_message):
    payload = {
        "text": f"🚨 *SECURITY ALERT* 🚨\n{alert_message}"
    }
    try:
        response = requests.post(WEB_HOOK_URL, json=payload)
        if response.status_code == 200:
            logger.info("[+] Successfully sent alert to Webhook!")
        else:
            logger.error(f"[-] Failed to send webhook. Status: {response.status_code}")
    except Exception as e:
        logger.error(f"[-] Webhook connection error: {e} or you havent entered the valid webhook link in the program please do it first")

def check_alert():
    try:
        while True:
            event = event_q.get()
            ip = event['ip']
            endpoint = event['endpoint']
            status = int(event['status'])
            if '../' in endpoint or '/etc/' in endpoint:
                if not is_rate_limited(ip):
                    send_webhook_alert("trying to access unauthorized critical files")

            if status in [401,402]:
                brute_force_tracker[ip] = brute_force_tracker.get(ip, 0) + 1

                if brute_force_tracker[ip] > 3:
                    if not is_rate_limited(ip):
                        send_webhook_alert(f"Possible Brute Force! IP {ip} had {brute_force_tracker[ip]} failed attempts.")
                        # Reset their score so we don't spam them forever
                        brute_force_tracker[ip] = 0

            event_q.task_done()

    except Exception as e:
        logger.error(f"got an error {e} or an exception while trying to check the parsed data ")



def main():
    parser = argparse.ArgumentParser(description="this is the capston for the log parsing and alerting ")
    parser.add_argument("-f", "--file", help = "to add the file that should be constantly running in the background constantly.")
    args= parser.parse_args()
    
    files_to_watch = total_files(args.file)
    
    if not files_to_watch:
        logger.error("please enter the valid files to watch or enter the files to watch ")
        return

    logger.info(f"Starting Daemon. Watching {len(files_to_watch)} file(s)")
    threading.Thread(target=check_alert, daemon=True).start()

    for f in files:
        threading.Thread(target=parse_tail,args= (f,) ,daemon = True).start()

    while True:
        time.sleep(1)



if __name__ == "__main__":
    main()
