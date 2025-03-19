import sys # importing basic modules
import os
import base64
import encodings
import json
os.system("echo off")
print("making sure you have thy dependencies installed") 
try:
    import discord # type: ignore
    import colorama # type: ignore
    from cryptography.fernet import Fernet # type: ignore
    import requests

except ImportError:
    print("dependencies not installed, installing now")
    import os
    os.system("pip install py-cord")
    os.system("pip install colorama")
    os.system("pip install cryptography")
    os.system("pip install requests")
    print("dependencies installed, remember to install dependencies next time dumbass")
import discord # type: ignore
from discord.ext import commands  # type: ignore | borrowing this from whirl
from colorama import Fore, Back, Style # type: ignore
# non required
import random # type: ignore
from cryptography.fernet import Fernet # type: ignore
import requests
from google import genai
print("loading Logger...")
def logger(arg1, arg2): # logger("log, debug, mod, command", "message") Supports F
    if arg1.lower() == "debug":
        status = Fore.GREEN + "[debug]".upper()
    if arg1.lower() == "log":
        status = Fore.LIGHTBLACK_EX + "[log]".upper()
    if arg1.lower() == "bad":
        status = Fore.RED + "[bad!]".upper()
    if arg1.lower() == "mod":
        status = Fore.CYAN + "[mod]".upper()
    if arg1.lower() == "command":
        status = Fore.LIGHTGREEN_EX + "[command]".upper()
    if arg1.lower() == "warn":
        status = Fore.YELLOW + "[warn]".upper()
    print(f"{status} {Fore.RESET} {arg2}")
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
            cse = data['apikeys']['cse']
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

aikey = get_gemini_api_key()
imgkey = get_Gimg_apikey()
gifkey = get_tenor_apikey()
def ask_gemini(prompt):
    try:
        client = genai.Client(api_key=aikey)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt)
        return str(response.text)
    except Exception as e:
        return f" <:ActionNotDone:1351396510054617210> Error from Gemini API: {e}"

def get_gimg(query):
    safe_search = "active"  # moderate: moderate safe search
    api_key = imgkey
    cse_id = cse
    query = query.strip()
    num = 1
    filter = "top"
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}&searchType=image&num={num}&safe={safe_search}"
    data = requests.get(url).json()
    try:
        imageurl = data["items"][0]["link"]
        return imageurl
    except Exception as e:
        return f" <:ActionNotDone:1351396510054617210> No image found for {query}"

def get_tenor_gif(query):
    api_key = gifkey
    search_term = query.strip()
    limit = 10  # Number of GIFs to retrieve
    url = f"https://tenor.googleapis.com/v2/search?q={search_term}&key={api_key}&limit={limit}&media_filter=gif"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data["results"]:
            random_gif = random.choice(data["results"])
            return random_gif["media_formats"]["gif"]["url"]
        else:
            return "No GIFs found for that query."
    except requests.exceptions.RequestException as e:
        return f"Error fetching GIF: {e}"

def get_github_apikey():
    try:
        with open('.apikeys.json', 'r') as f:
            data = json.load(f)
            return data['apiKeys']['github']
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        logger("bad", f"Error reading GitHub API key: {e}")
        return None

github_token = get_github_apikey()

version = 0.7
channel = "public_beta"
update_name = "the sentience update"

def update_bot(user, init):
    logger("command",f"{user} initiated an update, from {init}") # we check on github for a updated version
    try:
        # Replace 'YourUsername' and 'YourRepository' with your actual GitHub username and repository name
        github_api_url = "https://api.github.com/repos/Lietzen-py/very-cool-bot/releases/latest"
        headers = {}
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        response = requests.get(github_api_url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        release_info = response.json()
        latest_version = release_info["tag_name"]
        latest_release_url = release_info["html_url"]

        if latest_version > str(version):
            os.system("python3 update.py")
            return (
                f"A new version is available! Current version: {version}, Latest version: {latest_version}. "
                f" <:Actionpending:1351789321140699191> Downloading update!"
            )

        else:
            return " <:ActionDone:1351392427637739633> You are already running the latest version."
    except requests.exceptions.RequestException as e:
        return f" <:ActionNotDone:1351396510054617210> Error checking for updates: {e}"
    except KeyError:
        return " <:ActionNotDone:1351396510054617210> Error parsing release information from GitHub."


# Version info...


logger("warn", "Discord.py is installed! If you get a module error please report it to the bug tracker here [placeholder link]")

platversion = os.name
with open('emojis.json', 'r', encoding='utf-8') as f: # this is for the $remoji command
    data = json.load(f)
    emojis = data['emojis']

def get_emoji(number):
    # Check if the number is within the valid range
    if 0 <= number < len(emojis):
        return emojis[number]
    else:
        return "Invalid number"  # Or handle the error as you see fit

# Example usage:
# Get a random number
random_number = random.randint(0, len(emojis) - 1)

# Get the corresponding emoji
emoji = get_emoji(random_number)
logger("log", f"v{version}/{platversion}/{channel}: {update_name}")
logger("debug", "checking for token.dbt...") 
osusername = os.getlogin()
global token
if os.path.exists("token.dbt"):
    logger("log", "token.dbt found") # every token has a .key file that is used to decrypt its counterpart
    with open("token.dbt", "rb") as file:
     dtoken = file.read()
    if os.path.exists("key.key"):
        with open("key.key", "rb") as key_file:
            key = key_file.read()
            Fernet = Fernet(key)
            # decrypt token
            token = Fernet.decrypt(dtoken.decode())
            logger("log", "token decrypted")
    else:
        logger("bad", "key not found, please check the programs directory or regenerate your token")
        sys.exit()
else:
    logger("log", "token.dbt not found")
    token = input("enter your bot's token (this will get saved): ")
    with open("token.dbt", "wb") as file:
        global etoken
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        fernet = Fernet(key)
        etoken = fernet.encrypt(token.encode())
        file.write(etoken)
    logger("log", "token saved to token.dbt")
# time for thy main bot thingy
intents = discord.Intents.default() # Defining intents
intents.message_content = True # Adding the message_content intent so that the bot can read user messages
# / commands take a bit to sync, but after they sync they wont disappear
bot = commands.Bot(command_prefix="$", intents=intents)
@bot.event
async def on_ready():
    logger("log", f"{bot.user} is online.")

@bot.slash_command(name="info", description="see the bot's info")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond(f"```very cool bot, {version}, {update_name}, made by lietzen```")
    logger("command", f"{ctx.author} used /info")
@bot.slash_command(name="remoji", description="generates a random emoji")
async def remoji(ctx: discord.ApplicationContext):
    random_number = random.randint(0, len(emojis) - 1)
    emoji = get_emoji(random_number)
    await ctx.respond(emoji)
    logger("command", f"{ctx.author} used /remoji")
@bot.slash_command(name="rnumber", description="generates a random number 1-100")
async def rnumber(ctx: discord.ApplicationContext):
    await ctx.respond(f"you got... {random.randint(1, 100)}!")
    logger("command", f"{ctx.author} used /rnumber")

@bot.slash_command(name="yippee", description="sends the autism gif")
async def yippee(ctx: discord.ApplicationContext):
    await ctx.respond('https://media.discordapp.net/attachments/1216948285319938162/1343387298473050166/image0.gif?ex=67bd166a&is=67bbc4ea&hm=d8e6c194b8311d07ff8612990dc7b43727d75ea9992bcd9b019e0588919369ae&=')
    logger("command", f"{ctx.author} used /yippee")
# dice rolling starts here
@bot.slash_command(name="d4", description="roll a d4")
async def d6(ctx: discord.ApplicationContext):
    await ctx.respond(f'you rolled a {random.randint(1, 4)}')
    logger("command",f"{ctx.author} rolled a d4")

@bot.slash_command(name="d6", description="roll a d6")
async def d6(ctx: discord.ApplicationContext):
    await ctx.respond(f'you rolled a {random.randint(1, 6)}')
    logger("command",f"{ctx.author} rolled a d6")

@bot.slash_command(name="d8", description="roll a d8")
async def d6(ctx: discord.ApplicationContext):
    await ctx.respond(f'you rolled a {random.randint(1, 8)}')
    logger("command",f"{ctx.author} rolled a d8")

@bot.slash_command(name="d10", description="roll a d10")
async def d6(ctx: discord.ApplicationContext):
    await ctx.respond(f'you rolled a {random.randint(1, 10)}')
    logger("command",f"{ctx.author} rolled a d10")

@bot.slash_command(name="d12", description="roll a d12")
async def d6(ctx: discord.ApplicationContext):
    await ctx.respond(f'you rolled a {random.randint(1, 12)}')
    logger("command",f"{ctx.author} rolled a d12")

@bot.slash_command(name="d20", description="roll a d20")
async def d6(ctx: discord.ApplicationContext):
    await ctx.respond(f'you rolled a {random.randint(1, 20)}')
    logger("command",f"{ctx.author} rolled a d20")
# dice rolling ends here
@bot.slash_command(name="wtf", description="Use this when you are very horrified")
async def wtf(ctx: discord.ApplicationContext):
    await ctx.respond(f'{ctx.author} is very scared for their life.')
    logger("command", f"{ctx.author} was horrified")
@bot.slash_command(name="help", description="help command, lists other commands (even tho discord does this)")
async def help(ctx: discord.ApplicationContext):
    await ctx.respond('no.')

@bot.slash_command(name="selfdestruct", description="boom")
async def help(ctx: discord.ApplicationContext):
    await ctx.respond(':boom:')

@bot.slash_command(name="rgif", description="Picks a random gif from tenor")
async def rgif(ctx: discord.ApplicationContext, query: discord.Option(str, "choose what topic of gif")):
    await ctx.defer()
    await ctx.respond(f"{get_tenor_gif(query)}")

@bot.slash_command(name="ask", description="Ask gemini 2.0 a question")
async def askai(ctx: discord.ApplicationContext, prompt: discord.Option(str, "Prompt for gemini")):
    await ctx.defer()
    gemini_response = ask_gemini(str(prompt))
    if len(gemini_response) > 2000:
        truncated_response = gemini_response[:1997] + "..."  # Truncate and add ellipsis
        await ctx.respond(truncated_response)
    else:
        await ctx.respond(f"{gemini_response}")
@bot.slash_command(name="image", description="get a certain image from google")
async def image(ctx: discord.ApplicationContext, query: discord.Option(str, "What to search for")):
    await ctx.defer()
    image_url = get_gimg(query)
    await ctx.followup.send(image_url)

@bot.slash_command(name="update", description="check for a update")
async def update(ctx: discord.ApplicationContext):
    init = f"{ctx.guild}, {ctx.channel}"
    await ctx.respond(f"{update_bot(ctx.user, init)}")  # need to make this

@bot.command()
async def remoji(ctx):
    random_number = random.randint(0, len(emojis) - 1)
    emoji = get_emoji(random_number)
    await ctx.send(emoji)
    logger("command", f"{ctx.author} used $remoji")

bot.run(token.decode('utf-8')) # run the bot with the decrypted token from line 72

