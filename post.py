import requests
import json
import os

# Function to load cookies from cookies.json
def load_cookies(cookies_file="cookies.json"):
    try:
        if not os.path.exists(cookies_file):
            raise FileNotFoundError(f"Cookie file '{cookies_file}' not found")
        
        with open(cookies_file, 'r') as f:
            cookies_data = json.load(f)
        
        # Extract cookie values from the JSON structure
        cookies = {}
        for cookie in cookies_data:
            cookies[cookie['name']] = cookie['value']
        
        return cookies
    except Exception as e:
        print(f"Error loading cookies: {e}")
        return None

# Function to get public IP
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except Exception as e:
        print(f"Error getting IP: {e}")
        return "0.0.0.0"  # Fallback

# Load cookies from file
cookies = load_cookies()
if not cookies:
    print("Failed to load cookies. Exiting.")
    exit(1)

# Extract required cookie values
jsessionid = cookies.get('JSESSIONID')
wl_authcookie = cookies.get('_WL_AUTHCOOKIE_JSESSIONID')
oracle_bmc_route = cookies.get('X-Oracle-BMC-LBS-Route')

# Validate that required cookies are present
if not all([jsessionid, wl_authcookie, oracle_bmc_route]):
    print("Missing required cookies in cookies.json file")
    print(f"JSESSIONID: {'✓' if jsessionid else '✗'}")
    print(f"_WL_AUTHCOOKIE_JSESSIONID: {'✓' if wl_authcookie else '✗'}")
    print(f"X-Oracle-BMC-LBS-Route: {'✓' if oracle_bmc_route else '✗'}")
    exit(1)

# Data from the provided item (assuming one item; extend for multiple if needed)
item = {
    "Id": 1,
    "Fag": "PB3A STU",
    "Stkode": "PB",
    "KlTrinn": "3",
    "KlId": "A",
    "KNavn": "STU",
    "GruppeNr": "$",
    "Dato": "20250903",
    "Timenr": 21609421,
    "StartKl": "0900",
    "SluttKl": "0945",
    "UndervisningPaagaar": 1,
    "Typefravaer": "",
    "ElevForerTilstedevaerelse": 1,
    "Kollisjon": 1,
    "TidsromTilstedevaerelse": "09:00 - 09:15"
}

# Construct parameters based on the item and example
# Assuming 'M' for presence since Typefravaer is null (adjust if needed)
fravaerstype = "M" if item["Typefravaer"] is None else item["Typefravaer"]
ip = get_public_ip()

parameters = [
    {"fylkeid": "00"},  # Fixed from example
    {"skoleid": "312"},  # Fixed from example
    {"planperi": "2025-26"},  # Based on year
    {"ansidato": item["Dato"]},  # Use Dato from item
    {"stkode": item["Stkode"]},
    {"kl_trinn": item["KlTrinn"]},
    {"kl_id": item["KlId"]},
    {"k_navn": item["KNavn"]},
    {"gruppe_nr": item["GruppeNr"]},
    {"timenr": item["Timenr"]},
    {"fravaerstype": fravaerstype},
    {"ip": ip}
]

payload = {
    "name": "lagre_oppmote",
    "parameters": parameters
}

# Build URL with JSESSIONID (extract the part before the first '!' if present)
jsessionid_clean = jsessionid.split('!')[0] if '!' in jsessionid else jsessionid
url = f"https://iskole.net/iskole_elev/rest/v0/VoTimeplan_elev_oppmote;jsessionid={jsessionid}"

headers = {
    "Host": "iskole.net",
    "Cookie": f"X-Oracle-BMC-LBS-Route={oracle_bmc_route}; JSESSIONID={jsessionid_clean}; _WL_AUTHCOOKIE_JSESSIONID={wl_authcookie}",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Accept-Language": "nb-NO,nb;q=0.9",
    "Sec-Ch-Ua": "\"Chromium\";v=\"139\", \"Not;A=Brand\";v=\"99\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/vnd.oracle.adf.action+json",
    "Origin": "https://iskole.net",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://iskole.net/elev/?isFeideinnlogget=true&ojr=fravar",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=4, i",
    "Connection": "keep-alive"
}

# Send the POST request
print("Sending request with loaded cookies...")
response = requests.post(url, json=payload, headers=headers)

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

# If you have multiple items, you can loop over them and send separate requests