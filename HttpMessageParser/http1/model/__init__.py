import json

import requests

url = "http://127.0.0.1:8080"
headers = {"Content-Type": "application/json", "hhh": "123"}
data = {"test": "123", "name": "[]*&*^%patrick"}
res = requests.post(url=url, headers=headers, data=json.dumps(data))
print(res.text)
