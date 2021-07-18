"""
SalmanBot - BETA!
-----------------
This discord bot can do:-
    1) Reddit new upvote posts
    2) Wheel
    3) TTS (Text To Speech)
    4) Special commands
    5) Math equations

===== Check these websites for more info =====

# Check: https://stackoverflow.com/questions/62120537/is-there-a-way-to-play-songs-from-a-dict-discord-py
# Music bot: https://gist.github.com/vbe0201/ade9b80f2d3b64643d854938d40a0a2d

# Reddit api: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
# Reddit api (Best): https://levelup.gitconnected.com/creating-a-reddit-bot-using-python-5464d4a5dff2

# Doc (asyncpraw): https://asyncpraw.readthedocs.io

# https://repl.it/@JunkE/sDB#main.py
# https://uptimerobot.com/

"""


# Defualt packages
import os, asyncio, random

# Get env values
from decouple import config

# Discord packages
import discord
from discord.ext import commands

# V=================== Database details ===================V #
dataBase = (config('DB_HOSTNAME'), 
            config('DB_USERNAME'),
            config('DB_PASSWORD'), 
            config('DB_NAME'))
# ^=====================================================^ #


# V=================== Discord details ==================V #
# Discord token
TOKEN = config('TOKEN')

# Set prefix (dollr sign or anything you want :D)
client = commands.Bot(command_prefix="$")
# ^=====================================================^ #




##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##
# DO NOT ADD ANYTHING UNDER THIS LINE!
##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##
# RUN THE BOT!
client.run(TOKEN)