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
    
#on message balance 

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("$balance"):
        await message.channel.send(f"Your balance is {message.author.balance}")
        return
    if message.content.startswith("$roll"):
        number = random.randint(1, 6)
        await message.channel.send(f"You rolled {number} and your new balance is {message.author.balance}")
        message.author.balance += number
        return

# make a robbing system that can be used to rob someone

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("$rob"):
        await message.channel.send(f"You robbed {message.mentions[0]} for {message.author.balance}")
        message.author.balance -= message.mentions[0].balance
        message.mentions[0].balance = 0
        return


# on command ping
@bot.command()

async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")
    return

# on command say

@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)
    return

# on command roll

@bot.command()
async def roll(ctx):
    number = random.randint(1, 6)
    await ctx.send(f"You rolled a {number}")
    return







bot.run(TOKEN)