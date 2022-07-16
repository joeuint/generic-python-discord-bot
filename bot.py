# TODO: Refactor commands into cogs
"""ATTENTION
The following code is only intended to be used for my server.
I am currently refactoring it to be more generic and reusable.
"""

# Import a the discord.py library
from discord.ext import commands
import discord

# Import other libraries
import requests
from dotenv import load_dotenv
from os import getenv
import asyncio
from captcha.image import ImageCaptcha
import random

VERSION = "1.1"

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

# Do when someone joins the server
@bot.event
async def on_member_join(member):
    # Create the embed
    embed=discord.Embed(title='Welcome', color=0x0dc609)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name=f'Welcome to the server, {member.name}#{member.discriminator}!', value='We hope you enjoy your stay ;)', inline=True)
    embed.set_footer(text='This is an automated welcome message')
    
    # DM the user
    await member.create_dm()
    await member.dm_channel.send(embed=embed)
    await member.dm_channel.send('Start the verification process by typing !verify in #verify')

    # Send the message to the welcome channel
    welcome_channel = bot.get_channel(753819624491057174)
    await welcome_channel.send(embed=embed)
    print(f'{member.name} ({member.id}) has joined {member.guild.name} ({member.guild.id})')

# Print when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


class Utility:
    """Utility commands
    
    These are commands that are purely for utility purposes. (like verification, pinging, etc)
    """
    @bot.command()
    async def ping(ctx):
        # Return Pong with the latency of the bot
        await ctx.send('Pong! ' + str(round(bot.latency*1000, 1)) + 'ms')

    @bot.command()
    async def verify(ctx):
        VERIFIED_ROLE = bot.get_guild(753088484998119454).get_role(753088874661543988)

        # Check if the user is already verified
        if VERIFIED_ROLE in ctx.author.roles:
            await ctx.send('You are already verified!')
            return

        # Delete the user's message
        await ctx.message.delete()

        # DM the user
        dm = await ctx.author.create_dm()
        await dm.send('Looks like you are ready to verify!\nPlease type the captcha below to verify your account. Note: Only lowercase letters and digits are allowed.')

        # Define a character set excluding ambiguous characters
        char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '2', '3', '4', '5', '6', '7', '8', '9']

        # Generate a random string'
        code = ''.join(random.choices(char_list, k=6))
        print(code)

        # Create the captcha
        image = ImageCaptcha(width=400, height=100)

        # DM the user with the captcha
        await dm.send(file=discord.File(image.generate(code), 'captcha.png'))

        # Get the user's input
        try:
            msg = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await dm.send('You took too long to type the captcha. Please try again.')
            print(f'{ctx.author.name} ({ctx.author.id}) has failed to verify')
            return

        # Check if the user's input is correct
        if msg.content == code:
            # Send them a DM and add the verified role
            await dm.send('You have been verified!')
            print(f'{ctx.author.name} ({ctx.author.id}) has been verified')
            await ctx.author.add_roles(VERIFIED_ROLE)
        else:
            # Send them a DM and tell them they failed
            await dm.send('Incorrect captcha. Please try again.')
            print(f'{ctx.author.name} ({ctx.author.id}) has failed to verify')

class Moderation:
    """Moderation Commands
    
    These are commands that are used to assist moderators and administrators moderate the server and keep it safe
    """
    # Create a predicate to check if the user is the server owner
    def is_owner(ctx):
        return ctx.author.id == ctx.guild.owner.id

    # Create a predicate to check if the user is an adminisrator
    def is_admin(ctx):
        return ctx.author.guild_permissions.administrator

    # Create a predicate to check if the user is a moderator
    def is_mod(ctx):
        mod_role = bot.get_guild(753088484998119454).get_role(753088662090023042)
        return mod_role in ctx.author.roles

    # Eval command
    @bot.command()
    @commands.check(is_owner)
    async def eval(ctx, *, code: str):
        # WARNING: EVAL IS DANGEROUS AND SHOULD ONLY BE ALLOWED FOR USE BY THE SERVER OWNER! DO NOT TRUST RANDOM PEOPLE WITH THIS!
        try:
            result = eval(code)
            await ctx.send(f'```py\n{result}\n```')
        except Exception as e:
            await ctx.send(f'```py\n{e}\n```')
    
    # Ban command
    @bot.command()
    @commands.check(is_admin)
    async def ban(ctx, member: discord.Member, *, reason: str):
        # Ban the user
        await member.ban(reason=reason + f' ({ctx.author.name}#{ctx.author.discriminator})')
        await ctx.send(f'{member.name} has been banned for {reason}')
        print(f'{member.name} has been banned for {reason}')

    # Unban command
    @bot.command()
    @commands.check(is_admin)
    async def unban(ctx, *, id: int):
        # Get the banned user
        user = await bot.fetch_user(id)

        # Unban the user
        await ctx.guild.unban(user)

    # Clear command
    @bot.command()
    @commands.check(is_mod or is_admin)
    async def clear(ctx, amount: int):
        # Delete the specified amount of messages
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'Cleared {amount} messages')
        print(f'Cleared {amount} messages')

    # Kick command
    @bot.command()
    @commands.check(is_mod or is_admin)
    async def kick(ctx, member: discord.Member, *, reason: str):
        # Kick the user
        await member.kick(reason=reason + f' ({ctx.author.name}#{ctx.author.discriminator})')
        await ctx.send(f'{member.name} has been kicked for {reason}')
        print(f'{member.name} has been kicked for {reason}')
    
    # Slowmode command
    @bot.command()
    @commands.check(is_mod or is_admin)
    async def slowmode(ctx, seconds: int):
        # Set the slowmode
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f'Slowmode set to {seconds} seconds')
        print(f'Slowmode in {ctx.channel.name} set to {seconds} seconds')

    # Mute command
    @bot.command()
    @commands.check(is_mod or is_admin)
    async def mute(ctx, member: discord.Member, *, reason: str):
        # Mute the user
        await member.add_roles(ctx.guild.get_role(753342159444377611))
        await ctx.send(f'{member.name} has been muted for {reason}')
        print(f'{member.name} has been muted for {reason}')

    # Unmute command
    @bot.command()
    @commands.check(is_mod or is_admin)
    async def unmute(ctx, member: discord.Member):
        # Unmute the user
        await member.remove_roles(ctx.guild.get_role(753342159444377611))
        await ctx.send(f'{member.name} has been unmuted')
        print(f'{member.name} has been unmuted')

class Fun:
    """Fun Commands
    
    This class includes some fun commands for users to play with!
    """

    # 8ball command
    @bot.command(aliases=['8ball'])
    async def _8ball(ctx):
        responses = ['It is certain.',
                    'It is decidedly so.',
                    'Without a doubt.',
                    'Yes definitely.',
                    'You may rely on it.',
                    'As I see it, yes.',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    'Signs point to yes',
                    'Reply hazy, try again.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    'Don\'t count on it.',
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good.',
                    'Very doubtful.']
        await ctx.send(f'{random.choice(responses)}')

    # Cat command
    @bot.command()
    async def cat(ctx):
        cat_api = 'https://aws.random.cat/meow'

        await ctx.send(f'{requests.get(cat_api).json()["file"]}')

# Run the bot
bot.run(TOKEN)