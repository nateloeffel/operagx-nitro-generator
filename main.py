import requests
import json
import string

QUANTITY = 2
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

    # Handling rate limiting
    if response.status_code == 429:
        print("Rate limited")
        return False

    # Checking for successful response
    if response.status_code // 100 == 2:
        try:
            token = response.json().get('token', 'No token found')
            link = base_path + token

            # Write the link to the file 'nitrolinks.txt'
            with open('nitrolinks.txt', 'a') as file:
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

    return True

rate_limit_count = 0
while rate_limit_count < 5:
    if not gen():
        rate_limit_count += 1
    else:
        rate_limit_count = 0


for i in range(QUANTITY):
    gen()
