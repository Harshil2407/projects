import gzip
from pathlib import Path 
import os
import argparse
import shutil 
from datetime import datetime
import logging 

#loging basic config
logging.basicConfig(   
			 level=logging.INFO,    
			 format="%(asctime)s - %(levelname)s - %(message)s")logger = logging.getLogger(__name__)

#parser setup taking input from the args 
parser = argparse.ArgumentParser(description = "take the input of the file from argparse")
parser.add_argument("--f" , "--file" , default = "app.log", help = "to give the file name as the input")
args = parser.parse_args()

#path to the target file 
target_file = Path(args.file)

def zip_app():
    if target_file.exists(): 

        if not target_file.stat().st_size == 0:
            
            if not app_log.exists():
                logger.info(f"starting the zipping the {target_file}")
                shutil.copy2(target_file, target_archive)

        
                logger.info(f"copied the {target_file} into the {target_archive}")
                with open("targget_archive", "rb") as f_in:
                    with gzip.open("app_log", "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                with open(f"{target_file}" , "w") as tf:
                    tf.truncate(0)
                logger.info("zippeed the file and truncated the original")
               
            else:
                logger.error("the file we are going to zip already exixts when the 7 days complete then only we are going to remove the file and then only we are going to zip the existing log so be patient ")
        else: 
            logger.error(f"{target_file} is empty already ")

    else:
        logger.error(f"{target_file} does not exist")

#time from the last modification
modified_time = datetime.fromtimestamp(app_log.stat().st_mtime)
ctime = (datetime.now() - modified_time ).days

def time_based_del():
    if ctime >= 7 :
        os.remove(Path(app_log))
        logger.info(f"deleted {app_log}")
    else :
        logger.info("the file is not 7 days old yet")


try : 
    time_based_del()
    zip_app()
    logger.info("executing both in the sequence first time_based_del and then zip_app")
except:
    logger.exception("some error occured .")
