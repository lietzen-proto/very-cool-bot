import json
import os
import requests

def getlatestbuild(arg1, arg2):
    latestjson = "https://raw.githubusercontent.com/The-Firefly-Team/Firefly/refs/heads/web/Builds/LatestBuild.json"
    headers = {}
    response = requests.get(latestjson, headers=headers)

    # Check if the response is valid
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

    try:
        data = response.json()  # Attempt to parse the response as JSON
    except requests.exceptions.JSONDecodeError:
        raise Exception(f"Invalid JSON response: {response.text}")

    # Extract links from the JSON data
    try:
        LightningLink = data['Lightning']['link']
        Fireflylink = data['Firefly']['link']
    except KeyError as e:
        raise Exception(f"Missing expected key in JSON data: {e}")

    # Determine which link to return
    if arg1.lower() == "lightning":
        link = LightningLink
    elif arg1.lower() == "firefly":
        link = Fireflylink
    else:
        raise ValueError("Invalid argument. Use 'lightning' or 'firefly'.")

    if arg2 == "tw":
        latest = "https://turbowarp.org/?project_url=" + link
        return latest

    if arg2 == "dl":
        # Download the file and save it to a cache directory
        cache_dir = "cache"
        os.makedirs(cache_dir, exist_ok=True)  # Create the cache directory if it doesn't exist
        file_name = os.path.join(cache_dir, os.path.basename(link))

        with requests.get(link, stream=True, headers=headers) as download_response:
            download_response.raise_for_status()
            with open(file_name, "wb") as file:
                for chunk in download_response.iter_content(chunk_size=8192):
                    file.write(chunk)

        return file_name