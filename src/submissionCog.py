import discord
import keyUtil
import roleUtil
import re
from discord.ext import commands

class SubmissionCog(commands.Cog):
    def __init__(self, bot, logger, registrationDb, submissionDb):
        self.bot = bot
        self.logger = logger
        self.registrationDb = registrationDb
        self.submissionDb = submissionDb

    @commands.command()
    async def submit(self, ctx, problemNumber):
        'Submit a solution to the given problem number. You must attach your submission file to the message. Mutiple files must be submitted as a zip archive. You must DM CodeWarsBot to use this command Syntax: `$submit <problemNumber>`'
        if isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author != self.bot.user:
            self.logger.Log(f'submit {ctx.author} {problemNumber}')

            submitter = keyUtil.KeyFromAuthor(ctx.author)
            teamNumber = await self.registrationDb.GetEntry(submitter)

            if teamNumber is None:
                await ctx.send(f'{submitter} is not registered to a team. Please use the `$register <teamNumber>` command to register yourself to your team.')
                return

            if len(ctx.message.attachments) == 0:
                await ctx.send(f'No attachment found, please attach your submission files to the command message. Multiple files may be submitted as a zip archive.')
                return

            if len(ctx.message.attachments) > 1:
                await ctx.send(f'More than one attachment detected. Multiple files must be submitted as a zip archive.')
                return

            if await self.submissionDb.SubmissionAlreadyInProgress(teamNumber, int(problemNumber)):
                await ctx.send(f'team #{teamNumber} has already submitted problem {problemNumber}. Please wait for the judges to judge your submission before resubmitting.')
                return

            if not await self.VerifyFileName(ctx.message.attachments[0].filename, int(problemNumber)):
                await ctx.send(f'Submission filename is incorrect, filename format is `probXX.ext` where `XX` is the problem number with a leading zero for single digit problem numbers and `ext` is one of `py2` `py3` `java` `js` `c` `cpp` `zip`. Additionally, make sure the problem number of the attachment matches the one in the command.')
                return

            await ctx.send(f'Submission of problem {problemNumber} for team #{teamNumber} received. It has been forwarded to the judges for grading.')

            await self.submissionDb.AddSubmission(keyUtil.KeyFromAuthor(ctx.author), teamNumber, int(problemNumber), ctx.message.attachments[0].url, ctx.author.id)

            for attachment in ctx.message.attachments:
                await ctx.send(f'Attachment receipt:\nID {attachment.id}\nSize: {attachment.size}\nFilename: {attachment.filename}\nURL: {attachment.url}')
        else:
            await ctx.send(f'You must direct message CodeWarsBot to use that command')

    @commands.command()
    async def list_submissions(self, ctx):
        'Lists all submissions currently in the database'
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
        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return

        entries = await self.submissionDb.GetUngradedSubmissions()
        displayString = 'Ungraded Submissions:\n'
        for entry in entries:
            displayString += f'> Problem: {entry.GetProblemNumber()}, team: {entry.GetTeamNumber()}\n'

        await ctx.send(displayString)

    @commands.command()
    async def list_team_submissions(self, ctx):
        'Lists all submissions for a team'
        if not await roleUtil.IsValidDMContext(ctx, self.bot):
            return

        teamNumber = await self.registrationDb.GetEntry(keyUtil.KeyFromAuthor(ctx.author))
        entries = await self.submissionDb.GetTeamSubmissions(teamNumber)
        displayString = f"Team #{teamNumber} Submissions:\n"
        for entry in entries:
            displayString += f'> Problem: {entry.GetProblemNumber()}, status: {entry.GetGradeStatus()}\n'

        await ctx.send(displayString)

    async def VerifyFileName(self, fileName, problemNumber):
        result = re.match('^prob([0-9][0-9])\.(py2|py3|java|js|c|cpp|zip)$', fileName)
        if result == None:
            return False
        if int(result.group(1)) != problemNumber:
            return False
        return True