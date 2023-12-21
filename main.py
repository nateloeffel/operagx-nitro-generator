import requests
import json
import random

QUANTITY = 2
base_path = "https://discord.com/billing/partner-promotions/1180231712274387115/"
url = 'https://api.discord.gx.games/v1/direct-fulfillment'

# Generates 64 character hex code to circumvent partnerUserId restriction
hex_code = ''.join(random.choice('0123456789abcdef') for n in range(64))

payload = {
    "partnerUserId": f"{hex_code}"
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

    # Handling rate limiting
    if response.status_code == 429:
        print("Rate limited")
        exit(0)

    # Checking for successful response
    if response.status_code // 100 == 2:
        try:
            token = response.json().get('token', 'No token found')
            link = base_path + token
            with open('links.txt', 'a') as file:
                file.write(link + "\n")
            print(link)
        except json.JSONDecodeError:
            print("JSONDecodeError: Unable to parse response as JSON.")
            print("Response text:", response.text)
        except Exception as e:
            print("An unexpected error occurred:", str(e))
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response text:", response.text)

for i in range(QUANTITY):
    gen()
