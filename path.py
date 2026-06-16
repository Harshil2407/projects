from pathlib import *
import sys 

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    print("please enter the file that you want to open.")

file_path = Path(file)

if file_path.exists() : 
    with open( file , "r") as f: 
        content = f.read()
        print(f" {file}files content is shown below")
        print("_" * 40 )
        print(content)
else: 
    print("error")

