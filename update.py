import os
import requests
import zipfile
import io
import shutil
import json

def logger(arg1, arg2): # Simple logger for the update script
    print(f"[UPDATE] {arg1.upper()}: {arg2}")

def get_github_apikey():
    try:
        with open('.apikeys.json', 'r') as f:
            data = json.load(f)
            return data['apiKeys']['github']
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        logger("bad", f"Error reading GitHub API key: {e}")
        return None

def download_and_replace(repo_owner, repo_name):
    """Downloads the latest release from GitHub, replaces vcbs.py, and keeps other files."""
    github_token = get_github_apikey()
    try:
        # 1. Get the latest release information
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        headers = {}
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        release_info = response.json()
        zipball_url = release_info["zipball_url"]

        # 2. Download the zip file
        logger("log", f"Downloading zip file from {zipball_url}")
        response = requests.get(zipball_url, stream=True, headers=headers)
        response.raise_for_status()

        # 3. Extract the zip file
        logger("log", "Extracting zip file")
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))

        # Determine the root directory within the zip file
        root_dir = zip_file.namelist()[0]  # Assumes the first entry is the root directory

        # 4. Replace vcbs.py and keep other files
        logger("log", "Replacing vcbs.py and keeping other files")
        for file in zip_file.namelist():
            # Extract files to the current directory, stripping the root directory
            target_path = os.path.join(os.getcwd(), file.replace(root_dir, '', 1).lstrip('/'))

            if file.endswith("vcbs.py"):
                # Extract and replace vcbs.py
                logger("log", f"Extracting and replacing: {file}")
                with zip_file.open(file) as source, open("vcbs.py", "wb") as target:
                    shutil.copyfileobj(source, target)
            elif not os.path.exists(target_path):
                # Extract other files only if they don't already exist
                logger("log", f"Extracting new file: {file}")
                with zip_file.open(file) as source, open(target_path, "wb") as target:
                    shutil.copyfileobj(source, target)
            else:
                logger("log", f"Skipping existing file: {file}")

        logger("log", "Update complete!")

    except requests.exceptions.RequestException as e:
        logger("error", f"Request exception: {e}")
    except zipfile.BadZipFile as e:
        logger("error", f"Bad zip file: {e}")
    except KeyError as e:
        logger("error", f"Key error: {e}. Check the GitHub API response format.")
    except Exception as e:
        logger("error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    repo_owner = "Lietzen-py"  # Replace with the actual repository owner
    repo_name = "very-cool-bot"  # Replace with the actual repository name
    download_and_replace(repo_owner, repo_name)

os.system("python3 vcbs.py")
