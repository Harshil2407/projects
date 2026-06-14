import sys

from pathlib import Path

def get_target_directory():
    if len(sys.argv)> 1:
        target_path = Path(sys.argv[1])
    else: 
        target_path = Path(Path.cwd())
    
    return target_path


directory = get_target_directory()


if not directory.exists() or not directory.is_dir():
    print(f"the path provided {directory} is not valid or it is not a directory")
    sys.exit(1)

print(f"the directory: {directory}")
print("_"*40)


subdirect = []
subfiles = []


for file in directory.iterdir():
    if file.is_dir():
        subdirect.append(file.name)
    else :
        subfiles.append(file.name)

for d in sorted(subdirect):
    print(f"{d}/")

for f in sorted(subfiles):
    print(f"{f}" )
