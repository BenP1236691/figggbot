import discord
from discord.ext import commands 
import random
import os

env_vars = dict()
with open(".env") as f:
    env_vars = dict(
        tuple(line.strip().split("="))
        for line in f.readlines()
        if not line.startswith("#")
    )

TOKEN = env_vars["TOKEN"]

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

# on ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"with {len(bot.guilds)} servers"))
    
# on message
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if message.content.startswith("$ping"):
        await message.channel.send(f"Pong! {round(bot.latency * 1000)}ms")
        return
    

# on command
@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)
    return

@bot.command()
async def roll(ctx):
    await ctx.send(random.randint(1, 6))
    return 

# on slash command
@bot.tree.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")
    return

@bot.tree.command(name="roll")
async def roll(ctx):
    await ctx.send(random.randint(1, 6))
    return

@bot.tree.command(name="say")
async def say(ctx, *, message):
    await ctx.send(message)
    return

@bot.tree.command(name="help")
async def help(ctx):
    await ctx.send(ctx.tree)
    return





bot.run(TOKEN)