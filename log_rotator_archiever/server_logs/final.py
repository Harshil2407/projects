import os
import shutil
import gzip
import argparse
import logging
from pathlib import Path
from datetime import datetime

# --- 1. CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Log Rotation and Archiving Utility")
parser.add_argument("-f", "--file", default="app.log", help="Target log file to rotate")
args = parser.parse_args()

target_file = Path(args.file)

# --- 2. PHASE 1: ROTATE AND COMPRESS ---
def zip_app(log_file):
    if not log_file.exists():
        logger.error(f"FATAL: {log_file} does not exist.")
        return # Exit the function early

    if log_file.stat().st_size == 0:
        logger.warning(f"SKIPPED: {log_file} is already empty.")
        return

    try:
        # Step A: Generate the new filenames dynamically
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        copied_log = Path(f"{log_file}.{timestamp}.copied")
        final_archive = Path(f"{log_file}.{timestamp}.gz")

        # Step B: Copy the file safely
        logger.info(f"Copying {log_file} to {copied_log}...")
        shutil.copy2(log_file, copied_log)

        # Step C: Truncate the ORIGINAL file immediately
        # We open the original file in "w" (write) mode to clear it out
        with open(log_file, "w") as original:
            original.truncate(0)
        logger.info(f"Truncated original file: {log_file}")

        # Step D: Compress the copied file
        logger.info(f"Compressing into {final_archive}...")
        with open(copied_log, "rb") as f_in:
            with gzip.open(final_archive, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Step E: Delete the uncompressed copy
        os.remove(copied_log)
        logger.info(f"SUCCESS: Log rotated and compressed to {final_archive}")

    except PermissionError:
        logger.error(f"Failed to access {log_file}. Is it locked by another process?")
        raise # Pass the error up to the main try/except block

# --- 3. PHASE 2: RETENTION POLICY (PURGE) ---
def time_based_del(directory, days_to_keep=7):
    logger.info(f"Scanning {directory} for archives older than {days_to_keep} days...")
    
    # We scan the parent directory for ALL .gz files
    for archive in directory.glob("*.gz"):
        try:
            # Calculate how many days old this specific archive is
            modified_time = datetime.fromtimestamp(archive.stat().st_mtime)
            age_in_days = (datetime.now() - modified_time).days

            if age_in_days >= days_to_keep:
                os.remove(archive)
                logger.info(f"PURGED: {archive.name} ({age_in_days} days old)")
        
        except Exception as e:
            logger.error(f"Could not process {archive.name}: {e}")

# --- 4. MAIN EXECUTION ---
if __name__ == "__main__":
    try:
        logger.info("--- Starting Log Rotation Sequence ---")
        
        # 1. Rotate the active file
        zip_app(target_file)
        
        # 2. Scan the folder (target_file.parent) and purge old zips
        time_based_del(target_file.parent, days_to_keep=7)
        
        logger.info("--- Log Rotation Sequence Complete ---")

    # Catching a specific Exception object "e" so we can log the exact stack trace
    except Exception as e:
        logger.exception(f"CRITICAL FAILURE: The script crashed. Details: {e}")
