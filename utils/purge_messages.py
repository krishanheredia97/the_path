import os
import discord
from discord.ext import commands

TOKEN = os.getenv('TUSK_TOKEN')
SERVER_ID = int(os.getenv('SERVER_ID'))

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def clean(ctx):
    channel = ctx.channel
    messages = await channel.purge(limit=None)
    await ctx.send(f'Deleted {len(messages)} message(s) from #{channel.name}')

bot.run(TOKEN)