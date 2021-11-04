# pylint: disable=redefined-outer-name
from kubernetes import client, config, watch
import re
from time import strptime
import requests
import json

URL = "http://elastic.rancher.rabaz.org/athena/_doc"

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()
ret = v1.list_pod_for_all_namespaces(watch=False)

POD_NAMESPACE = "ingress-nginx"




data = {'remote_addr': '84.110.55.154', 'remote_user': '-', '@timestamp': '2021-11-03T23:18:00', 'request': 'GET /v3/subscribe?sockId=273 HTTP/1.1', 'status': '400', 'bytes_sent': '453', 'http_referer': '-', 'http_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36', 'gzip_ratio': ' "-"'}



def post_req(json_data):
    payload = json.dumps(json_data)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", URL, headers=headers, data=payload)

    print(response.status_code)

# post_req(data)




def main():
    v1 = client.CoreV1Api()
    w = watch.Watch()
    for i in ret.items:
        if (i.metadata.namespace=="ingress-nginx" and "ingress-controller" in i.metadata.name):
            pod_name = i.metadata.name
    POD_NAMESPACE = "ingress-nginx"    
    for pod_log in w.stream(v1.read_namespaced_pod_log,name=pod_name, namespace=POD_NAMESPACE):
        send_log(pod_log)
    

        
    

def send_log(pod_log):
    try:
        pod_json_log = convert_to_elk_format(pod_log)
        post_req(pod_json_log)
    except Exception as e:
        print(e)
        pass


def mock_elk():
    for i in ret.items:
            if(i.metadata.namespace=="ingress-nginx" and "ingress-controller" in i.metadata.name ):
                    pod_name = i.metadata.name
                    pod_log_list = v1.read_namespaced_pod_log( name=pod_name, namespace=POD_NAMESPACE).split('\n')

                    for pod_log in pod_log_list:
                        try:
                            pod_json_log = convert_to_elk_format(pod_log)
                            post_req(pod_json_log)
                        except Exception as e:
                            print(e)
                            pass
    return pod_log_list



def convert_to_elk_format(pod_log):

    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', pod_log)[0]
    pod_log=pod_log.split(ip)[1]
    
    remote_user = pod_log.split(' ')[2]

    pod_log = "-".join(pod_log.split(remote_user)[2:])
    
    time_local = pod_log.split('[')[1].split(']')[0]
    time_convert = convert_to_elk_time(time_local)

    pod_log = pod_log.split(time_local)[1].split(']')[1]

    request_pod = pod_log.split('"')[1]
    pod_log = pod_log.split(request_pod)[1]
    
    status = re.findall(r'\d+', pod_log)[0]

    pod_log = pod_log.split(status)[1]

    bytes_sent = re.findall(r'\d+', pod_log)[0]

    pod_log = pod_log.split(bytes_sent)[1]

    http_referer = pod_log.split('"')[1]
    
    pod_log = "-".join(pod_log.split(remote_user)[1:])
    
    http_user_agent = pod_log.split('"')[2]

    gzip_ratio = '"'.join(pod_log.split('"')[3:])


    pod_log_json={
        "remote_addr": ip,
        "remote_user": remote_user,
        "@timestamp" : time_convert,
        "request" : request_pod,
        "status" : status,
        "bytes_sent": bytes_sent,
        "http_referer": http_referer,
        "http_user_agent": http_user_agent,
        "gzip_ratio":gzip_ratio
        }
    return pod_log_json



def get_pod_logs(pod_name, pod_namespace):
    pod_log_list = v1.read_namespaced_pod_log( name=pod_name, namespace=pod_namespace).split('\n')        



def convert_to_elk_time(time):
    day = time.split("/")[0]
    month = time.split("/")[1]
    year = time.split("/")[2].split(":")[0]
    hour = time.split("/")[2].split(":")[1]
    min = time.split("/")[2].split(":")[2]
    sec = time.split("/")[2].split(":")[3].split(" ")[0]
    month = strptime(month, '%b').tm_mon
    time = f'{year}-{month}-{day}T{hour}:{min}:{sec}'
    return time

main()




