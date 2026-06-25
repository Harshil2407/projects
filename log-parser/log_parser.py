import sys
from pathlib import Path

if len(sys.argv) > 1:
    filename = sys.argv[1]
else: 
    print("[-] Please enter a valid file name.")
    sys.exit(1) 

file_path = Path(filename)
target_users = set()

if file_path.exists(): 
    with open(file_path, "r") as f:
        for line in f:
            if "Failed password" in line:
                words = line.split()
                try:
                    anchor_index = words.index("from")
                    username = words[anchor_index - 1]
                    ip_address = words[anchor_index + 1]
                    
                    combined_entry = f"{username} @ {ip_address}"
                    target_users.add(combined_entry)

                except ValueError:
                    pass

with open("blacklist.txt", "a") as black:
    black.write("\n--- THREAT INTEL EXTRACT ---\n")
    for entry in sorted(target_users):
        black.write(f"{entry}\n")
        print(f"[+] Logged Threat: {entry}")
