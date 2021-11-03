import requests
import os
import json


def elk_data_to_json(elk_processed_data=None):
    # Save data to json object
    data = {
        "elk": elk_processed_data
    }
    return json.dumps(data)


def splunk_data_to_json(splunk_processed_data=None):
    # Save data to json object
    data = {
        "splunk": splunk_processed_data,
    }
    return json.dumps(data)


def elk_data_processor(raw_data):
    return raw_data


def splunk_data_processor(raw_data):
    return raw_data


def postrequest(url, data):
    r = requests.post(url, data=data)
    return r


def send_to_elk(data):
    ELK_URL = os.getenv('ELK_URL', """http://localhost:9200/""")
    r = postrequest(ELK_URL, data)
    print(r)


def send_to_splunk(data):
    SPLUNK_URL = os.getenv('SPLUNK_URL', """http://localhost:8088/""")
    r = postrequest(SPLUNK_URL, data)
    print(r)


def sender(splunk_processed_data=None, elk_processed_data=None):
    try:
        elk_data = elk_data_to_json(elk_processed_data)
        send_to_elk(elk_data)
        # splunk_data = splunk_data_to_json(splunk_processed_data)
        # send_to_splunk(splunk_data)
    except Exception as e:
        print(e)


def main():
    print("Lets go!")
    splunk_raw_data = None
    elk_raw_data = None
    splunk_processed_data = splunk_data_processor(splunk_raw_data)
    elk_processed_data = elk_data_processor(elk_raw_data)
    sender(splunk_processed_data,elk_processed_data)


if __name__ == '__main__':
    main()
