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

    @commands.command()
    async def smallfont(self, ctx, *, text):
        font = {
            'q': 'ǫ',
            'w': 'ᴡ',
            'e': 'ᴇ',
            'r': 'ʀ',
            't': 'ᴛ',
            'y': 'ʏ',
            'u': 'ᴜ',
            'i': 'ɪ',
            'o': 'ᴏ',
            'p': 'ᴘ',
            'a': 'ᴀ',
            's': 's',
            'd': 'ᴅ',
            'f': 'ғ',
            'g': 'ɢ',
            'h': 'ʜ',
            'j': 'ᴊ',
            'k': 'ᴋ',
            'l': 'ʟ',
            'z': 'ᴢ',
            'x': 'x',
            'c': 'ᴄ',
            'v': 'ᴠ',
            'b': 'ʙ',
            'n': 'ɴ',
            'm': 'ᴍ',
        }

        await ctx.send(''.join([font.get(char, char) for char in text]))

    @commands.command()
    async def rps(self, ctx, *, choice):
        choices = ['rock', 'paper', 'scissors']
        bot_choice = random.choice(choices)
        if choice.lower() not in choices:
            await ctx.send('Please choose rock, paper or scissors')
            return None

        if choice.lower() == bot_choice:
            await ctx.send(f'You chose {choice}, I chose {bot_choice}. It\'s a tie!')
        elif choice.lower() == 'rock' and bot_choice == 'scissors':
            await ctx.send(f'You chose {choice}, I chose {bot_choice}. You win!')
        elif choice.lower() == 'paper' and bot_choice == 'rock':
            await ctx.send(f'You chose {choice}, I chose {bot_choice}. You win!')
        elif choice.lower() == 'scissors' and bot_choice == 'paper':
            await ctx.send(f'You chose {choice}, I chose {bot_choice}. You win!')
        else:
            await ctx.send(f'You chose {choice}, I chose {bot_choice}. I win!')
        
    @commands.command()
    async def coinflip(self, ctx):
        await ctx.send(f'{random.choice(["Heads", "Tails"])}')

    @commands.command()
    async def roll(self, ctx, *, faces=6):
        await ctx.send(f'{random.randint(1, faces)}')

    @commands.command()
    async def choose(self, ctx, *, choices):
        await ctx.send(f'I choose {random.choice(choices.split(", "))}!')
    
    @commands.command()
    @commands.cooldown(5, 30, commands.BucketType.user)
    async def meme(self, ctx):
        meme_api = 'https://meme-api.herokuapp.com/gimme'
        meme = requests.get(meme_api).json()
        nsfw = meme['nsfw']
        if nsfw:
            await ctx.send('No clean memes found, try again later.')
            return None
        else:
            embed = discord.Embed(title=meme['title'], url=meme['postLink'])
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'👍 {meme["ups"]} | 🧑 {meme["author"]} | 📜 r/{meme["subreddit"]}')
            await ctx.send(embed=embed)

    @commands.command()
    async def reverse(self, ctx, *, text):
        await ctx.send(text[::-1])

    @commands.command(aliases=['mock'])
    async def sarcasm(self, ctx, *, text):
        await ctx.send(''.join([char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(text)]))

    @commands.command()
    async def clap(self, ctx, *, text):
        await ctx.send(':clap:'.join(text.split(' ')))

    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        await ctx.send(member.avatar_url)

def setup(bot):
    bot.add_cog(Fun(bot))