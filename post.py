import requests

# Function to get public IP
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except Exception as e:
        print(f"Error getting IP: {e}")
        return "0.0.0.0"  # Fallback

# Data from the provided item (assuming one item; extend for multiple if needed)
item = {
    "Id": 1,
    "Fag": "PB3A STU",
    "Stkode": "PB",
    "KlTrinn": "3",
    "KlId": "A",
    "KNavn": "STU",
    "GruppeNr": "$",
    "Dato": "20250825",
    "Timenr": 21578207,
    "StartKl": "0900",
    "SluttKl": "0945",
    "UndervisningPaagaar": 1,
    "Typefravaer": None,
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

# IMPORTANT: Replace with your actual JSESSIONID and other session-specific values from your browser's dev tools
jsessionid = "VKXLQQhgAnLoHYo-t9jjGZEnuXK95QS-CQIZQJHZ2AsY1qazL7DR!854864944!NONE!1755756910843"
wl_authcookie = "SHWlp8NbyV45wfThqoUt"  # Replace if different
oracle_bmc_route = "5b77d0961fadf1e852bfbb189bcc11ebc314be12"  # Replace if different

url = f"https://iskole.net/iskole_elev/rest/v0/VoTimeplan_elev_oppmote;jsessionid={jsessionid}"

headers = {
    "Host": "iskole.net",
    "Cookie": f"X-Oracle-BMC-LBS-Route={oracle_bmc_route}; JSESSIONID={jsessionid.split('!')[0]}; _WL_AUTHCOOKIE_JSESSIONID={wl_authcookie}",
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
response = requests.post(url, json=payload, headers=headers)

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

# If you have multiple items, you can loop over them and send separate requests