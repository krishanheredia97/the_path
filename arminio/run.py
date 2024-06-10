import os
import discord
from discord.ext import commands

TOKEN = os.getenv('ARMINIO_TOKEN')
SERVER_ID = 1238187583734022246
KEEP_ROLE_ID = 1248715938627325993

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='pop')
async def pop(ctx, language: str):
    from utils.create_default_roles import create_default_roles
    from utils.populate import populate
    if ctx.guild.id != SERVER_ID:
        await ctx.send("This command can only be used in the specified server.")
        return

    # Create default roles
    role_ids, base_role_id = await create_default_roles(ctx.guild)
    await ctx.send(f"Created default roles")

    # Call populate function
    await populate(ctx, ctx.guild, language, role_ids, bot)

@bot.command()
async def rdelall(ctx):
    from utils.delete_roles import delete_all_roles
    if ctx.guild.id != SERVER_ID:
        await ctx.send("This command can only be used in the specified server.")
        return

    try:
        deleted_roles = await delete_all_roles(ctx.guild, KEEP_ROLE_ID)
        await ctx.send(f"Deleted roles: {', '.join(deleted_roles)}")
    except ValueError as e:
        await ctx.send(str(e))

@bot.command()
async def rdel(ctx, *role_ids):
    from utils.delete_roles import delete_roles
    if ctx.guild.id != SERVER_ID:
        await ctx.send("This command can only be used in the specified server.")
        return

    deleted_roles = await delete_roles(ctx.guild, *role_ids)
    await ctx.send(f"Deleted roles: {', '.join(deleted_roles)}")

@bot.command()
async def cdel(ctx, *channel_ids):
    from utils.delete_channels import delete_channels
    if ctx.guild.id != SERVER_ID:
        await ctx.send("This command can only be used in the specified server.")
        return

    # Adding debug print to check received channel IDs
    print(f"Received channel IDs for deletion: {channel_ids}")

    deleted_channels = await delete_channels(ctx.guild, *channel_ids)
    await ctx.send(f"Deleted channels: {', '.join(deleted_channels)}")

bot.run(TOKEN)
