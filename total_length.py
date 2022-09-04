import os
import json

length = 0

for file in os.listdir():
    filename = os.fsdecode(file)
    if filename.endswith('.json'):
        with open(filename, 'r') as f:
            pyObj = json.load(f)
        length += len(pyObj)

print(length)
