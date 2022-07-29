from discord.ext import commands
import datetime
import re
import discord
from time import time as now
import asyncio

def time_str_to_dict(time_str):
    """Splits a time string into a dictionary of time units"""
    conv_dict = {
    'd': 'days',
    'h': 'hours',
    'm': 'minutes',
    's': 'seconds',
    }

    pat = r'[0-9]+[s|m|h|d]{1}'
    time_dict =  {conv_dict[p[-1]]: int(p[:-1]) for p in re.findall(pat, time_str)}
    return convert_dict_to_timedelta(time_dict)

def convert_dict_to_timedelta(time_dict):
    """Converts a time dictionary into a timedelta object"""
    return datetime.timedelta(**time_dict)
    


class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Predicates
    def isMod(ctx):
        mod_role = ctx.guild.get_role(753088662090023042)
        return mod_role in ctx.author.roles

    @commands.command()
    @commands.check(isMod)
    async def create_poll(self, ctx, time, *, question):

        # Get the unix timestamp of the time
        time = time_str_to_dict(time)

        # Add the current unix timestamp to the time
        time = round(now() + time.total_seconds())

        # Create the embed
        embed = discord.Embed(title='Poll', color=0x4287f5)
        embed.add_field(name=question, value=f'React with :white_check_mark: to vote yes and :x: to vote no\nEnds <t:{time}:R>', inline=False)

        # Send the embed
        message = await ctx.send(embed=embed)

        # Add the reactions
        check_emoji = '✅'
        x_emoji = '❌'

        await message.add_reaction(check_emoji)
        await message.add_reaction(x_emoji)
        await ctx.message.delete()

        # While loop to check if the time has passed
        while now() < time:
            await asyncio.sleep(1)
            pass

        # Get the reactions
        message = await ctx.fetch_message(message.id)
        reactions = message.reactions

        # Get the number of reactions
        check_reactions = reactions[0].count - 1
        x_reactions = reactions[1].count - 1

        # Remove the reactions
        await message.clear_reactions()

        # Create the results embed
        results_embed = discord.Embed(title='Poll Results', color=0x4287f5)
        results_embed.add_field(name=question, value=f'Yes: {check_reactions}\nNo: {x_reactions}\nAsked <t:{time}:R>', inline=False)

        # Edit the message
        await message.edit(embed=results_embed)


def setup(bot):
    bot.add_cog(Polls(bot))