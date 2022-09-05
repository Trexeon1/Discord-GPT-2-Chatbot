import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
parsed_str = ""
MY_USERNAME = os.getenv("MY_USERNAME")
END_DELIMITER = "<|endoftext|>\n"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def remove_newlines(string):
    string = string.splitlines()
    string = " ".join(string)
    return string


def delta_time(new_timestamp_str, old_timestamp_str):
    timestamp1 = datetime.strptime(new_timestamp_str, DATE_FORMAT)
    timestamp2 = datetime.strptime(old_timestamp_str, DATE_FORMAT)
    d_time = timestamp1 - timestamp2
    return d_time.total_seconds()


for file in os.listdir():
    filename = os.fsdecode(file)

    if filename.endswith('.json'):
        previous_m_ts = None  # previous message timestamp
        with open(filename, 'r') as f:
            pyObj = json.load(f)
            pyObj = pyObj[::-1]

        for message in pyObj:
            message_content = remove_newlines(message['content'])
            if message_content == "":
                continue

            current_m_ts = message['timestamp'][:19]  # previous message timestamp
            if previous_m_ts is not None:
                time_difference = delta_time(current_m_ts, previous_m_ts)
                if time_difference > 14400:
                    parsed_str += END_DELIMITER

            if message['author']['username'] == MY_USERNAME:
                message_str = f"[me] {message_content}\n"
            else:
                message_str = f"[others] {message_content}\n"
            parsed_str += message_str
            previous_m_ts = current_m_ts

        parsed_str += END_DELIMITER

with open('data.txt', 'w', encoding="utf-8") as f:
    f.write(parsed_str[:-1])
