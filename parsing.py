import json
import os
from dotenv import load_dotenv

load_dotenv()
parsed_str = ""
MY_USERNAME = os.getenv("MY_USERNAME")
END_DELIMITER = "\n<|endoftext|>\n"

for file in os.listdir():
    filename = os.fsdecode(file)
    if filename.endswith('.json'):
        with open(filename, 'r') as f:
            pyObj = json.load(f)
        for message in pyObj:
            if message['author']['username'] ==  MY_USERNAME:
                message_str = f"[me] {message['content']}\n"
            else:
                message_str = f"[others] {message['content']}\n"
            parsed_str += message_str
        parsed_str += END_DELIMITER
