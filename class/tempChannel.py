from discord.ext import tasks, commands
import discord
from logs import *

#TODO: Save all temp channels in file.txt

class TempChannels(commands.Cog):
    """Create temp channel and give member permission to manage it"""
    
    def __init__(self, bot, BOT_DETAILS):
        self.bot =  bot
        self.BOT_DETAILS = BOT_DETAILS
        self.logs = Logs(name="tempChannels.py")
        self.is_running = False

        self.corrent_tempChannels = []
        # corrent_tempChannel:
        #   [..], <- Temp channel array
        #   [
        #    channel,
        #    category,
        #    member     <- Channel owner permissions[manage_channel=True, move_members=True]
        #   ]

        self.BOT_ATT = {
            'guild': None,
            'temp_channel_category': None,
            'temp_channel': None
        }

    # Get all att and set them to self.BOT_ATT
    def set_BOT_ATT(self):
        # Get guild by guild ID
        guild = self.bot.get_guild(self.BOT_DETAILS['guild_id'])

        # Get category by category ID
        categories = guild.categories
        # Search in discord about category with id = temp_channel_category
        for cg in categories:
            if cg.id == self.BOT_DETAILS['temp_channel_category']:
                    category = cg
                    break
        # Set all atts
        self.BOT_ATT['guild'] = guild
        self.BOT_ATT['temp_channel_category'] = category
        self.BOT_ATT['temp_channel'] = self.bot.get_channel(self.BOT_DETAILS['temp_channel_id'])

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.is_running:
            # To set all atts
            self.set_BOT_ATT()
            self.is_running = True

        if not self.tempChannels.is_running():
            self.tempChannels.start()

            # When tempChannel.py ready
            self.logs.log("Temp Channels is ready!", True)

    @tasks.loop(seconds=1)
    async def tempChannels(self):
        """Create new temporary channel when user join spsecifc channel"""
 
        # Delete empty channels!
        try:
            # Check if corrent channels empty!
            for channel in self.corrent_tempChannels:
                membersInChannel = len(channel[0].members)
                if membersInChannel == 0:
                    self.logs.log(f"Channel removed (channel name: {channel[0].name}, Category: {channel[1].name}, Member ID: {channel[2].id})", True)
                    await channel[0].delete()
                    self.corrent_tempChannels.remove(channel)

        # If channel not found (Most likely member deleted its own channel)
        except discord.NotFound:
            self.corrent_tempChannels.remove(channel)
        except Exception as e:
            self.logs.log(f"Can not delete channel. Exception -> {e}", True, type="Error")

        # Create new temp channel
        try:
            # Get Temp channel members
            members = self.BOT_ATT['temp_channel'].members

            # Create channel for each member in temp channel
            # member = channel owner (For temp channel)
            for member in members:
                temp_channelName = self.BOT_DETAILS['temp_channel_name'].replace("$MEMBER_NAME$", member.name)

                # Create new temp channel and give memnber 'manage_chaannel, move_members' premissions
                createdChannel = await self.BOT_ATT['guild'].create_voice_channel(temp_channelName, category=self.BOT_ATT['temp_channel_category'])
                await member.move_to(createdChannel)

                # Set permission (manage_channels, move_members) to channel owner
                await createdChannel.set_permissions(member, manage_channels=True, move_members=True)

                # Insert new temp channel details to corrent_tempChannels array
                self.corrent_tempChannels.append([createdChannel, self.BOT_ATT['temp_channel_category'], member])

                # For log
                self.logs.log(f"Create new channel (Channel name: {temp_channelName}, Catrgory: {self.BOT_ATT['temp_channel_category']}, Member ID: {member.id})", True)

        except discord.HTTPException as httperror:
            self.logs.log(f'Creating the channel failed! (Member ID: {member.id}). -> Exception: {httperror}', True, type="Error")

            # If filed to create temp channel
            await member.send('للأسف، لايمكن انشاء غرفة مؤقتة! الرجاء التواصل مع الإدارة')

        except Exception as e:
            self.logs.log(f"Can not create new temp channel. Exception -> {e}", True, type='Error')