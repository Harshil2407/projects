import json
import logging
import argparse
import sys
from pathlib import Path

logging.basicConfig(   
			 level=logging.INFO,    
			 format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



def check_parsed_result(data):
    try:
        for ip, events in data.items():
            err_count = 0
            for request in events:
                if request['status_code'] in [403,401]:
                    err_count += 1

                endpoint = request['endpoint']
                if "../" in endpoint or "/etc/" in endpoint or ".env" in endpoint :
                    logger.critical(f"path traversal detected in {ip} targeted {endpoint}")
            if err_count > 3:
                logger.warning(f"we got an chance of the attacker:{ip} trying to bruteforce cause it got err_count:{err_count}")
                        
        
    except Exception as e:
        logger.error(f"we got an error {e} while cheking the parsed data")




def main():
    parser = argparse.ArgumentParser(description= "tool for detecting the output from the json file ")
    parser.add_argument("-f", "--file", default= "result.json", help = "please enter the json file which you got after execution of project 1" )

    args = parser.parse_args()

    target_file  = Path(args.file)
    
    if not target_file.exists():
        logger.error(f" Cannot find the file '{args.file}'. Did Project 1 run successfully?")
        sys.exit(1)
    
    with open(args.file, "r") as f:
        data =json.load(f)

    check_parsed_result(data)



if __name__ == "__main__":
    main()
