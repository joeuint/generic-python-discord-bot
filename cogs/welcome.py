import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
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
        welcome_channel = self.bot.get_channel(753819624491057174)
        await welcome_channel.send(embed=embed)
        print(f'{member.name} ({member.id}) has joined {member.guild.name} ({member.guild.id})')
    