import os
import sys 
from pathlib import Path 
import argparse


parser = argparse.ArgumentParser(description = "Mini-Tripwire: File Integrity Monitor")

parser.add_argument(
        "-d","--directory",
        default = "secure_vault" ,
        help = "Thw target directory to monitor (secure_vault is default )"
    )


mode_group = parser.add_mutually_exclusive_group(required = True)
mode_group.add_argument("--baseline", action = "store_true", help = "generate the new baseline")
mode_group.add_argument("--audit", action = "store_true", help = "does the audit against the baseline records")

args = parser.parse_args()

folder = Path(args.directory)

baseline_data={}

os.chdir(path_to_folder)
if args.baseline:
    print(f"[*] Initializing BASELINE generation for '{target_folder}'...")
    for files in d:
        filesize = file.stat().st_size
        with open("baseline.txt", "a") as f:
                f.add(f"{file} : {filesize}")

elif args.audit:
    print(f"[*] Initializing SECURITY AUDIT for '{target_folder}'...")

    baseline_file = Path("baseline.txt")
    if not baseline_file.exists():
        print(f"the file baseline.txt is not found try the --baseline argument first to create the analysys of the data then only you can compare and check")
        sys.exit(1)

    with open("baseline.txt" , "r") as base:
            for lines in f:
                clean_line = line.strip()

                parts = clean_line.split("|")

                if len(parts) == 2:
                    filename = parts[0]

                    size = int(parts[1])

                    baseline_data[filename] = size

    print("data stored into the dictionary")

    print(f"[*] Scanning {folder} for modifications...\n")

    for file_path in folder.iterdir():
        if file_path.is_file():
            try:
                current_name = file_path.name
                current_size = file_path.stat().st_size

                if current_name in baseline_data:
                    expected_size = baseline_data[current_name]
                    
                    if current_size != expected_size:
                        print(f"[critical] : unauthorized modification detected in {current_name}")
                else:
                    print(f"[warning] : unchecked file found : {current_name}")

            except PermissionError:
                # If the OS blocks us from reading a file, silently skip it
                pass

