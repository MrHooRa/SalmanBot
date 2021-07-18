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

import sys
sys.path.append("class")

# Defualt packages
import os, asyncio, random

# my classes
import runDiscord
from logs import *

# Get env values
from decouple import config

# # Discord packages
# import discord
# from discord.ext import commands

logs = Logs(name='main.py')

# V=================== Database details ===================V #
dataBase = (config('DB_HOSTNAME'), 
            config('DB_USERNAME'),
            config('DB_PASSWORD'), 
            config('DB_NAME'))
# ^=====================================================^ #


# V=================== Discord details ==================V #
runDiscord = runDiscord.runDiscord(config('TOKEN'))


# # Discord token
# TOKEN = config('TOKEN')

# # Set prefix (dollr sign or anything you want :D)
# client = commands.Bot(command_prefix="$")
# ^=====================================================^ #




##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##
# DO NOT ADD/CHANGE ANYTHING UNDER THIS LINE!
##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##
# RUN THE BOT!
if __name__ == '__main__':
    msg = """
    ***********************************
            SalmanBot - Beta
            ----------------
        
        Running in Python 3.9.6
        '$' is default prefix command
    ***********************************
    """
    logs.log("Run SalmanBot", False, "START")
    logs.log(msg, True, "START")   
    
    runDiscord.run()