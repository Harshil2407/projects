import re
import argparse
import sys
import logging 
from pathlib import Path
import json

logging.basicConfig(   
			 level=logging.INFO,    
			 format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

LOG_PATTERN = re.compile(
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})'       # Extracts IP Address
    r'.*?"(?P<method>[A-Z]+)\s+'             # Extracts HTTP Method (e.g., GET)
    r'(?P<endpoint>.*?)\s+HTTP.*?"\s+'       # Extracts Endpoint (e.g., /login)
    r'(?P<status>\d{3})'                     # Extracts 3-digit Status Code
)

def stream_log_events(file):
    try:
        with open(Path(file), "r") as f:
            for line in f:
                match = LOG_PATTERN.search(line)
                if match:
                    yield match.groupdict()

    except Exception as e : 
        logger.error(f"we got an error {e} reading or accessing the input file.")



def parse_log_file(file_path, ):
    parsed_data = {}

    for event in stream_log_events(file_path):
        ip = event['ip']

        if ip not in parsed_data:
            parsed_data[ip] = []

        parsed_data[ip].append({
            "method" : event['method'],
            "endpoint": event['endpoint'],
            "status_code" : int(event['status'])
            })
    return parsed_data


def main():
    parser = argparse.ArgumentParser(description= "it is the log parser with the re ")
    parser.add_argument("-f" , "--file",required =True, help = "use -f or --file to give the log file which should be parsed")

    args = parser.parse_args()

    if not Path(args.file).exists():
        logger.error("please enter the file containing logs which should be parsed")
        sys.exit(1)

    data = parse_log_file(args.file)
    
    with open("result.json" , "w") as result:
        json.dump(data, result, indent=4)
        logger.info("Successfully saved parsed logs to result.json")


if __name__ == "__main__":
    main()
