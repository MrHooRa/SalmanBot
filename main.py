"""
SalmanBot - BETA!
-----------------
This discord bot can do:-
    1) Reddit new upvote posts
    2) Wheel - DONE
    3) TTS (Text To Speech) - DONE
    4) Special commands (clear)
    5) Math equations

===== Check these websites for more info =====

# Check: https://stackoverflow.com/questions/62120537/is-there-a-way-to-play-songs-from-a-dict-discord-py
# Music bot: https://gist.github.com/vbe0201/ade9b80f2d3b64643d854938d40a0a2d

# Reddit api: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
# Reddit api (Best): https://levelup.gitconnected.com/creating-a-reddit-bot-using-python-5464d4a5dff2

# Doc (asyncpraw): https://asyncpraw.readthedocs.io

# https://repl.it/@JunkE/sDB#main.py
# https://uptimerobot.com/

# https://discordpy.readthedocs.io/en/stable/index.html
# https://github.com/Rapptz/discord.py/tree/v1.7.3/examples

"""

import sys
sys.path.append("class")

# Defualt packages
import os, asyncio, random
import logging

# my classes
import runDiscord
from logs import *

# Get env values
from decouple import config

# Discord packages
import discord
# from discord import FFmpegPCMAudio

# Calcualte mp3 file size (seconds)
import eyed3

# Transorm from text --> voice
from gtts import gTTS

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

logs = Logs(name='main.py')

# V=================== Database details (For Reddit) ===================V #
dataBase = (config('DB_HOSTNAME'), 
            config('DB_USERNAME'),
            config('DB_PASSWORD'), 
            config('DB_NAME'))
# ^=====================================================^ #


# V=================== Discord details ==================V #
rd = runDiscord.runDiscord(config('TOKEN'))

client = rd.bot_client()
# ^=====================================================^ #


@client.event
async def on_ready():
    logs.log(f"Logged in as (Name: {client.user.name}, ID: {client.user.id})", True)
    logs.log("SalmanBot is ready :D", True)
# 000000000000000000000

# ----____Text to voice____----
# text -> voice :D
# Usage: $tts lang text

@client.command(pass_context=True, name="tts", hidden=True)
async def _tts(ctx, lan, *msg):
    logMsg = " ".join(msg)
    msg = "".join(msg)
    # Create mp3 voice and play it in discord
    try:    
        myObj = gTTS(text=msg, lang=lan)
        myObj.save("mp3/audio.mp3")

        # Calculate mp3 size (x seconds)
        duration = eyed3.load('mp3/audio.mp3').info.time_secs

        # Play
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('mp3/audio.mp3'))

        # Disconnected from channel after x seconds
        await asyncio.sleep((duration + 0.11))
        await vc.disconnect()

        await ctx.reply('تم يا وحش', mention_author=True)

        # log
        logs.log(f"Played (Lan: {lan}, Msg: {logMsg})", True, type="command", author=ctx.author.name)
    except Exception as e:
        await ctx.reply('رجاءً إختر اللغة', mention_author=True)
        logs.log(f"Something wrong with tts(lan={lan}, msg={msg})\t-> Exception: {e}", True, type="Error", author=ctx.author.name)
# ____----Text to voice----____

# ----____Random Wheel____----
# get random with animation

@client.command(pass_context=True, name="wheel", hidden=True)
async def _wheel(ctx, *arr):
    getWinner = arr[random.randint(0, (len(arr) - 1))]
    msg = await ctx.channel.send(f"The winner is {getWinner}...")

    for _ in range(4):
        await asyncio.sleep(0.05)
        await msg.edit(content=f"The winner is {arr[random.randint(0, (len(arr) - 1))]}...")
    await msg.edit(content=f"The winner is {getWinner} :D")
# ____----Random Wheel----____

# ----____Clear channel chat____----
# (defualt = 5)

@client.command(pass_context=True, name="clear")
async def _clear(ctx, amount=5):
    await ctx.channel.purge(limit=(amount+1))
    logs.log(f"Clear chat (Channel: {ctx.channel.name}, amount: {amount})", True, type="command", author=ctx.author.name)
# ____----Clear channel chat----____

#00000000000000000000000Test Area0000000000000000000000000
@client.command(pass_context=True, name="test1", hidden=True)
async def _test(ctx, a):
    if rd.bot_prefix(a, author=ctx.author.name):
        await ctx.reply('تم التغيير بنجاح!', mention_author=True)
    else:
        await ctx.reply("Error!", mention_author=True)
#000000000000000000000000000000000000000000000000000000000


msg = f"""
    ***********************************
            SalmanBot - Beta
    https://github.com/MrHooRa/SalmanBot
            ----------------
        
        Running in Python 3.9.6
        '{rd.bot_prefix()}' is default prefix command
    ***********************************
    """
##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##
# DO NOT ADD/CHANGE/REMOVE ANYTHING UNDER THIS LINE!
##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##
# RUN THE BOT!
if __name__ == '__main__':
    logs.newLine("\n**********************************************************\n")
    logs.log("Run SalmanBot", False, "START")
    logs.log(msg, True, "START", saveInLog = False)   
    
    rd.run()