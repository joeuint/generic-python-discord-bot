import discord
from discord.ext import commands
from time import sleep
from aioconsole import aexec

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Moderation Commands
    
    These are commands that are used to assist moderators and administrators moderate the server and keep it safe
    """
    # Check if the user is the bot owner
    def is_bot_owner(ctx):
        return ctx.author.id == 457910942114512930

    # Create a predicate to check if the user is the bot owner
    def is_owner(ctx):
        return ctx.author.id == ctx.guild.owner.id

    # Create a predicate to check if the user is an adminisrator
    def is_admin(ctx):
        return ctx.author.guild_permissions.administrator

    # Create a predicate to check if the user is a moderator
    def is_mod(ctx):
        mod_role = ctx.guild.get_role(753088662090023042)
        return mod_role in ctx.author.roles

    # Eval command
    @commands.command(name='eval', hidden=True)
    @commands.check(is_bot_owner)
    async def _eval(self, ctx, *, body: str):
        # Variables for the exec command
        localVariables = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message
        }
        # Execute the code
        try:
            await aexec(body, localVariables)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await ctx.send(f'```py\n{e}```')
    
    # Ban command
    @commands.command()
    @commands.check(is_admin)
    async def ban(self, ctx, member: discord.Member, *, reason: str):
        # Ban the user
        await member.ban(reason=reason + f' ({ctx.author.name}#{ctx.author.discriminator})')
        await ctx.send(f'{member.name} has been banned for {reason}')
        print(f'{member.name} has been banned for {reason}')

    # Unban command
    @commands.command()
    @commands.check(is_admin)
    async def unban(self, ctx, *, id: int):
        # Get the banned user
        user = await self.bot.fetch_user(id)

        # Unban the user
        await ctx.guild.unban(user)

    # Clear command
    @commands.command()
    @commands.check(is_mod or is_admin)
    async def clear(self, ctx, amount: int):
        # Delete the specified amount of messages
        await ctx.channel.purge(limit=amount+1)
        confirmation = await ctx.send(f'Cleared {amount} messages')
        print(f'Cleared {amount} messages')
        sleep(3)
        if confirmation:
            await confirmation.delete()


    # Kick command
    @commands.command()
    @commands.check(is_mod or is_admin)
    async def kick(self, ctx, member: discord.Member, *, reason: str):
        # Kick the user
        await member.kick(reason=reason + f' ({ctx.author.name}#{ctx.author.discriminator})')
        await ctx.send(f'{member.name} has been kicked for {reason}')
        print(f'{member.name} has been kicked for {reason}')
    
    # Slowmode command
    @commands.command()
    @commands.check(is_mod or is_admin)
    async def slowmode(self, ctx, seconds: int):
        # Set the slowmode
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f'Slowmode set to {seconds} seconds')
        print(f'Slowmode in {ctx.channel.name} set to {seconds} seconds')

    # Mute command
    @commands.command()
    @commands.check(is_mod or is_admin)
    async def mute(self, ctx, member: discord.Member, *, reason: str):
        # Mute the user
        await member.add_roles(ctx.guild.get_role(753342159444377611))
        await ctx.send(f'{member.name} has been muted for {reason}')
        print(f'{member.name} has been muted for {reason}')

    # Unmute command
    @commands.command()
    @commands.check(is_mod or is_admin)
    async def unmute(self, ctx, member: discord.Member):
        # Unmute the user
        await member.remove_roles(ctx.guild.get_role(753342159444377611))
        await ctx.send(f'{member.name} has been unmuted')
        print(f'{member.name} has been unmuted')
    
def setup(bot):
    bot.add_cog(Moderation(bot))