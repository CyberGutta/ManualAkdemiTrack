import time
import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def save_cookies_to_files(cookies):
    """Save cookies to both JSON and TXT files"""
    
    # Save as JSON file
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f, indent=2)
    print("Cookies saved to cookies.json")
    
    # Save as TXT file (cookie string format)
    cookie_dict = {c['name']: c['value'] for c in cookies}
    cookie_string = '; '.join([f"{name}={value}" for name, value in cookie_dict.items()])
    
    with open('cookies.txt', 'w') as f:
        f.write(cookie_string)
    print("Cookies saved to cookies.txt")
    
    return cookie_dict, cookie_string


def load_cookies_from_json():
    """Load cookies from JSON file if it exists"""
    if os.path.exists('cookies.json'):
        with open('cookies.json', 'r') as f:
            cookies = json.load(f)
        print("Cookies loaded from cookies.json")
        return cookies
    return None


def load_cookies_from_txt():
    """Load cookies from TXT file if it exists"""
    if os.path.exists('cookies.txt'):
        with open('cookies.txt', 'r') as f:
            cookie_string = f.read().strip()
        print("Cookies loaded from cookies.txt")
        return cookie_string
    return None


def get_fresh_cookies():
    """Get fresh cookies by logging in through browser"""
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
    
    return cookies


def main():
    # Try to load existing cookies first
    print("Checking for existing cookies...")
    
    cookies = load_cookies_from_json()
    
    if cookies is None:
        print("No existing cookies found. Getting fresh cookies...")
        cookies = get_fresh_cookies()
        cookie_dict, cookie_string = save_cookies_to_files(cookies)
    else:
        print("Using existing cookies...")
        cookie_dict = {c['name']: c['value'] for c in cookies}
        cookie_string = '; '.join([f"{name}={value}" for name, value in cookie_dict.items()])

    # Try to find JSESSIONID
    jsessionid_cookie = cookie_dict.get('JSESSIONID', '')
    print(f"JSESSIONID: {jsessionid_cookie}")

    # Construct the URL
    url = "https://iskole.net/iskole_elev/rest/v0/VoTimeplan_elev_oppmote?finder=RESTFilter;fylkeid=00,planperi=2025-26,skoleid=312&onlyData=true&limit=99&offset=0&totalResults=true"

    # Headers
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

    # Send the GET request using the cookies
    print("Making API request...")
    response = requests.get(url, headers=headers)

    # Print the response
    print("Response status code:", response.status_code)
    
    if response.status_code == 200:
        print("Request successful!")
        print("Response content:")
        print(response.text)
    elif response.status_code == 401 or response.status_code == 403:
        print("Authentication failed. Cookies might be expired.")
        print("Deleting old cookies and getting fresh ones...")
        
        # Delete old cookie files
        if os.path.exists('cookies.json'):
            os.remove('cookies.json')
        if os.path.exists('cookies.txt'):
            os.remove('cookies.txt')
        
        # Get fresh cookies and try again
        cookies = get_fresh_cookies()
        cookie_dict, cookie_string = save_cookies_to_files(cookies)
        
        # Update headers with new cookies
        headers["Cookie"] = cookie_string
        
        # Try the request again
        print("Retrying with fresh cookies...")
        response = requests.get(url, headers=headers)
        print("Response status code:", response.status_code)
        print("Response content:")
        print(response.text)
    else:
        print(f"Unexpected response code: {response.status_code}")
        print("Response content:")
        print(response.text)


if __name__ == "__main__":
    main()