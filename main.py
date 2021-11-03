# pylint: disable=broad-except
import requests
import os
import json
from kubernetes import client, config, watch


def event_to_data(event):
    return event


def event_handler(event):
    raw_data = event_to_data(event)
    splunk_processed_data = splunk_data_processor(raw_data)
    elk_processed_data = elk_data_processor(raw_data)
    sender(splunk_processed_data, elk_processed_data)


def listener():
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.CoreV1Api()
    # print("Listing pods with their IPs:")
    # ret = v1.list_pod_for_all_namespaces(watch=False)
    # for i in ret.items:
    #         if(i.metadata.namespace=="ingress-nginx"):
    #                 print(f'{i.status}, {i.metadata.namespace},{i.metadata.name}')

    w = watch.Watch()
    for e in w.stream(v1.read_namespaced_pod_log, name="ingress-controller-ingress-nginx-controller-746658c4b8-7cntg", namespace="ingress-nginx"):
        print(e)
        event_handler(e)


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
    listener()


if __name__ == '__main__':
    main()
