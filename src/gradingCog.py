
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
        self.failureReasons = ['Did not compile', 'Did not run', 'Syntax Error', 'Program crashes', 'Incorrect output', 'Incomplete output', 'Fails with sample input data, please test your program with the sample data!', 'Fails with judge input data', 'Java class name does not match file name']
        self.mutex = asyncio.Lock()
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.gradingChannel = self.bot.get_channel(799397699735519262)
        if self.gradingChannel == None:
            self.logger.Log("Couldn't get channel for grading cog")
        
        await self.submissionDb.RegisterAddSubmissionCallback(self.OnAddSubmission)
        if await self.submissionDb.NumUngradedEntries() > 0:
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
    async def unclaim(self, ctx):
        'Remove claim of an ungraded submission. This must be used in your direct messages OR the judge-grading channel'
        self.logger.Log('unclaim')

        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return

        author = keyUtil.KeyFromAuthor(ctx.author)
        uuid = ''
        async with self.mutex:
            if author in self.currentSubmissionGraders:
                for k, v in self.ungradedSubmissions.items():
                    if v == author:
                        uuid = k
                        self.ungradedSubmissions[k] = 'unclaimed'
                        self.currentSubmissionGraders.remove(author)
                        break
                await ctx.send(f'You have removed your claim from problem {uuid}')
                return
        await ctx.send(f'You do not have a problem claimed')

    @commands.command()
    async def claim(self, ctx, requestuuid=None):
        'Claim an ungraded submission for judging. This must be used in your direct messages OR the judge-grading channel'
        self.logger.Log('claim')

        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return

        author = keyUtil.KeyFromAuthor(ctx.author)
        uuid = ''
        async with self.mutex:
            if author in self.currentSubmissionGraders:
                currentUuid = ''
                for k, v in self.ungradedSubmissions.items():
                    if v == author:
                        currentUuid = k
                        break
                await ctx.send(f'You have already checked out problem {currentUuid}. Please `$pass`, `$fail`, `$quick_fail` or `$unclaim` that problem before claiming a new one.')
                return
            if requestuuid == None:
                for k, v in self.ungradedSubmissions.items():
                    if v == 'unclaimed':
                        self.ungradedSubmissions[k] = author 
                        self.currentSubmissionGraders.append(author)
                        uuid = k
                        break
                if uuid == '':
                    await ctx.send('Could not find an unclaimed submission, try again later or check current submissions with `$list_submissions` or `$list_ungraded_submissions`')
                    return
            else:
                if requestuuid in self.ungradedSubmissions:
                    if self.ungradedSubmissions[requestuuid] != 'unclaimed':
                        await ctx.send(f'The problem with the requested uuid has already been claimed, ask {self.ungradedSubmissions[requestuuid]} to unclaim it.')
                        return
                    self.ungradedSubmissions[requestuuid] = author
                    self.currentSubmissionGraders.append(author)
                    uuid = requestuuid
                else:
                    await ctx.send(f'The problem with the requested uuid is not a valid problem. It has either been graded or the uuid you have requested is incorrect.')
                    return
        ## UNLOCK MUTEX

        await ctx.send(f'{author} claimed {uuid}, you will receive a direct message with the details.')
        submission = await self.submissionDb.GetSubmission(uuid)

        await ctx.author.send(f'Submission details:\nProblem Number: {submission.GetProblemNumber()}\nTeam Number: {submission.GetTeamNumber()}\nURL: {submission.GetUrl()}\nUUID: {submission.GetUuid()}\n')
        await ctx.author.send(f'You may `$pass`, `$fail`, `$quick_fail` or `$unclaim` this problem\n----------------------------------------------------------------------------------------------------------------------')

    #pass is a keyword in python, hence _pass
    @commands.command(name="pass")
    async def _pass(self, ctx):
        'Passes your currently claimed problem. This must be used in your direct messages OR the judge-grading channel'
        self.logger.Log('pass')
        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return

        uuid = ''
        author = keyUtil.KeyFromAuthor(ctx.author)
        async with self.mutex:
            if not author in self.currentSubmissionGraders:
                await ctx.send('You do not have a claimed problem. `$claim` to receive a problem for grading')
                return
            self.currentSubmissionGraders.remove(author)
            for k, v in self.ungradedSubmissions.items():
                if v == author:
                    uuid = k
            del self.ungradedSubmissions[uuid]
        ## UNLOCK MUTEX

        userId, teamNumber, problemNumber = await self.submissionDb.PassSubmission(uuid)
        user = await roleUtil.GetUserById(self.bot, userId)
        await ctx.send(f'Problem #{problemNumber} from team #{teamNumber} **passed** successfully!')
        await user.send(f"Team #{teamNumber}'s submission for problem {problemNumber} passed!")

    @commands.command()
    async def fail(self, ctx, reason):
        'Fails your currently claimed problem and send the submitting team the provided quote wrapped message. Your message must be surrounded by quotes. This must be used in your direct messages OR the judge-grading channel. '
        self.logger.Log('fail')
        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return

        uuid = ''
        author = keyUtil.KeyFromAuthor(ctx.author)
        async with self.mutex:
            if not author in self.currentSubmissionGraders:
                await ctx.send('You do not have a claimed problem. `$claim` to receive a problem for grading')
                return
            self.currentSubmissionGraders.remove(author)
            for k, v in self.ungradedSubmissions.items():
                if v == author:
                    uuid = k
            del self.ungradedSubmissions[uuid]
        ## UNLOCK MUTEX

        userId, teamNumber, problemNumber = await self.submissionDb.PassSubmission(uuid)
        user = await roleUtil.GetUserById(self.bot, userId)
        await ctx.send(f'Problem #{problemNumber} from team #{teamNumber} **failed** successfully!')
        await user.send(f"Team #{teamNumber}'s submission for problem {problemNumber} failed. Judge note: {reason}")

    @commands.command()
    async def quick_fail(self, ctx, number, note=''):
        'Fails your currently claimed problem and send the submitting team a prewritten message and an optional note. See $quick_fail_reasons to get responses. Your message must be surrounded by quotes. This must be used in your direct messages OR the judge-grading channel. '
        self.logger.Log('quick_fail')
        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return

        n = int(number)
        if n < 0 or n > len(self.failureReasons) - 1:
            await ctx.send(f'Failure number {n} is not valid. Valid failure numbers are 0 - {len(self.failureReasons) - 1}. See `$quick_fail_reasons` for all valid `$quick_fail` numbers.')
            return 

        await self.fail(ctx, self.failureReasons[n] + '. ' + note)

    @commands.command()
    async def quick_fail_reasons(self, ctx):
        'Lists all quick fail reason numbers and the message they correspond to'
        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return
        
        output = f'`$quick_fail` numbers:\n'
        for i in range(0, len(self.failureReasons) - 1):
            output += f'> #**{i}**: {self.failureReasons[i]}\n'

        await ctx.send(output)
