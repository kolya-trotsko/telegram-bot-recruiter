from pathlib import Path
import os
import logging

TG_TOKEN = ""

admin_chat_id = 1234567890

config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": ""
}


options = {
    "position 1": [
        "question 1",
        "question 2",
        "question 3"
    ],
    "position 2": [
        "question 1",
        "question 2"
    ],
    "position 3": [
        "question 1",
        "question 2",
        "question 3"
    ]
}

positions = options.keys()


log_path = os.path.join(Path(__file__).resolve().parent, "logfile.log")

logging.basicConfig(
    level=logging.ERROR,
    filename=log_path,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
