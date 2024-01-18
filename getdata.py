import os
from dotenv import load_dotenv
from urllib.parse import urljoin
import requests
import time
import json

# Load environment variables from the .env file
load_dotenv()


def get_access_token(username, password):
    auth_url = "https://api.rated.network/v0/auth/token"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    response = requests.post(auth_url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json().get("accessToken")
        return access_token
    else:
        print(f"Error getting access token: {response.status_code}")
        return None


def fetch_data(api_url, access_token):
    headers = {
        "accept": "application/json",
        "X-Rated-Network": "mainnet",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        process_data(data)

        # Check if there's more data
        next_url = data.get("next")

        # Use urljoin to construct the full URL
        api_url = urljoin(api_url, next_url) if next_url else None

        return api_url

    else:
        print(f"Error: {response.status_code}")
        return None


def process_data(data):
    # for item in data.get('data', []):
    #     print(f"Item: {item}")

    # Pretty print the data to the console
    print("Response:")
    print(json.dumps(data, indent=2))

    with open("output_data.json", "a") as json_file:
        json.dump(data, json_file)
        json_file.write("\n")


# Get the username and password from environment variables
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Check if both username and password are available
if username is not None and password is not None:
    # Get the access token
    # access_token = get_access_token(username, password)
    access_token = os.getenv("API_KEY")

    if access_token:
        # Set the initial API URL
        api_url = "https://api.rated.network/v0/eth/operators?window=30d&poolType=all&idType=poolShare&size=100"

        while api_url:
            # Fetch data from the current URL
            api_url = fetch_data(api_url, access_token)

            # Wait for 0.8 seconds between requests to comply with the rate limit
            time.sleep(5)
else:
    print(
        "Error: Missing username or password. Make sure to set them in the .env file."
    )
