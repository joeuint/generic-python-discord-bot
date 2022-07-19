# TODO: Refactor commands into cogs
"""ATTENTION
The following code is only intended to be used for my server.
I am currently refactoring it to be more generic and reusable.
"""

# Import a the discord.py library
from discord.ext import commands
import discord

# Import other libraries
from dotenv import load_dotenv
from os import getenv

VERSION = "1.1.5"

# Load .env file
load_dotenv()
TOKEN = getenv('BOT_TOKEN')

# Set intents
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True

# Create a bot instance
bot = commands.Bot(command_prefix='>', intents=intents)

# Print when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Import Welcome Cog
bot.load_extension('cogs.welcome')

# Import utility commands
bot.load_extension('cogs.utility')

# Import Moderation commands
bot.load_extension('cogs.moderation')

# Import fun commands
bot.load_extension('cogs.fun')

# Run the bot
bot.run(TOKEN)