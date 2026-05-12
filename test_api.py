import requests
import json

url = 'http://127.0.0.1:5000/predict'

# Sample data for a normal connection (approximated from dataset distribution)
sample_data = {
    "duration": 0,
    "protocoltype": "tcp",
    "service": "http",
    "flag": "SF",
    "srcbytes": 181,
    "dstbytes": 5450,
    "land": 0,
    "wrongfragment": 0,
    "urgent": 0,
    "hot": 0,
    "numfailedlogins": 0,
    "loggedin": 1,
    "numcompromised": 0,
    "rootshell": 0,
    "suattempted": 0,
    "numroot": 0,
    "numfilecreations": 0,
    "numshells": 0,
    "numaccessfiles": 0,
    "numoutboundcmds": 0,
    "ishostlogin": 0,
    "isguestlogin": 0,
    "count": 8,
    "srvcount": 8,
    "serrorrate": 0.0,
    "srvserrorrate": 0.0,
    "rerrorrate": 0.0,
    "srvrerrorrate": 0.0,
    "samesrvrate": 1.0,
    "diffsrvrate": 0.0,
    "srvdiffhostrate": 0.0,
    "dsthostcount": 9,
    "dsthostsrvcount": 9,
    "dsthostsamesrvrate": 1.0,
    "dsthostdiffsrvrate": 0.0,
    "dsthostsamesrcportrate": 0.11,
    "dsthostsrvdiffhostrate": 0.0,
    "dsthostserrorrate": 0.0,
    "dsthostsrvserrorrate": 0.0,
    "dsthostrerrorrate": 0.0,
    "dsthostsrvrerrorrate": 0.0
}

# Sample data for an anomaly (approximated)
anomaly_sample = {
    "duration": 0,
    "protocoltype": "tcp",
    "service": "http",
    "flag": "S0", # S0 flag is common in anomalies
    "srcbytes": 0,
    "dstbytes": 0,
    "land": 0,
    "wrongfragment": 0,
    "urgent": 0,
    "hot": 0,
    "numfailedlogins": 0,
    "loggedin": 0,
    "numcompromised": 0,
    "rootshell": 0,
    "suattempted": 0,
    "numroot": 0,
    "numfilecreations": 0,
    "numshells": 0,
    "numaccessfiles": 0,
    "numoutboundcmds": 0,
    "ishostlogin": 0,
    "isguestlogin": 0,
    "count": 255, # High connection count
    "srvcount": 255,
    "serrorrate": 1.0,
    "srvserrorrate": 1.0,
    "rerrorrate": 0.0,
    "srvrerrorrate": 0.0,
    "samesrvrate": 0.05,
    "diffsrvrate": 0.06,
    "srvdiffhostrate": 0.0,
    "dsthostcount": 255,
    "dsthostsrvcount": 255,
    "dsthostsamesrvrate": 0.05,
    "dsthostdiffsrvrate": 0.07,
    "dsthostsamesrcportrate": 0.0,
    "dsthostsrvdiffhostrate": 0.0,
    "dsthostserrorrate": 1.0,
    "dsthostsrvserrorrate": 1.0,
    "dsthostrerrorrate": 0.0,
    "dsthostsrvrerrorrate": 0.0
}

try:
    print("\nTesting Normal Sample...")
    response = requests.post(url, json=sample_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    print("\nTesting Anomaly Sample...")
    response = requests.post(url, json=anomaly_sample)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
