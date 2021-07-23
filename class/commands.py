from logs import *
from discord.ext import commands
import discord, asyncio, random

# Transorm from text --> voice
from gtts import gTTS

class Commands(commands.Cog):
    """This class contains all commands that are used in discord by members"""
    
    def __init__(self, bot ,rd):
        self.bot = bot
        self.rd = rd
        self.logs = Logs(name='commands.py')

    @commands.Cog.listener()
    async def on_ready(self):
        self.logs.log("Commands is ready!", True)

    @commands.command(pass_context=True, name="tts", help="- TTS (Text To Speech)\tUsage: %tts `lang` `msg`")
    async def _tts(self, ctx, lan, *msg):
        """
        Text To Speech
        Usage: $tts language msg
        language list -> (ar, en, ja, ru, it, etc...) *Note: search in google about languages code!
        """
        if len(msg) == 0:
            await ctx.reply("الرجاء كتابة نص!", mention_author=True)
            return

        channel = ctx.author.voice.channel if ctx.author.voice is not None else None          
        msg = " ".join(msg)

        # Create mp3 voice and play it in discord
        try:
            if channel != None:    
                ttsMP3 = gTTS(text=msg, lang=lan)
                ttsMP3.save("mp3/bot_tts.mp3")

                server = channel.guild
                def dc_bot(error):
                    try:
                        fut = asyncio.run_coroutine_threadsafe(server.voice_client.disconnect(), self.bot.loop)
                        fut.result()
                    except Exception as e:
                        self.logs.log(e, True, type="Error")

                if server.voice_client == None:
                    await channel.connect()
                    audio_source = discord.FFmpegPCMAudio('mp3/bot_tts.mp3')
                    server.voice_client.play(audio_source, after=dc_bot)
                    await ctx.reply('تم يا وحش', mention_author=True)

                # log
                self.logs.log(f"Played (Lan: {lan}, Msg: {msg})", True, type="command", author=ctx.author.id)
            else:
                self.logs.log(f"Member is not in voice channel!", True, type="Error", author=ctx.author.id)
                await ctx.reply('الرجاء دخول روم لإستخادم هذا الأمر!', mention_author=True)
        except Exception as e:
            await ctx.reply('الرجاء إختيار رمز لغة صحيح!', mention_author=True)
            self.logs.log(f"Something wrong with tts(lan={lan}, msg={msg})\t-> Exception: {e}", True, type="Error", author=ctx.author.name)

    @commands.command(pass_context=True, name="wheel", help="- Get random winner\tUsage: %wheel obj1 obj2 ...")
    async def _wheel(self, ctx, *arr):
        """
        TODO: Fix this shit. Fahad want put qumma.
        Wheel with animation
        Uasge: $wheel Obj1 Obj2 Obj3 ... Objn
        """
        getWinner = arr[random.randint(0, (len(arr) - 1))]
        msg = await ctx.channel.send(f"The winner is {getWinner}...")

        for _ in range(4):
            await asyncio.sleep(0.05)
            await msg.edit(content=f"The winner is {arr[random.randint(0, (len(arr) - 1))]}...")
        await msg.edit(content=f"The winner is {getWinner} :D")
    
    @commands.command(pass_context=True, name="clear", help = "- Clear text\tUsage %clear amount")
    async def _clear(self, ctx, amount=5):
        """
        Clear text in channel
        Usage: $clear n     -> n = is optional!
        By default n = 5
        """
        await ctx.channel.purge(limit=(amount))
        self.logs.log(f"Clear chat (Channel: {ctx.channel.name}, amount: {amount})", True, type="command", author=ctx.author.name)
        await asyncio.sleep(1)
        msg = await ctx.send(f"تم مسح {amount} من الرسائل!")
        await asyncio.sleep(2)
        await msg.delete()

    @commands.command(pass_context=True, name="prefix", hidden=True)
    @commands.has_role(603960582584139798) # For Admins only!
    async def _prefix(self, ctx, newPrefix: str):
        """Change bot prefix"""
        if self.rd._prefix(newPrefix, author=ctx.author.name):
            await ctx.author.send(f'Prefix changed to {newPrefix} successfully!')
        else:
            await ctx.author.send('Did not change prefix!')
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BotMissingRole):
            await ctx.author.send("You cant not use this command!")