import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
AUTH = os.getenv("AUTH")
CHANNEL_ID = os.getenv("CHANNEL_ID")


def get_messages(channel_id, last_message_id=None):
    headers = {
        "authorization": AUTH,
        "accept-encoding": "json",
        "content-type": "application/json"
    }
    if last_message_id is None:
        res = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100", headers=headers)
    else:
        res = requests.get(
            f"https://discord.com/api/v9/channels/{channel_id}/messages?before={last_message_id}&limit=100",
            headers=headers)
    data = json.loads(res.content)
    json_obj = json.dumps(data, indent=4, sort_keys=True)
    return json.loads(json_obj)


def clean(messages_lst: list):
    new_lst = [x for x in messages_lst if x['content'][:4] != 'http' and len(x['attachments']) == 0]
    print(len(new_lst))
    return new_lst


def main():
    num = int(input('Number of messages you would like to download '))
    messages = get_messages(CHANNEL_ID)
    last_message_id = messages[-1]['id']

    while len(messages) < num:
        messages = clean(messages)
        messages += get_messages(CHANNEL_ID, last_message_id=last_message_id)
        last_message_id = messages[-1]['id']

    with open(f"{CHANNEL_ID}_messages.json", "w") as f:
        json.dump(clean(messages), f)


if __name__ == '__main__':
    main()
