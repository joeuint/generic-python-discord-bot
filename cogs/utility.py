import discord
import asyncio
import random
from captcha.image import ImageCaptcha
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Utility commands
    
    These are commands that are purely for utility purposes. (like verification, pinging, etc)
    """
    @commands.command()
    async def ping(self, ctx):
        # Return Pong with the latency of the bot
        await ctx.send('Pong! ' + str(round(self.bot.latency*1000, 1)) + 'ms')

    @commands.command()
    async def verify(self, ctx):
        VERIFIED_ROLE = self.bot.get_guild(753088484998119454).get_role(753088874661543988)

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
            msg = await self.bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author)
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

def setup(bot):
    bot.add_cog(Utility(bot))