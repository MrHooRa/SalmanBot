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

BOT_DETAILS = {
    'name':         "SalmanBot",
    'author':       "Salman, MrHora",
    'github':       "https://github.com/MrHooRa",
    'bot_github':   "https://github.com/MrHooRa/SalmanBot",
    'verison':      "0.1",
    'default_prefix': "%",
    'python_version': "3.9.6"
}


import sys

from discord import guild
sys.path.append("class")

# Defualt packages
import os, asyncio, random
import logging

# my classes
import runDiscord
from logs import *
from sb_commands import SB_Commands
from sb_tasks import SB_Tasks

# Get env values
from decouple import config

# Discord packages
import discord
from discord import VoiceChannel
from discord.ext import tasks

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

logs = Logs(name='main.py', tabs=2)

# V=================== Database details (For Reddit) ===================V #
dataBase = (config('DB_HOSTNAME'), 
            config('DB_USERNAME'),
            config('DB_PASSWORD'), 
            config('DB_NAME'))
# ^=====================================================^ #


# V=================== Discord details ==================V #
rd = runDiscord.runDiscord(config('TOKEN'), description=f"[!] {BOT_DETAILS['name']} {BOT_DETAILS['verison']}", prefix=BOT_DETAILS['default_prefix'])
client = rd.bot_client()
client.command_prefix = BOT_DETAILS['default_prefix']
# ^=====================================================^ #

# Bot on_ready
@client.event
async def on_ready():
    tempChannel.start()
    logs.log(f"Logged in as (Name: {client.user.name}, ID: {client.user.id})", True)

#00000000000000000000000Test Area0000000000000000000000000
@client.command(pass_context=True, name="test1", hidden=True)
async def _test(ctx, a):
    if rd.bot_prefix(a, author=ctx.author.name):
        await ctx.reply('تم التغيير بنجاح!', mention_author=True)
    else:
        await ctx.reply("Error!", mention_author=True)
#000000000000000000000000000000000000000000000000000000000

corrent_tempChannels = []
# categoryTemp = 864650793655337011
categoryTemp = 866660422282379274

@tasks.loop(seconds=1)
async def tempChannel():
    try:
        for channel in corrent_tempChannels:
            memChannel = []
            for member in channel.members:
                memChannel.append(member)
            if len(memChannel) == 0 :
                logs.log(f"Channel removed (channel name: {channel.name})", True)
                await channel.delete()
                corrent_tempChannels.remove(channel)

    except Exception as e:
        logs.log(f"Can not delete channel. Exception -> {e}", True)

    try:
        tempChannel = client.get_channel(865306754446131210)
        members = tempChannel.members
        guild = client.get_guild(603958784230162442)
        categories = guild.categories

        for cg in categories:
            if cg.id == categoryTemp:
                categoy = cg

        for member in members:
            channel_details = {
                'name': f"{member.name} Channel",
                'category': categoy
            }

            createdChannel = await guild.create_voice_channel(channel_details['name'], category=channel_details['category'])
            await member.move_to(createdChannel)
            corrent_tempChannels.append(createdChannel)
            logs.log(f"Create new channel for {member.name} in {channel_details['category']} categoy", True)

    except Exception as e:
        logs.log(f"Can not create new temp channel. Exception -> {e}", True)


# Cogs
try:
    rd.add_cog(SB_Commands(client))
    rd.add_cog(SB_Tasks(client))
except Exception as e:
    logs.log(f"{BOT_DETAILS['name']} NOT READY. -> Exception: {e}")
    

msg = f"""
    ***********************************
            {BOT_DETAILS['name']} {BOT_DETAILS['verison']}
    {BOT_DETAILS['bot_github']}
            ----------------
        
        Running in Python {BOT_DETAILS['python_version']}
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
    rd.run()