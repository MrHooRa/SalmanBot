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
    'python_version': "3.9.6",
    'guild_id': 603958784230162442,
    'temp_channel_id': 867471772441903135,
    'temp_channel_category': 866660422282379274,
    'temp_channel_name': "$MEMBER_NAME$ Channel",         # Use $MEMBER_NAME$ for member name
}

# DO NOT EDIT THIS!
BOT_ATT = {
    'guild': None,
    'temp_channel_category': None
}

import sys

# Defualt packages
import os, asyncio, random
import logging

# SalmnBot classes
sys.path.append("class")
import runDiscord
from logs import *
from commands import Commands
from tasks import Tasks

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
client = rd._client()
client.command_prefix = BOT_DETAILS['default_prefix']
# ^=====================================================^ #

# Bot on_ready
@client.event
async def on_ready():
    tempChannel.start()
    logs.log(f"Logged in as (Name: {client.user.name}, ID: {client.user.id})", True)

    # Set guild
    BOT_ATT['guild'] = client.get_guild(BOT_DETAILS['guild_id'])

    # Set temp category
    categories = BOT_ATT['guild'].categories

    # Searh on category
    for cg in categories:
        if cg.id == BOT_DETAILS['temp_channel_category']:
            BOT_ATT['temp_channel_category'] = cg
            break

#00000000000000000000000Test Area0000000000000000000000000
@client.command(pass_context=True, name="test1", hidden=True)
async def _test(ctx, a):
    if rd._prefix(a, author=ctx.author.name):
        await ctx.reply('تم التغيير بنجاح!', mention_author=True)
    else:
        await ctx.reply("Error!", mention_author=True)
#000000000000000000000000000000000000000000000000000000000

# TEMP CHANNELS

#TODO: Take this function to tasks.py or tempChannel.py
#TODO: Store all temp channel to corrent            #DONE
#TODO: Make new command for temp channel memnber to kick another member from it own channel (Something like: $dc @member)

corrent_tempChannels = []
# corrent_tempChannel:
#   [..], <- Temp channel array
#   [
#    channel_name,
#    category,
#    member
#   ]

@tasks.loop(seconds=1)
async def tempChannel():
    """Make temp channel and move member to it. When all members leave the channel, it'l deleted"""
    try:
        for channel in corrent_tempChannels:
            memChannel = []
            for member in channel[0].members:
                memChannel.append(member)
            if len(memChannel) == 0 :
                logs.log(f"Channel removed (channel name: {channel[0].name}, Category: {channel[2].name}, Member ID: {channel[2].id})", True)
                await channel[0].delete()
                corrent_tempChannels.remove(channel)

    # If channel not found (Most likely member deleted its own channel)
    except discord.NotFound as e_NF:
        corrent_tempChannels.remove(channel)

    except Exception as e:
        logs.log(f"Can not delete channel. Exception -> {e}", True, type="Error")

    try:
        # Get Temp channel ID
        tempChannel = client.get_channel(BOT_DETAILS['temp_channel_id'])
        members = tempChannel.members
        
        # For all members in temp channel
        for member in members:
            tempChannelName = BOT_DETAILS['temp_channel_name'].replace("$MEMBER_NAME$", member.name)

            # Create new temp channel and move user to it!
            createdChannel = await BOT_ATT['guild'].create_voice_channel(tempChannelName, category=BOT_ATT['temp_channel_category'])
            await member.move_to(createdChannel)

            # Set permission (manage_channels) to user
            await createdChannel.set_permissions(member, manage_channels=True, move_members=True)

            # Insert new temp channel details to corrent_tempChannels array
            corrent_tempChannels.append([createdChannel, BOT_ATT['temp_channel_category'], member])

            # For log
            logs.log(f"Create new channel (Channel name: {tempChannelName}, Catrgory: {BOT_ATT['temp_channel_category']}, Member ID: {member.id})", True)

    except Exception as e:
        logs.log(f"Can not create new temp channel. Exception -> {e}", True, type='Error')


# Cogs
try:
    rd.add_cog(Commands(client))
    rd.add_cog(Tasks(client))
except Exception as e:
    logs.log(f"{BOT_DETAILS['name']} NOT READY. -> Exception: {e}", True, type="Error")
    

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
    logs.newLine("\n**********************************************************\n")
    logs.log("Run SalmanBot", False)
    logs.log(msg, True, saveInLog = False)
    rd.run()