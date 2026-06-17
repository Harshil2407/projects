import os
import sys 
from pathlib import Path 
import argparse

parser = argparse.ArgumentParser(description="Mini-Tripwire: File Integrity Monitor")

parser.add_argument(
    "-d", "--directory",
    default="secure_vault",
    help="The target directory to monitor (secure_vault is default)"
)

mode_group = parser.add_mutually_exclusive_group(required=True)
mode_group.add_argument("--baseline", action="store_true", help="Generate the new baseline")
mode_group.add_argument("--audit", action="store_true", help="Does the audit against the baseline records")

args = parser.parse_args()

folder = Path(args.directory)
baseline_data = {}

# --- PHASE 1: BASELINE ---
if args.baseline:
    print(f"[*] Initializing BASELINE generation for '{folder}'...")
    
    # Open in 'w' mode to create a fresh snapshot, and open it BEFORE the loop
    with open("baseline.txt", "w") as f:
        for file in folder.iterdir():
            if file.is_file():
                filesize = file.stat().st_size
                # Using "|" as the separator, and writing file.name (not the full path)
                f.write(f"{file.name}|{filesize}\n") 
                
    print("[+] Baseline successfully generated.")

# --- PHASE 2: AUDIT ---
elif args.audit:
    print(f"[*] Initializing SECURITY AUDIT for '{folder}'...")

    baseline_file = Path("baseline.txt")
    if not baseline_file.exists():
        print("[-] FATAL: baseline.txt not found. Try the --baseline argument first.")
        sys.exit(1)

    # 1. Load the Dictionary
    with open(baseline_file, "r") as base:
        for line in base: # Fixed variable name
            clean_line = line.strip()
            parts = clean_line.split("|") # Matches the "|" from Phase 1

            if len(parts) == 2:
                filename = parts[0]
                size = int(parts[1])
                baseline_data[filename] = size

    print("[+] Baseline data loaded into memory.")
    print(f"[*] Scanning '{folder}' for modifications...\n")

    # 2. Compare Current Files to Dictionary
    for file_path in folder.iterdir():
        if file_path.is_file():
            try:
                current_name = file_path.name
                current_size = file_path.stat().st_size

                if current_name in baseline_data:
                    expected_size = baseline_data[current_name]
                    
                    if current_size != expected_size:
                        print(f"[CRITICAL] Unauthorized modification detected in: {current_name}")
                else:
                    print(f"[WARNING] Untracked file found: {current_name}")

            except PermissionError:
                pass
                
    print("\n[*] Audit complete.")
