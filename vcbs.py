import sys # importing basic modules
import os
os.system("pip install -r requirements.txt")
import base64
import encodings
import json
import discord # type: ignore
from discord.ext import commands  # type: ignore | borrowing this from whirl
from colorama import Fore, Back, Style # type: ignore
# non required
import random # type: ignore
from cryptography.fernet import Fernet # type: ignore
import requests
from google import genai
import time
print("loading Logger...")
from logger import logger
from extensionlib import *
from apipy import *
import importlib.util
aikey = get_gemini_api_key()
imgkey = get_Gimg_apikey()
gifkey = get_tenor_apikey()

def extensions(base_path="extensions"):
    extensions = {}
    for root, dirs, files in os.walk(base_path):
        if "main.py" in files:  # Check if 'main.py' exists in the current folder
            main_file = os.path.join(root, "main.py")
            module_name = find_extension_info(os.path.join(root, "index.json"), "name")  # Use the name from index.json

            # Dynamically load the module
            spec = importlib.util.spec_from_file_location(module_name, main_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Set the main() function to the name of the extension
            if hasattr(module, "main"):
                extensions[module_name] = module.main
                logger("extension", f"Loaded extension '{module_name}' with main() function.")
            else:
                logger("extension", f"Loaded extension '{module_name}' but no 'main()' function found.")

    return extensions

extensions_ = extensions()

# call extensions with loaded_extensions["Extension"]()

logger('debug', f"extensions found: {extensions}")
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

version = 1.0
channel = "public_beta"
update_name = "The Extension Update"

def update_bot(user, init):
    logger("command",f"{user} initiated an update, from {init}") # we check on github for a updated version
    try:
        global latest_version
        global e
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
            return f"A new version is available! Current version: {version}, Latest version: {latest_version}. "

        else:
            return "<:ActionDone:1351392427637739633> You are already running the latest version."
    except requests.exceptions.RequestException as e:
        return f" <:ActionNotDone:1351396510054617210> Error checking for updates: {e}"
    except KeyError:
        return "<:ActionNotDone:1351396510054617210> Error parsing release information from GitHub."


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
async def rgif(ctx: discord.ApplicationContext, query: discord.Option(str, "choose what topic of gif")): # type: ignore
    await ctx.defer()
    gif_url = get_tenor_gif(query)
    await ctx.followup.send(gif_url)

@bot.slash_command(name="ask", description="Ask gemini 2.0 a question")
async def askai(ctx: discord.ApplicationContext, prompt: discord.Option(str, "Prompt for gemini")): # type: ignore
    await ctx.defer()
    gemini_response = ask_gemini(str(prompt))
    if len(gemini_response) > 2000:
        truncated_response = gemini_response[:1997] + "..."  # Truncate and add ellipsis
        await ctx.respond(truncated_response)
    else:
        await ctx.respond(f"{gemini_response}")
@bot.slash_command(name="image", description="get a certain image from google")
async def image(ctx: discord.ApplicationContext, query: discord.Option(str, "What to search for")): # type: ignore
    await ctx.defer()
    image_url = get_gimg(query)
    await ctx.followup.send(image_url)

@bot.slash_command(name="update", description="check for a update")
async def update(ctx: discord.ApplicationContext):
    await ctx.defer()  # Acknowledge the interaction immediately
    init = f"{ctx.guild}, {ctx.channel}"
    update_message = update_bot(ctx.author, init)
    await ctx.followup.send(update_message)
    if "A new version is available!" in update_message:
        os.system("python3 update.py")

@bot.command()
async def remoji(ctx):
    random_number = random.randint(0, len(emojis) - 1)
    emoji = get_emoji(random_number)
    await ctx.send(emoji)
    logger("command", f"{ctx.author} used $remoji")

from discord.commands import SlashCommandGroup

import datetime
async def schedule_message():
    target_user_id = 944722638624948315  # The user ID to send the message to
    target_date = datetime.date(datetime.date.year, 3, 22)  # The specific date (Year, Month, Day)

    while True:
        # Get the current date
        current_date = datetime.date.today()

        # Check if the current date matches the target date
        if current_date == target_date:
            user = await bot.fetch_user(target_user_id)  # Fetch the user by ID
            if user:
                try:
                    await user.send("Happy Birthday Suchanub!\n-#this message was customized by <@903468085099520000>")  # Send the message
                    logger("log", f"Message sent to user {user.id} on {target_date}.")
                except Exception as e:
                    logger("bad", f"Failed to send message to user {user.id}: {e}")
            break  # Exit the loop after sending the message

        # Wait for 24 hours before checking again
        await time.sleep(86400)

# Define the badmin group
badmin = SlashCommandGroup("badmin", "Bad Admin tools")

@badmin.command(name="timeout", description="Timeout somebody")
async def timeout(ctx: discord.ApplicationContext, member: discord.Member, reason: str = "No reason provided"):
    if not ctx.guild.me.guild_permissions.moderate_members:
        await ctx.respond("I don't have permission to Timeout members.", ephemeral=True)
        logger("mod", f"bot doesnt have perms for that")
        return
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.respond("You dont have the permission to Timeout members, this has been logged", ephemeral=True)
        logger("mod", f"{ctx.author} tried to use /Timeout on {member} for {reason}, watch for future attempts")
        return
    
    print("placeholder")

# Add the ban command to the badmin group
@badmin.command(name="ban", description="Ban someone")
async def ban(ctx: discord.ApplicationContext, member: discord.Member, reason: str = "No reason provided"):
    # Check if the bot has permission to ban members
    if not ctx.guild.me.guild_permissions.moderate_members:
        await ctx.respond("I don't have permission to ban members.", ephemeral=True)
        logger("mod", f"bot doesnt have perms for that")
        return
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.respond("You dont have the permission to ban members, this has been logged", ephemeral=True)
        logger("mod", f"{ctx.author} tried to use /ban on {member} for {reason}, watch for future attempts")
        return
    # Ban the member
    await member.ban(reason=reason)
    await ctx.respond(f"Banned {member.mention} for reason: {reason}")
    logger("mod", f"User {member} banned for {reason}")

# Register the badmin group with the bot
bot.add_application_command(badmin)

firefly = SlashCommandGroup(
    "firefly",
    "A set of commands for the guild, FireFly",
    guild_ids=[1333588480948703322]  # Replace with your guild ID
)

@firefly.command(name="getoslink", description="Gets the latest build of FireFly / Lightning")
async def getlink(ctx: discord.ApplicationContext,
                  version: discord.Option(str, choices=['lightning', 'firefly'])): # type: ignore
    from gfs import getlatestbuild
    await ctx.respond(f"{getlatestbuild(version, 'tw')}")

@firefly.command(name="getoslinkdwnld", description="Gets the latest build and downloads it")
async def getdwnld(ctx: discord.ApplicationContext,
                   version: discord.Option(str, choices=['lightning', 'firefly'])): # type: ignore
    from gfs import getlatestbuild
    try:
        # Get the download link
        download_link = getlatestbuild(version, 'dl')
        # Send the file to the channel
        await ctx.respond(file=discord.File(download_link))
    except Exception as e:
        await ctx.respond(f"An error occurred: {e}")


@firefly.command(name="putlightningintoitsplace", description="Yeah, you heard me.")
async def assertdominance(ctx: discord.ApplicationContext):
    await ctx.respond("<@1341152716583338084> is far less than the **POWER OF VERY COOL BOT**")


bot.add_application_command(firefly)
bot.run(token.decode('utf-8')) # run the bot with the decrypted token from line 72-
