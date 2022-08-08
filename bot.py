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

# Replit
try:
    import alive
    alive.keep_alive()
    print("I am alive!")
except:
    print("keep_alive() not found")

VERSION = "1.2.0"

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

# Import welcome Cog
bot.load_extension('cogs.welcome')

# Import utility commands
bot.load_extension('cogs.utility')

# Import moderation commands
bot.load_extension('cogs.moderation')

# Import fun commands
bot.load_extension('cogs.fun')

# Import polls commands
bot.load_extension('cogs.polls')

# Error handling
@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That command does not exist')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required argument')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permission to use that command')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send('You do not have permission to use that command')
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send('This command is on cooldown, please try again later')
    else:
        await ctx.send('An error has occured')

# Run the bot
bot.run(TOKEN)