"""
SalmanBot - 0.1!
-----------------

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
# https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
# Discord embed: https://cog-creators.github.io/discord-embed-sandbox/
# Json error codes :https://discord.com/developers/docs/topics/opcodes-and-status-codes#json-json-error-codes
# reqeust in discord.py (To prevent blocking): https://www.reddit.com/r/Discord_Bots/comments/cmrake/sending_nonblocking_web_requests_with_discordpy/
# Reddit videos (Mearge video with audio) https://gist.github.com/aminnj/2d05f7f2173e12d518f455d47cdf690d
"""

# TODO: Do NOT forget to put Forbidden exception in all classes!
# Forbidden: For bot, if the bot did not have permission to do something.

# TODO: Create new config file.
# Use python config (https://docs.python.org/3/library/configparser.html)
# https://towardsdatascience.com/from-novice-to-expert-how-to-write-a-configuration-file-in-python-273e171a8eb3

import sys
sys.path.append("class")

import logging
import runDiscord
from logs import *
from commands import Commands
from tasks import Tasks
from tempChannel import TempChannels
from reddit import Reddit
from decouple import config
import discord

BOT_DETAILS = {
    'name': "SalmanBot",
    'author': "Salman, MrHora",
    'github': "https://github.com/MrHooRa",
    'bot_github': "https://github.com/MrHooRa/SalmanBot",
    'verison': "0.1",
    'default_prefix': "%",
    'python_version': "3.9.6",
    'guild_id': ---------,      # Change this to your guild id
    'temp_channel_id': 867471772441903135,
    'temp_channel_category': 866660422282379274,
    'temp_channel_name': "$MEMBER_NAME$ Channel", # Use $MEMBER_NAME$ for member name
    'admin_roles': [],
    'reddit_channel': 806551646321901638,
    'cuttly_key': config('CUTTLY_KEY')
}


# DO NOT EDIT THIS!
BOT_ATT = {
    'guild': None,
    'temp_channel_category': None,
    'temp_channel': None
}

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

logs = Logs(name='main.py', tabs=2)

# V=================== Discord details ==================V #
rd = runDiscord.runDiscord(config('TOKEN'),
                           description=f"[!] {BOT_DETAILS['name']} {BOT_DETAILS['verison']}",
                           prefix=BOT_DETAILS['default_prefix'])
client = rd.client
client.command_prefix = BOT_DETAILS['default_prefix']

class MyClient(discord.Client):
    def __init__(self):
        self.is_running = False

    async def on_ready(self):
        if self.is_running:
            return

        logs.log(
            f"Logged in as (Name: {client.user.name}, ID: {client.user.id})", True)

        # Set guild
        BOT_ATT['guild'] = client.get_guild(BOT_DETAILS['guild_id'])

        # Set temp channle
        BOT_ATT['temp_channel'] = client.get_channel(
            BOT_DETAILS['temp_channel_id'])

        # Set temp category
        categories = BOT_ATT['guild'].categories

        # Searh on category and get temp category
        for cg in categories:
            if cg.id == BOT_DETAILS['temp_channel_category']:
                BOT_ATT['temp_channel_category'] = cg
                break
        self.is_running = True

# Cogs
try:
    rd.add_cog(Commands(client, rd))
    rd.add_cog(Tasks(client))
    rd.add_cog(TempChannels(client, BOT_DETAILS))
    rd.add_cog(Reddit(client, BOT_DETAILS))
except Exception as e:
    logs.log(
        f"{BOT_DETAILS['name']} NOT READY. -> Exception: {e}", True, type="Error")

msg = f"""
    ***********************************
            {BOT_DETAILS['name']} {BOT_DETAILS['verison']}
    {BOT_DETAILS['bot_github']}
            ----------------
        
        Running in Python {BOT_DETAILS['python_version']}
        Discord version {discord.__version__}
        Defualt prefix ({rd._prefix()})
    ***********************************
    """
##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##+##

if __name__ == '__main__':
    logs.newLine(
        "\n**********************************************************\n")
    logs.log("Run SalmanBot", False)
    logs.log(msg, True, saveInLog=False)
    rd.run()
