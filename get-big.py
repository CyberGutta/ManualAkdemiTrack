import requests
import json
import os

def load_cookies_from_file(file_path="cookies.json"):
    """Load cookies from JSON file and convert to requests-compatible format"""
    try:
        with open(file_path, 'r') as f:
            cookies_data = json.load(f)
        
        # Convert to simple name:value dictionary for requests
        cookies = {}
        for cookie in cookies_data:
            cookies[cookie['name']] = cookie['value']
        
        return cookies
    except FileNotFoundError:
        print(f"Error: {file_path} not found!")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}")
        return None

def make_iskole_request(start_date="20250901", end_date="20250907"):
    """Make request to iskole API with cookies"""
    
    # Load cookies from file
    cookies = load_cookies_from_file()
    if not cookies:
        return None
    
    # Base URL and parameters
    base_url = "https://iskole.net/iskole_elev/rest/v0/VoTimeplan_elev"
    
    # Parameters from the original request
    params = {
        'finder': 'RESTFilter;fylkeid=00,planperi=2025-26,skoleid=312,startDate=' + start_date + ',endDate=' + end_date,
        'onlyData': 'true',
        'limit': '1000',
        'totalResults': 'true'
    }
    
    # Headers from the original request
    headers = {
        'Host': 'iskole.net',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept-Language': 'no-NB',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Sec-Ch-Ua': '"Not)A;Brand";v="8", "Chromium";v="138"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://iskole.net/elev/?isFeideinnlogget=true&ojr=timeplan',
        'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=1, i',
        'Connection': 'keep-alive'
    }
    
    try:
        # Make the GET request
        response = requests.get(base_url, params=params, headers=headers, cookies=cookies)
        
        # Check if request was successful
        if response.status_code == 200:
            print("Request successful!")
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def main():
    """Main function to run the program"""
    print("Making request to iskole API...")
    
    # You can customize the date range here
    start_date = "20250901"  # YYYYMMDD format
    end_date = "20250907"    # YYYYMMDD format
    
    # Make the request
    data = make_iskole_request(start_date, end_date)
    
    if data:
        print("\nData received successfully!")
        print(f"Response type: {type(data)}")
        
        # Pretty print the JSON response
        print("\nResponse data:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Optionally save to file
        save_to_file = input("\nDo you want to save the response to a file? (y/n): ")
        if save_to_file.lower() == 'y':
            filename = f"timeplan_{start_date}_to_{end_date}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {filename}")
    else:
        print("Failed to retrieve data.")

if __name__ == "__main__":
    main()