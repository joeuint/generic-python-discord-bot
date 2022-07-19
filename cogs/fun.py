from discord.ext import commands
import discord
import requests
import random

from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # 8ball command
    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx):
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
    @commands.command()
    @commands.cooldown(5, 30, commands.BucketType.user)
    async def cat(self, ctx):
        cat_api = 'https://aws.random.cat/meow'

        await ctx.send(f'{requests.get(cat_api).json()["file"]}')

def setup(bot):
    bot.add_cog(Fun(bot))