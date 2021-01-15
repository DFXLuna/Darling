import discord
import keyUtil
import roleUtil
from discord.ext import commands

class GradingCog(commands.Cog):
    def __init__(self, submissionDb, bot, logger):
        self.submissionDb = submissionDb
        self.bot = bot
        self.gradingChannel = None
        self.logger = logger
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.gradingChannel = self.bot.get_channel(799397699735519262)
        if self.gradingChannel == None:
            self.logger.Log(f"Couldn't get channel for grading cog")
        
        await self.submissionDb.RegisterAddSubmissionCallback(self.OnAddSubmission)

    async def OnAddSubmission(self, submission):
        await self.gradingChannel.send("Test message")
