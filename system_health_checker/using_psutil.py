import psutil
import argparse
import yaml
from pathlib import Path
import logging
import sys

logging.basicConfig(   
			 level=logging.INFO,    
			 format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

def get_memory_usage():
    memory_usage = psutil.virtual_memory()
    return memory_usage.percent

def load_yaml(yaml_path):
    file = Path(yaml_path)
    if file.exists() and file.stat().st_size != 0 :
                
            with open(f"{file}", "r") as f:
                try:
                    config = yaml.safe_load(f)
                    return config

                except yaml.YAMLError as e:
                    logger.exception(f"[error] : we got error in {file} {e}")
                    sys.exit(1)
                     
    else:
           logger.error(f"{file} does not exists. or is empty")
           sys.exit(1)




def main():
    parser = argparse.ArgumentParser(description= "it is to take the input of the yaml file ")
    parser.add_argument("-y", "--yaml", default = "mod_2.yaml" , help = "you can choose any yaml file but if not then the default yaml file is the mod_2.yaml")

    args = parser.parse_args()
    config = load_yaml(args.yaml)
    ram_limit = config.get("max_ram_percent",80) #used 80 as default value if not specified in the yaml
    cpu_usage_limit = config.get("max_cpu_percent" , 85) #here 85 as the default value
    
    live_cpu_usage = get_cpu_usage()
    live_ram = get_memory_usage()

    if live_ram >= ram_limit and live_cpu_usage >= cpu_usage_limit:
        logger.critical("[critical]system is in danger as cpu usage and ram uasge both have hit the limit.")

    elif live_ram >= ram_limit and live_cpu_usage<= cpu_usage_limit:
        logger.error("ram is used above its limit but cpu is in stable state now")

    elif live_cpu_usage >= cpu_usage_limit and live_ram <= ram_limit:
        logger.error("cpu is used about its limits and ram is in stable state now")

    elif (65 <= live_ram <= 80) and (65 <= live_cpu_usage <= 80):
        logger.warning("[warning] : there is no problem yet but keep a close eye.")

    else:
        logger.info("[info] : both cpu and memory uage are in the limits and better state")
        

if __name__ == "__main__":
    main()

