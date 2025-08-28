import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# Set up Selenium with Chrome
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open the student login page
driver.get("https://iskole.net/elev/?ojr=login")

print("The browser is now open. Please complete the login process manually (e.g., via Feide).")
print("After successful login, navigate to the relevant page if needed, then come back here and press Enter.")

# Wait for user to login manually
input("Press Enter once you have logged in...")

# Optionally, navigate to the referer page to ensure session is active
driver.get("https://iskole.net/elev/?isFeideinnlogget=true&ojr=fravar")
time.sleep(2)  # Give it a moment to load

# Extract all cookies from the browser
cookies = driver.get_cookies()

# Close the browser
driver.quit()

# Construct cookie string for requests
cookie_dict = {c['name']: c['value'] for c in cookies}
cookie_string = '; '.join([f"{name}={value}" for name, value in cookie_dict.items()])

# Try to find JSESSIONID
jsessionid_cookie = cookie_dict.get('JSESSIONID', '')

# Construct the URL without ;jsessionid first
url = "https://iskole.net/iskole_elev/rest/v0/VoTimeplan_elev_oppmote?finder=RESTFilter;fylkeid=00,planperi=2025-26,skoleid=312&onlyData=true&limit=99&offset=0&totalResults=true"

# If you want to try with ;jsessionid, uncomment the next line
# url = f"https://iskole.net/iskole_elev/rest/v0/VoTimeplan_elev_oppmote;jsessionid={jsessionid_cookie}?finder=RESTFilter;fylkeid=00,planperi=2025-26,skoleid=312&onlyData=true&limit=99&offset=0&totalResults=true"

# Headers (same as before, but Cookie will be set dynamically)
headers = {
    "Host": "iskole.net",
    "Cookie": cookie_string,
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Accept-Language": "no-NB",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Sec-Ch-Ua": "\"Chromium\";v=\"139\", \"Not;A=Brand\";v=\"99\"",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://iskole.net/elev/?isFeideinnlogget=true&ojr=fravar",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=4, i",
    "Connection": "keep-alive"
}

# Send the GET request using the extracted cookies
response = requests.get(url, headers=headers)

# Print the response
print("Response status code:", response.status_code)
print("Response content:")
print(response.text)

# If the above doesn't work (e.g., session not recognized), try the version with ;jsessionid appended to the URL.
# You may need to experiment if the full jsessionid requires an additional timestamp part.
# The jsessionid in the URL is typically found by inspecting network requests in your browser's dev tools after login.
# Look for requests to /rest/v0/... and copy the ;jsessionid=... part from the URL.