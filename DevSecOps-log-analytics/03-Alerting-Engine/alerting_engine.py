import json
import logging
import argparse
import sys
import time
import requests
from pathlib import Path

logging.basicConfig(   
             level=logging.INFO,    
             format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

WEBHOOK_URL = "<put your link here>" 
STATE_FILE = "state.json"
COOLDOWN_SECONDS = 300  

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
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            logger.info("[+] Successfully sent alert to Webhook!")
        else:
            logger.error(f"[-] Failed to send webhook. Status: {response.status_code}")
    except Exception as e:
        logger.error(f"[-] Webhook connection error: {e} or you havent entered the valid webhook link in the program please do it first")


def check_parsed_result(data):
    try:
        for ip, events in data.items():
            err_count = 0
            for request in events:
                if request['status_code'] in [403,401]:
                    err_count += 1

                endpoint = request['endpoint']
                if "../" in endpoint or "/etc/" in endpoint or ".env" in endpoint:
                    message = f"Path traversal detected! IP {ip} targeted {endpoint}"
                    logger.critical(message)
                    
                    if not is_rate_limited(ip):
                        send_webhook_alert(message)

            if err_count > 3:
                message = f"Possible Brute Force! IP {ip} had {err_count} failed attempts."
                logger.warning(message)
                
                if not is_rate_limited(ip):
                    send_webhook_alert(message)
                        
    except Exception as e:
        logger.error(f"we got an error {e} while checking the parsed data")


def main():
    parser = argparse.ArgumentParser(description= "tool for detecting the output from the json file ")
    parser.add_argument("-f", "--file", default= "result.json", help = "please enter the json file which you got after execution of project 1" )

    args = parser.parse_args()

    target_file  = Path(args.file)
    
    if not target_file.exists():
        logger.error(f" Cannot find the file '{args.file}'. Did Project 1 run successfully?")
        sys.exit(1)
    
    with open(args.file, "r") as f:
        data = json.load(f)

    check_parsed_result(data)


if __name__ == "__main__":
    main()
