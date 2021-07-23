import discord
from discord.ext import commands
from logs import *

class runDiscord():
    def __init__(self, TOKEN, prefix = '$', description = 'SalmanBot'):
        self.logs = Logs(name='runDiscord.py')
        self.TOKEN = TOKEN
        self.prefix = prefix
        self.description = description

        intents = discord.Intents.default()
        intents.members = True
        intents.reactions = True
        intents.guilds = True

        try:
            # Create client
            self.client = commands.Bot(command_prefix="$", intents=intents, description=description)
        
        #TODO: Choose correct Exception!
        except Exception as e:
            self.logs.log("\"runDiscord.py\" cannot init\n{e}\n", True, type="Error")
        
    def _prefix(self, setPrefix="__defualt__", author="Bot"):
        """Get prefix or set new one"""
        if setPrefix == "__defualt__":
            return self.prefix
        try:
            self.client.command_prefix = setPrefix
            self.logs.log(f"Set new prefix ({self.prefix}) -> ({setPrefix})", True, author=author)
            self.prefix = str(setPrefix)
            return True
        except Exception as e:
            self.logs.log(f"Error while change bot_prefix. -> Exception: {e}", True, "Error", author=author)
            return False

    def _description(self, setDescription = "__defualt__", author="Bot"):
        """Get description or set new one"""
        if setDescription == "__defualt__":
            return self.description

        self.client.description = setDescription
        self.logs.log(f"Set new description ({self.description}) -> ({setDescription})", True, type="command", author=author)
        self.description = str(setDescription)
        return self.description

    def run(self):
        """Run SalmanBot"""
        try:
            self.logs.log("client running...", True)
            self.client.run(self.TOKEN)
            return True
        except Exception as e:
            self.logs.log(f"Cannot run discord bot. -> Exception: {e}\n", True, type="Erorr")
            return False
            
    def add_cog(self, className):
        """Add cog to bot"""
        try:
            self.client.add_cog(className)
        except Exception as e:
            self.logs.log(f"add_cog did not work. -> Exception: {e}")