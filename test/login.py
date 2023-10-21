import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'http://localhost:3000',
    'Referer': 'http://localhost:3000/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0',
    'sec-ch-ua': '"Opera";v="103", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

json_data = {
    'username': 'test',
    'password': 'password',
}

response = requests.post('http://localhost:8000/auth/login', headers=headers, data=json_data)
print()