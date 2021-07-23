from discord.ext import tasks, commands
from logs import *

class Tasks(commands.Cog):
    """This class contains all commands that are used in discord by users"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logs = Logs(name='tasks.py', tabs=2)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logs.log("Tasks is ready!", True)    