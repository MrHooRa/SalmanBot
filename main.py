# Check: https://stackoverflow.com/questions/62120537/is-there-a-way-to-play-songs-from-a-dict-discord-py
# Music bot: https://gist.github.com/vbe0201/ade9b80f2d3b64643d854938d40a0a2d

# Reddit api: https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
# Reddit api (Best): https://levelup.gitconnected.com/creating-a-reddit-bot-using-python-5464d4a5dff2

# Doc (asyncpraw): https://asyncpraw.readthedocs.io

# https://repl.it/@JunkE/sDB#main.py
# https://uptimerobot.com/

# defualt packages
import os
import asyncio

# Make discord bot alive 24/7 by using https://uptimerobot.com
from keep_alive import keep_alive
# from keep_alive import home

# Discord packages
import discord
from discord import FFmpegPCMAudio
from discord.utils import get
from discord.ext import commands
from discord.ext import tasks

# Transorm from text --> voice
from gtts import gTTS
import speech_recognition as sr

# Calcualte mp3 file size (seconds)
import eyed3

# Play songs
from discord.utils import get
import youtube_dl
import requests

# Get reddit json and upvote system
import requests
import json
import asyncpraw
import praw
from redditClass import Reddit

# Random wheel
import random

# Mysql db
import mysql.connector
from mysql.connector import Error

# Threading
from threading import Thread

# Other
# from fivePD import FivePD

# Java app
from javaApp import getMessage

# Get token
TOKEN = os.getenv('TOKEN')

# Set prefix (sign or anything you want :D)
client = commands.Bot(command_prefix="$")

# Reddit api
reddit = asyncpraw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                          client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                          password=os.getenv('REDDIT_PASSWORD'),
                          user_agent="SalmanBot 0.1 by u/IHoora",
                          username=os.getenv('REDDIT_USERNAME'))

host = os.getenv('DB_HOSTNAME')
user = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

R = Reddit("IHooRa", "new", 20)
# F = FivePD()

# Connecte to MySql database
try:
    connection = mysql.connector.connect(host=host,
                                     database=database,
                                     user=user,
                                     password=password)
    print("Database is connected")
except:
    print("Error while connected to database")

# ----____Reddit upvote____----
# Update reddit every x seconds


@tasks.loop(seconds=100)
async def runReddit():
    channel = client.get_channel(806551646321901638)
    R.db(str(host), str(user), str(password),
         str(database), "discordBot_redditPosts")

    try:
        r = R.update()
        R.db_close()

        for i in range(len(r)):
            isVideo = r[i][5]
            isYoutube = r[i][6]
            isImageGif = r[i][7]
            isText = r[i][8]
            # Default image
            rIcon = "https://user-images.githubusercontent.com/33750251/59486444-3699ab80-8e71-11e9-9f9a-836e431dcbfd.png"
            req = 0

            # Create a new embed
            embed = discord.Embed(
                title=f"{r[i][2]}", url=r[i][3], color=0xFF5733)

            if isVideo or isYoutube:
                await channel.send(r[i][3])
                req = "Video/Youtube"
            elif isImageGif:
                tRPT = r[i][3].replace("gifv", "gif")
                tRPAU = f"https://www.reddit.com/{r[i][1]}/comments/{r[i][0]}"
                embed = discord.Embed(title=r[i][2], url=tRPAU, color=0xFF5733,
                                      description=f"Posted in {r[i][1]} by u/{r[i][9]} • {r[i][10]} points and {r[i][11]} comments")
                embed.set_author(name="reddit")
                embed.set_image(url=tRPT)
                await channel.send(embed=embed)
                req = "Image/gif"
            else:
                await channel.send(r[i][3])
                req = "Text/Other"

            print(
                f"Reddit\n\t-> ID: {r[i][0]}\n\t-> Subreddit: {r[i][1]}\n\t-> Req: {req}")

    except Error as e:
        print("Error while print R.update() ->", e)
# ____----Reddit upvote----____


# ----____FivePD____----
# # Update reddit every x seconds
# @tasks.loop(seconds=30)
# async def getFivePDDATA():
#     channel = client.get_channel(821460408153538640)

#     F.db(str(host), str(user), str(password), str(database), "users")
#     i = 3

#     try:
#         # print("\n*****\nUPDATE\n")
#         await channel.purge(limit=i)

#         GetF = F.get()
#         F.db_close()

#         for x in GetF:
#             isAdmin = "Yes" if x[1] == 1 else "No"
#             activated = "On duty" if x[2] == 1 else "Out of duty"

#             await channel.send(content=f"```GameName: {x[0]}\n\tIsAdmin: {isAdmin} \t| Activate: {activated}```")

#             # msg = await channel.fetch_message(msgList[i])
#             # await msg.edit(content=f"```GameName: {x[0]}\n\tIsAdmin: {isAdmin} \t| Activate: {activated}```")

#             # await channel.send(f"`GameName: {x[0]}\t\t\t\t\t\t\t\t\t\t\n\tIsAdmin: {isAdmin} \t| Activate: {activated}`")
#             # print("Update " + f" GameName: {x[0]}\n\tIsAdmin: {isAdmin} \t| Activate: {activated}")

#     except Error as e:
#         print("Error while trying to get data ->", e)
# ____----FivePD----____

# ----____Java app____----

async def javaGetMessage():
    a = 0
    while True:
        try:
            msg = getMessage(connection)
            if msg[3] != "true":
                channel = client.get_channel(int(msg[2]))
                await channel.send(msg[1])
        except:
            a = 0
        await asyncio.sleep(0.3)


@client.command()
async def startJava(ctx):
    print("Java message running")
    client.loop.create_task(javaGetMessage())


# @tasks.loop(seconds=2)
# async def javaMessage():
#     print("loop ya 3r9")
#     try:
#         msg = getMessage()
#         if msg[3] != "true":
#             channel = client.get_channel(int(msg[2]))
#             await channel.send(msg[1])
#     except:
#         print("Error")
# ____----Java app----____

# Check if the bot connected to the server or not :D
# Check if reddit api is connected


@client.event
async def on_ready():
    runReddit.start()
    # getFivePDDATA.start()
    print("Bot is ready :D")

# ----____Text to voice____----
# text -> voice :D
# Usage: $p "text"


@client.command(pass_context=True)
async def t(ctx, msg, lan="ar"):

    # Create mp3 voice
    myObj = gTTS(text=msg, lang=lan)
    myObj.save("mp3/audio.mp3")

    # log
    print(f"Played: {msg}")

    # Calculate mp3 size (x seconds)
    duration = eyed3.load('mp3/audio.mp3').info.time_secs

    # Play
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('mp3/audio.mp3'),
            after=lambda e: print('done', e))

    # Disconnected from channel after x seconds
    await asyncio.sleep((duration + 0.1))
    await vc.disconnect()
# ____----Text to voice----____

# ----____Clear channel chat____----
# (defualt = 5)


@client.command(pass_context=True, name="clear")
async def _clear(ctx, amount=5):
    await ctx.channel.purge(limit=(amount+1))
    print("clear chat")
# ____----Clear channel chat----____

# ----____Play youtube video____----
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
song_queue = []

# Search on youtube


def search(arg):
    try:
        requests.get("".join(arg))
    except:
        arg = " ".join(arg)
    else:
        arg = "".join(arg)
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f"ytsearch: {arg}", download=False)[
            'entries'][0]
    return {"source": info['formats'][0]['url'], 'title': info['title']}


async def play_next(ctx):
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    # voice = get(client.voice_clients, guild=ctx.guild)
    if len(song_queue) > 1:
        del song_queue[0]
        vc.play(discord.FFmpegPCMAudio(
            song_queue[0]['source'], **FFMPEG_OPTIONS))
        vc.is_playing()

# Play song (Youtube)


@client.command(pass_context=True)
async def play(ctx, *arg):
    channel = ctx.message.author.voice.channel

    if channel:
        vc = await channel.connect()

        if vc and vc.is_connected():
            await vc.move_to(channel)
        else:
            vc = await channel.connect()

        if not vc.is_playing():
            vc.play(discord.FFmpegPCMAudio(
                search(arg)['source'], **FFMPEG_OPTIONS))
            vc.is_playing()
        else:
            await ctx.channel.send("Added to queue")
    else:
        await ctx.channel.send("You're not connected to any channel!")

# Stop song


@client.command(pass_context=True)
async def stop(ctx, *arg):
    channel = ctx.message.author.voice.channel
    if channel:
        vc = await channel.connect()
        if vc.is_playing():
            await vc.disconnect()
# ____----Play youtube video----____


# ----____Get reddit upvotes____----
@client.command(pass_context=True)
async def r(ctx, u):
    # Get url from client and get json
    r = requests.get(u, headers={'User-agent': 'SalmanBot 0.1'})
    # load json to make it easy to get what we want
    r = json.loads(r.text)
    await ctx.channel.purge(limit=1)
    rU = r[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
    await ctx.channel.send(f"تفضل يا {ctx.message.author.mention} -> {rU}")
# ____----Get reddit upvotes----____


# ----____Random Wheel____----
@client.command(pass_context=True, name="wheel")
async def _wheel(ctx, *arr):
    getWinner = arr[random.randint(0, (len(arr) - 1))]
    await ctx.channel.send(f"The winner is {getWinner} :D")

    # wheelList = []
    # for i in range(len(arr)):
    #     # TO-DO: Fix this shit (It should check if the last char is "," or "،" and igonre blank -_-)
    #     tempWord = []
    #     for j in range(len(arr[i])):
    #         if arr[i][j] != ',' and arr[i][j] != ",":
    #             tempWord.append(arr[i][j])
    #         else:
    #             pass

    #     wheelList.append("".join(tempWord))
    # print(wheelList)
    # if len(wheelList) > 0:
    #     for i in range(len(arr)):
    #         wheelList.append(arr[i])
    # getWinner = wheelList[random.randint(0, (len(wheelList) - 1))]
    # await ctx.channel.send(f"The winner is {getWinner} :D")
# ____----Random Wheel----____

# # ----____Get data from DB____----
# @client.command(pass_context=True, name="list")
# async def _list(ctx):
#     mycursor.execute("SELECT * FROM `discordBot_musicList`")
#     getMusicList = mycursor.fetchall()

#     for music in getMusicList:
#         channel = client.get_channel(806551646321901638)
#         await channel.send(music)
# # ____----Get data from DB____----

# ----____TEST____----


@client.command(pass_context=True, name="dev1")
async def _dev1(ctx, n):
    channel = client.get_channel(821460408153538640)
    for i in range(int(n)):
        await channel.send(n)


@client.command(pass_context=True, name="getArg")
async def _getArg(ctx, *a):
    print(a)


# get top reddit
@client.command(pass_context=True, name="reddit")
async def _reddit(ctx, subR, l=5):
    # to find the top most submission in the subreddit "MLPLounge"
    subreddit = await reddit.subreddit(str(subR))
    async for submission in subreddit.hot(limit=l):
        await ctx.channel.send(submission.title)
        await ctx.channel.send(submission.url)

# get song name and url


@client.command(pass_context=True)
async def getSong(ctx, *arg):
    await ctx.channel.send("Search: {0}".format(search(arg)['source']))

# Leave channel


@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    await channel.disconnect()

# help


@client.command(pass_context=True, name="list")
async def _list(ctx):
    await ctx.channel.send("Cleared :7190_linkpepehype: {0.author.mention}".format(ctx.message))
# ____----TEST----____

# To keep the bot running 24/7
keep_alive()

# Run
client.run(TOKEN)