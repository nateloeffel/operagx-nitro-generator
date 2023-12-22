import requests
import json
import random


DESIRED_LINKS_NUM = 50

BASE_PATH = "https://discord.com/billing/partner-promotions/1180231712274387115/"
BASE_URL = 'https://api.discord.gx.games/v1/direct-fulfillment'

HEADERS = {
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

PROXIES = {
    # Placeholder for avoiding rate limiting
}


def gen():
    # Generates 64 character hex code to circumvent partnerUserId restriction
    hex_code = ''.join(random.choice('0123456789abcdef') for n in range(64))

    payload = {
        "partnerUserId": f"{hex_code}"
    }
    
    link_added = 0
    rate_limited = 0
    
    response = requests.post(BASE_URL, json=payload, headers=HEADERS)

    # Handles rate limiting
    if response.status_code == 429:
        print("429 Too Many Requests: Program has been rate limited.")
        rate_limited = 1
        return link_added, rate_limited
        
    # Checks for successful response
    if response.status_code // 100 == 2:
        try:
            token = response.json().get('token', 'No token found')
            link = BASE_PATH + token
            with open('links.txt', 'a') as file:
                file.write(link + "\n")
            print(f"Nitro link '...{link[108:138]}...' written.")
            link_added = 1
        except json.JSONDecodeError:
            print("JSONDecodeError: Unable to parse response as JSON.")
            print("Response text:", response.text)
        except Exception as e:
            print("An unexpected error occurred:", str(e))
    elif response.status_code == 504:
        print("504 Gateway Timeout: Servers experiencing high traffic.")
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response text:", response.text)
    
    return link_added, rate_limited


# UI start
with open('links.txt') as file:
    line_count = 0
    for line in file:
        line_count += 1

print(f"'links.txt' starting with {line_count} links.")

added_lines = 0
rate_limited = 0

for i in range(DESIRED_LINKS_NUM):
    print(f"{i+1}. ", end='')
    link_added, rate_limited = gen()
    if rate_limited:
        break
    added_lines += link_added

print(f"'links.txt' finishing with {line_count + added_lines} links.")
