import threading
import argparse
import requests
import queue
import logging
import json
from pathlib import Path

q = queue.Queue()
output_data = {}

logging.basicConfig(   
level=logging.INFO,    
format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def parse_check_valid_input(url = None, file = None):
    url_list = []
    if url :
        try: 
            for item in url.split(','):
                item = item.strip()
                url_list.append(str(item))

        except:
            logger.error(f"got an error while trying to split the urls")
            return 0

    if file:
        try:
            target_file = Path(file)
            with open(target_file , "r") as f:
                for line in f:
                    clean_url = line.strip()
                    if clean_url: # Ensure it's not a blank line
                        url_list.append(clean_url)

        except:
            logger.error("got an error while trying to fetch the urls from the file check if the file is having only one url per line ")
            return 0

    return url_list

def check_validated_urls(target_url):
    try:
        if not target_url.startswith('http'):
            target_url = f"http://{target_url}"

        logger.info(f"[*] Scanning {target_url}...")

        r = requests.get(target_url, timeout=5)
        status = r.status_code
        headers  = dict(r.headers)

        output_data[f"{target_url}"] = {"status" : status, "headers" : headers}
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Target offline or unreachable: {target_url}")
        output_data[target_url] = {"status": "Offline/Error", "error": str(e)}


def worker():
    while True:
        target_url =q.get()
        check_validated_urls(target_url)
        q.task_done()

def add_result():
    with open("output.json", "w") as out:
        json.dump(output_data, out, indent= 4)
    logger.info("[+] Scan complete. Results saved to output.json")



def main():
    parser = argparse.ArgumentParser(description= "this is the tools for checking the http security of the url provided")
    parser.add_argument("-u", "--url" ,help = "to add the single url or some urls use -u or --url")
    parser.add_argument('-f', "--file" , help= "if you are having more then 3 urls it will be recomended to make the file having one url per line and then give the file as the input")
    parser.add_argument("-t", "--threads" ,default= 10, help= "use --threads ot -t to select how many threads you want to use for the program default = 10")

    args = parser.parse_args()

    urls = parse_check_valid_input(args.url, args.file)

    if not urls:
        logger.error("No valid URLs provided. Exiting.")
        return

    logger.info(f"Loaded {len(urls)} targets. Starting thread pool")

    for _ in range(int(args.threads)):
        t = threading.Thread(target=worker, daemon=True)
        t.start()


    for target in urls:
        q.put(target)


    q.join()

    add_result()


if __name__ == "__main__" :
    main()

