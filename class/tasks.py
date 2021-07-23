from discord.ext import tasks, commands
from logs import *

class Tasks(commands.Cog):
    """This class contains all commands that are used in discord by users"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logs = Logs(name='tasks.py', tabs=2)
        self.tempChannels.start()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logs.log("Tasks is ready!", True)

    @tasks.loop(seconds=1.0)
    async def tempChannels(self):
        """Create new temporary channel when user join spsecifc channel"""
        pass
        # try:
        #     channel = commands.get_channel(temp_channel_id)
        #     print(channel)





        #     # # Get channel
        #     # channel = self.bot.get_channel(temp_channel_id)

        #     # # Get members from channel
        #     # members = channel.members

        #     # memids = [] #(list)
        #     # for member in members:
        #     #     memids.append(member.id)

        #     # self.logs.log(memids, True)
        # except Exception as e:
        #     self.logs.log(f"Channel ID: {temp_channel_id} -> Exception: {e}", True, type="Error")
    
    