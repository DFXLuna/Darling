import discord
import keyUtil
import roleUtil
import numProblems
import re
import datetime
import asyncio
from discord.ext import commands

class SubmissionCog(commands.Cog):
    def __init__(self, bot, logger, registrationDb, submissionDb):
        self.num_problems = numProblems.num_problems
        self.bot = bot
        self.logger = logger
        self.registrationDb = registrationDb
        self.submissionDb = submissionDb
        self.submissionsOpen = False

    @commands.command()
    async def submit(self, ctx, problemNumber):
        'Submit a solution to the given problem number. You must attach your submission file to the message. Mutiple files must be submitted as a zip archive. You must DM CodeWarsBot to use this command Syntax: `$submit <problemNumber>`'
        self.logger.Log(f'submit {ctx.author} {problemNumber}')
        
        if not await roleUtil.IsValidDMContext(ctx, self.bot):
            return

        submitter = keyUtil.KeyFromAuthor(ctx.author)
        teamNumber = await self.registrationDb.GetEntry(submitter)

        if self.submissionsOpen is False and int(problemNumber) > 1:
            await ctx.send(f'Submissions are not open, please wait for the event to start.')
            return

        if int(problemNumber) < 0 or int(problemNumber) > self.num_problems:
            await ctx.send(f'Problem number must be greater than 0 and less than {self.num_problems}')
            return

        if teamNumber is None:
            await ctx.send(f'{submitter} is not registered to a team. Please use the `$register <teamNumber>` command to register yourself to your team.')
            return

        if len(ctx.message.attachments) == 0:
            await ctx.send(f'No attachment found, please attach your submission file to the command message. Multiple files may be submitted as a zip archive.')
            return

        if len(ctx.message.attachments) > 1:
            await ctx.send(f'More than one attachment detected. Multiple files must be submitted as a zip archive.')
            return

        if await self.submissionDb.SubmissionAlreadyInProgress(teamNumber, int(problemNumber)):
            await ctx.send(f'Team #{teamNumber} has already submitted problem {problemNumber}. It has either already passed or is currently in grading')
            return

        if not await self.VerifyFileName(ctx.message.attachments[0].filename, int(problemNumber)):
            await ctx.send(f'Submission filename is incorrect, filename format is `probXX.ext` where `XX` is the problem number with a leading zero for single digit problem numbers and `ext` is one of `py2` `py3` `java` `js` `c` `cpp` `zip`. Additionally, make sure the problem number of the attachment matches the one in the command.')
            return

        await asyncio.gather(
            self.submissionDb.AddSubmission(keyUtil.KeyFromAuthor(ctx.author), teamNumber, int(problemNumber), ctx.message.attachments[0].url, ctx.author.id),
            ctx.send(f'Submission of problem {problemNumber} for team #{teamNumber} received. It has been forwarded to the judges for grading.'),
        )

        for attachment in ctx.message.attachments:
            await ctx.send(f'Attachment receipt:\nID {attachment.id}\nSize: {attachment.size}\nFilename: {attachment.filename}\nURL: {attachment.url}')

    @commands.command()
    async def list_submissions(self, ctx):
        'Lists all submissions currently in the database'
        self.logger.Log('list_submissions')
        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return

        entries = await self.submissionDb.GetAllSubmissions()
        displayString = 'Submissions:\n'
        for entry in entries:
            displayString += f'> Problem: **{entry.GetProblemNumber()}**, Team: **{entry.GetTeamNumber()}**, Status: **{entry.GetGradeStatus()}**\n'

        await ctx.send(displayString)

    @commands.command()
    async def list_uuids(self, ctx):
        'Lists all submissions with uuids currently in the database'
        self.logger.Log('list_uuids')
        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return

        entries = await self.submissionDb.GetAllSubmissions()
        displayString = 'Submissions:\n'
        for entry in entries:
            displayString += f'> UUID: {entry.GetUuid()} Problem: **{entry.GetProblemNumber()}**, Team: **{entry.GetTeamNumber()}**, Status: **{entry.GetGradeStatus()}**\n'

        await ctx.send(displayString)

    @commands.command()
    async def list_ungraded_submissions(self, ctx):
        'Lists all ungraded submissions currently in the database'
        self.logger.Log('list_ungraded_submissions')
        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return

        entries = await self.submissionDb.GetUngradedSubmissions()
        displayString = 'Ungraded Submissions:\n'
        for entry in entries:
            displayString += f'> Problem: **{entry.GetProblemNumber()}**, team: **{entry.GetTeamNumber()}**\n'

        await ctx.send(displayString)

    @commands.command()
    async def list_team_submissions(self, ctx):
        'Lists all submissions for a team'
        self.logger.Log('list_team_submissions')
        if not await roleUtil.IsValidDMContext(ctx, self.bot):
            return

        teamNumber = await self.registrationDb.GetEntry(keyUtil.KeyFromAuthor(ctx.author))
        entries = await self.submissionDb.GetTeamSubmissions(teamNumber)
        displayString = f"Team #**{teamNumber}** Submissions:\n"
        for entry in entries:
            displayString += f'> Problem: **{entry.GetProblemNumber()}**, status: **{entry.GetGradeStatus()}**\n'

        await ctx.send(displayString)

    @commands.command()
    async def scoreboard(self, ctx):
        self.logger.Log('scoreboard')
        passes = await self.submissionDb.GetPasses()
        fails = await self.submissionDb.GetFails()

        displayString = '```\nProblem | Passes | Fails | %\n---------------------------------\n'
        for i in range(0, len(passes)):
            if passes[i] + fails[i] != 0:
                displayString += f'{i:02}      | {passes[i]:02}     | {fails[i]:02}    | {(passes[i]/(passes[i] + fails[i])) * 100}%\n'
            else:
                displayString += f'{i:02}      | {passes[i]:02}     | {fails[i]:02}    | 0.0%\n'
        displayString += '```'
        await ctx.send(displayString)

    @commands.command()
    async def delete_submission(self, ctx, uuid):
        self.logger.Log(f'delete_submission')

        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return
        name = keyUtil.KeyFromAuthor(ctx.author)

        if name != 'DFXLuna#4329' and name != 'MattGrant117#1885':
            await ctx.send("You are not authorized to use this command. Contact Matt Grant if you think there is an error.")
            return

        if await self.submissionDb.DeleteSubmission(uuid):
            grading = self.bot.get_cog('GradingCog')
            if grading is not None:
                await grading.DeleteSubmission(uuid)
            else:
                self.logger.Log("Grading was none")
            await ctx.send(f'Successfully deleted submission {uuid}')
        else:
            await ctx.send(f'Could not delete {uuid}')
        return

    @commands.command()
    async def open_submissions(self, ctx):
        'Open submissions and begin the contest'
        self.logger.Log(f'open_submissions')

        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return
        name = keyUtil.KeyFromAuthor(ctx.author)

        if name != 'DFXLuna#4329' and name != 'MattGrant117#1885':
            await ctx.send("You are not authorized to use this command. Contact Matt Grant if you think there is an error.")
            return

        self.submissionsOpen = True
        ts = datetime.datetime.now()
        await ctx.send(f'Submissions are now open. Current time MTN is [{ts}]')

    @commands.command()
    async def close_submissions(self, ctx):
        'Close submissions and end the contest'
        self.logger.Log(f'close_submissions')

        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return
        name = keyUtil.KeyFromAuthor(ctx.author)

        if name != 'DFXLuna#4329' and name != 'MattGrant117#1885':
            await ctx.send("You are not authorized to use this command. Contact Matt Grant if you think there is an error.")
            return

        self.submissionsOpen = False

        ts = datetime.datetime.now()
        await ctx.send(f'Submissions are now closed. Current time MTN is [{ts}]')

    async def VerifyFileName(self, fileName, problemNumber):
        result = re.match('^prob([0-9][0-9])\.(py2|py3|java|js|c|cpp|zip)$', fileName)
        if result == None:
            return False
        if int(result.group(1)) != problemNumber:
            return False
        return True