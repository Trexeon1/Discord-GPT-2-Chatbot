import json
import os
from dotenv import load_dotenv

load_dotenv()
parsed_str = ""
MY_USERNAME = os.getenv("MY_USERNAME")
END_DELIMITER = "<|endoftext|>\n"


def remove_newlines(string):
    string = string.splitlines()
    string = " ".join(string)
    return string


for file in os.listdir():
    filename = os.fsdecode(file)

    if filename.endswith('.json'):
        with open(filename, 'r') as f:
            pyObj = json.load(f)
            pyObj = pyObj[::-1]

        for message in pyObj:
            message_content = remove_newlines(message['content'])
            if message_content == "":
                continue

            if message['author']['username'] == MY_USERNAME:
                message_str = f"[me] {message_content}\n"
            else:
                message_str = f"[others] {message_content}\n"
            parsed_str += message_str

        parsed_str += END_DELIMITER

with open('data.txt', 'w', encoding="utf-8") as f:
    f.write(parsed_str)
