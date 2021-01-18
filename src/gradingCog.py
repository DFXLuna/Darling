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
        self.currentSubmissionGraders = []
        self.mutex = asyncio.Lock()
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.gradingChannel = self.bot.get_channel(799397699735519262)
        if self.gradingChannel == None:
            self.logger.Log("Couldn't get channel for grading cog")
        
        await self.submissionDb.RegisterAddSubmissionCallback(self.OnAddSubmission)
        if await self.submissionDb.NumUngradedEntries() > 0:
            self.logger.Log(f'Loading {await self.submissionDb.NumUngradedEntries()} ungraded entries')
            count = 0
            async with self.mutex:
                for uuid in await self.submissionDb.GetUngradedSubmissionUuids():
                    self.ungradedSubmissions[uuid] = 'unclaimed'
                    count += 1
                self.logger.Log(f'Loaded {count} ungraded entries')
            await self.gradingChannel.send(f'Server has started, loaded {count} ungraded entries. Any previous claims have been invalidated.')


    async def OnAddSubmission(self, submission):
        self.logger.Log(f'OnAddSubmission {submission.GetUuid()}')
        async with self.mutex:
            if not submission.IsGraded():
                self.ungradedSubmissions[submission.GetUuid()] = 'unclaimed'
                await self.gradingChannel.send(f'New submission received, there are {len(self.ungradedSubmissions)} open submissions. Claim one with the `$claim` command')

    @commands.command()
    async def claim(self, ctx):
        'Claim an ungraded submission for judging. This must be used in the judge-grading channel'
        self.logger.Log('claim')
        if not roleUtil.IsJudge(ctx.author.roles):
            await ctx.send('You do not have permission to use this command')
            return
        if ctx.channel.name != 'judge-grading':
            await ctx.send(f'You must use this command in the `judge-grading` channel. This channel is `{ctx.channel.name}`')
            return
        async with self.mutex:
            author = keyUtil.KeyFromAuthor(ctx.author)
            
            if author in self.currentSubmissionGraders:
                currentUuid = ''
                for k, v in self.ungradedSubmissions.items():
                    if v == author:
                        currentUuid = k
                        break
                await ctx.send(f'You have already checked out problem {currentUuid}. Please `$pass` or `$fail` that problem before claiming a new one.')
                return
            
            uuid = ''
            for k, v in self.ungradedSubmissions.items():
                if v == 'unclaimed':
                    self.ungradedSubmissions[k] = author
                    self.currentSubmissionGraders.append(author)
                    uuid = k
                    break
            if uuid == '':
                await ctx.send('Could not find an unclaimed submission, try again later or check current submissions with `$list_submissions` or `$list_ungraded_submissions`')
                return
            
            await ctx.send(f'successfully claimed {uuid}, you will receive a direct message with the details.')
        # Grab submission details from submission db and dm ctx owner with deets