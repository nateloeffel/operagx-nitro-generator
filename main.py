import requests
import json

QUANTITY = 100

# im not a python dev gimme some slack
base_path = "https://discord.com/billing/partner-promotions/1180231712274387115/"
url = 'https://api.discord.gx.games/v1/direct-fulfillment'
payload = {
    "partnerUserId": "d05d65629f9b076a55c0661fcf7e9871bbf7052042d26b5185784d29f06081ab"
}

headers = {
    'authority': 'api.discord.gx.games',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.opera.com',
    'referer': 'https://www.opera.com/',
    'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'
}

def gen():
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 429:
        print("ratelimit")
        exit(0)
    token = response.json().get('token', 'No token found')
    link = base_path + token
    with open('links.txt', 'a') as file:
        file.write(link + "\n")

    print(link)

for i in range(QUANTITY):
    gen()
