import requests

url = 'http://127.0.0.1:8000/user/register'
payload ={"username": "test", "password": "password"}
resp = requests.post(url=url, json=payload)
print(resp.json())