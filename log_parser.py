import sys
from pathlib import Path

# 1. Argument Handling & Safe Exit
if len(sys.argv) > 1:
    filename = sys.argv[1]
else: 
    print("[-] Please enter a valid file name.")
    sys.exit(1) # Kill the script immediately if no file is provided

file_path = Path(filename)
target_users = set()

# 2. File Parsing Phase
if file_path.exists(): 
    # Use 'file_path' directly, no need for f-strings here
    with open(file_path, "r") as f:
        # BUG FIX 1: Loop over 'f', not 'filename'
        for line in f:
            # BUG FIX 2: Capital 'F'
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

# 3. Export Phase
# Using "a" mode so we append to the blacklist instead of overwriting it
with open("blacklist.txt", "a") as black:
    black.write("\n--- THREAT INTEL EXTRACT ---\n")
    for entry in sorted(target_users):
        black.write(f"{entry}\n")
        print(f"[+] Logged Threat: {entry}")
