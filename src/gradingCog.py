import discord
import keyUtil
import roleUtil
import asyncio
from discord.ext import commands

class GradingCog(commands.Cog):
    def __init__(self, submissionDb, bot, logger):
        self.submissionDb = submissionDb
        self.bot = bot
        self.gradingChannel = None
        self.logger = logger
        self.ungradedSubmissions = {}
        self.mutex = asyncio.Lock()
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.gradingChannel = self.bot.get_channel(799397699735519262)
        if self.gradingChannel == None:
            self.logger.Log("Couldn't get channel for grading cog")
        
        await self.submissionDb.RegisterAddSubmissionCallback(self.OnAddSubmission)

    async def OnAddSubmission(self, submission):
        with self.mutex:
            if not submission.IsGraded():
                self.ungradedSubmissions[submission.GetUuid()] = 'unclaimed'
                await self.gradingChannel.send(f'New submission received, there are {len(self.ungradedSubmissions)} open submissions. Claim one with the `$claim` command')

    @commands.command()
    async def claim(self, ctx):
        'Claim an ungraded submission for judging. This must be used in the judge-grading channel'
        if not roleUtil.IsJudge(ctx.author.roles):
            await ctx.send('You do not have permission to use this command')
            return
        if ctx.channel.name != 'judge-grading':
            await ctx.send(f'You must use this command in the `judge-grading` channel. This channel is `{ctx.channel.name}`')
            return
        with self.mutex:
            uuid = ''
            for k, v in self.ungradedSubmissions:
                if v == 'unclaimed':
                    v = keyUtil.KeyFromAuthor(ctx.author)
                    uuid = k
            if uuid == '':
                await ctx.send('Could not find an unclaimed submission, try again later or check current submissions with `$list_submissions` or `$list_ungraded_submissions`')
        # Grab submission details from submission db and dm ctx owner with deets