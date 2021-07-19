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
from sb_commands import SB_Commands

# Get env values
from decouple import config

# Discord packages
import discord


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
rd = runDiscord.runDiscord(config('TOKEN'), description="[!] SalmanBot - Beta")

client = rd.bot_client()
# ^=====================================================^ #


@client.event
async def on_ready():
    logs.log(f"Logged in as (Name: {client.user.name}, ID: {client.user.id})", True)
# 000000000000000000000






#00000000000000000000000Test Area0000000000000000000000000
@client.command(pass_context=True, name="test1", hidden=True)
async def _test(ctx, a):
    if rd.bot_prefix(a, author=ctx.author.name):
        await ctx.reply('تم التغيير بنجاح!', mention_author=True)
    else:
        await ctx.reply("Error!", mention_author=True)
#000000000000000000000000000000000000000000000000000000000



# Cogs
try:
    rd.add_cog(SB_Commands(client))
except Exception as e:
    logs.log("SalmanBot NOT READY. -> Exception: {e}")
    

msg = f"""
    ***********************************
            SalmanBot - Beta
    https://github.com/MrHooRa/SalmanBot
            ----------------
        
        Running in Python 3.9.6
        Discord version {discord.__version__}
        Defualt prefix ({rd.bot_prefix()})
    ***********************************
    """
##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##
# DO NOT ADD/CHANGE/REMOVE ANYTHING UNDER THIS LINE!
##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##
# RUN THE BOT!
if __name__ == '__main__':
    logs.newLine("\n**********************************************************\n")
    logs.log("Run SalmanBot", False)
    logs.log(msg, True, saveInLog = False)
    if rd.run():
        logs.log("SalmanBot is ready!", True)
