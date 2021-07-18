import sys
sys.path.append("class")

# Packages
from discord.ext import commands
from logs import *

# This class to run discord bot
class runDiscord():
    def __init__(self, TOKEN, prefix = '$'):
        self.logs = Logs(name='runDiscord.py')
        self.TOKEN = TOKEN
        self.prefix = prefix
        try:
            self.client = commands.Bot(command_prefix="$")
        except Exception as e:
            self.logs.log("\"runDiscord.py\" cannot init\n{e}\n", True, type="Error")
        
    def getClient(self):
        """Get client"""
        return self.client

    def prefix(self, setPrefix = "__defualt__"):
        """Get prefix or set new one"""
        if setPrefix == "__defualt__":
            return self.prefix
        else:
            self.prefix = str(setPrefix)

    def run(self):
        """Run SalmanBot"""
        try:
            self.logs.log("client running...", True, "Info")
            self.client.run(self.TOKEN)
        except Exception as e:
            self.logs.log(f"Cannot run discord bot. Make sure you put correct/valid token!\n{e}\n", True, type="Erorr")