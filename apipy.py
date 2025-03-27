import json
from logger import *
def get_gemini_api_key():
    try:
        with open('.apikeys.json', 'r') as f:
            data = json.load(f)
            return data['apiKeys']['Gemini-flash-2.0']
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        logger("bad", f"Error reading API key: {e}")
        return None

def get_Gimg_apikey():
    try:
        with open('.apikeys.json', 'r') as f:
            data = json.load(f)
            global cse
            cse = "55612e53d0e624367"
            return data['apiKeys']['Google-images']
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        logger("bad", f"Error reading API key: {e}")
        return None

def get_tenor_apikey():
    try:
        with open('.apikeys.json', 'r') as f:
            data = json.load(f)
            return data['apiKeys']['Tenor']
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        logger("bad", f"Error reading API key: {e}")
        return None