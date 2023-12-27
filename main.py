import requests
import json
import random


DESIRED_LINKS_NUM = 100

# Sample proxies are given below. Only HTTP is necessary.
# To get your own proxies, check https://free-proxy-list.net/ 
PROXIES = (
    None,     # Direct connection.
    {'http': 'http://50.168.210.226:80'},
    {'http': 'http://50.218.57.68:80'}
)

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

BASE_PATH = "https://discord.com/billing/partner-promotions/1180231712274387115/"
BASE_URL = 'https://api.discord.gx.games/v1/direct-fulfillment'


def gen_link(proxy_idx, proxy_looped):
    """
    Generates and writes a Discord Nitro link to 'links.txt'.
    
    Args:
        (int) proxy_idx: The index of the proxy from which the generator should start.   
        (bool) proxy_looped: Whether or not all proxies have been used once.
    
    Returns:
        (int) gen_state: state in which function finished: 0, 1 or 2.
            0: no link added,
            1: link added,
            2: no link added and rate limited, 
        (int) proxy_idx: The index of the proxy on which the generator finished.
        (bool) proxy_looped: Whether or not all proxies have been used once.
    """
    gen_state = 0

    # Generates 64 character hex code to circumvent partnerUserId restriction.
    hex_code = ''.join(random.choice('0123456789abcdef') for n in range(64))

    payload = {
        "partnerUserId": f"{hex_code}"
    }

    # Proxy rotation.
    proxy_valid = False

    while not proxy_valid:
    
        if proxy_idx == len(PROXIES):
            proxy_idx = 0
            proxy_looped = True
        
        response = requests.post(BASE_URL, json=payload, headers=HEADERS, proxies=PROXIES[proxy_idx])

        # Handles rate limiting
        if response.status_code == 429:
            print("429 Too Many Requests: ", end='')
            
            if proxy_looped:
                print("All proxies rate limited.")
                gen_state = 2
                return gen_state, proxy_idx, proxy_looped

            print("Trying a different proxy.")
            proxy_idx += 1
            continue
            
        proxy_valid = True

    # Checks for successful response.
    if response.status_code // 100 == 2:
        try:
            token = response.json().get('token', 'No token found')
            link = BASE_PATH + token
            
            with open('links.txt', 'a') as file:
                file.write(link + "\n")
                
            print(f"Nitro link '...{link[108:138]}...' written.")
            gen_state = 1
        except json.JSONDecodeError:
            print("JSONDecodeError: Unable to parse response as JSON.")
            print("Response text:", response.text)
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            
    elif response.status_code == 504:
        print("504 Gateway Timeout: Servers experiencing high traffic. Trying again.")
        gen_state, proxy_idx, proxy_looped = gen_link(proxy_idx, proxy_looped)
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response text:", response.text)
    
    return gen_state, proxy_idx, proxy_looped


# UI start.
with open('links.txt') as file:
    line_count = 0
    for line in file:
        line_count += 1

print(f"'links.txt' starting with {line_count} links.")

proxy_idx = 0
proxy_looped = False

added_lines = 0

for link_num in range(DESIRED_LINKS_NUM):
    print(f"{link_num+1}. ", end='')
    gen_state, proxy_idx, proxy_looped = gen_link(proxy_idx, proxy_looped)
    
    if gen_state == 2:
        print("Program stopping. Try adding more proxies to PROXIES to avoid rate limiting.")
        break
    else:
        added_lines += gen_state

print(f"'links.txt' finishing with {line_count + added_lines} links ({added_lines} added).")
