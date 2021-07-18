import sys
sys.path.append("class")

# Packages
import discord
from discord.ext import commands
from logs import *

# This class to run discord bot
class runDiscord():
    def __init__(self, TOKEN, prefix = '$', description = 'SalmanBot'):
        self.logs = Logs(name='runDiscord.py')
        self.TOKEN = TOKEN
        self.prefix = prefix
        self.description = description

        intents = discord.Intents.default()
        intents.members = True

        try:
            self.client = commands.Bot(command_prefix="$", intents=intents, description=description)
        except Exception as e:
            self.logs.log("\"runDiscord.py\" cannot init\n{e}\n", True, type="Error")
        
    def bot_client(self):
        """Get client"""
        return self.client

    def bot_prefix(self, setPrefix="__defualt__", author="Bot"):
        """Get prefix or set new one"""
        if setPrefix == "__defualt__":
            return self.prefix
        else:
            try:
                self.logs.log(f"Set new prefix ({self.prefix}) -> ({setPrefix})", True, type="command", author=author)
                self.prefix = str(setPrefix)
                self.client.command_prefix = self.prefix
                return True
            except Exception as e:
                self.logs.log("Error while change bot_prefix", True, "Error", author=author)
                return False

    def bot_description(self, setDescription = "__defualt__", author="Bot"):
        """Get description or set new one"""
        if setDescription == "__defualt__":
            return self.description
        else:
            self.logs.log(f"Set new description ({self.description}) -> ({setDescription})", True, type="command", author=author)
            self.description = str(setDescription)
            self.client.description = self.description
            return self.description

    def run(self):
        """Run SalmanBot"""
        try:
            self.logs.log("client running...", True, "Info")
            self.client.run(self.TOKEN)
        except Exception as e:
            self.logs.log(f"Cannot run discord bot. Make sure you put correct/valid token!\n{e}\n", True, type="Erorr")