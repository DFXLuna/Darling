
import discord
import keyUtil
import roleUtil
import asyncio
from discord.ext import commands

class ScoringCog(commands.Cog):
    def __init__(self, submissionDb, registrationDb, bot, logger):
        self.num_problems = 31
        self.submissionDb = submissionDb
        self.registrationDb = registrationDb
        self.bot = bot
        self.logger = logger
        self.pointValues = [ x for x in range(self.num_problems) ]

    @commands.command()
    async def team_score(self, ctx):
        'Gets the score for your team'
        self.logger.Log('team_score')
        if not await roleUtil.IsValidDMContext(ctx, self.bot):
            return
        submissions = await self.submissionDb.GetTeamSubmissions(await self.registrationDb.GetEntry(keyUtil.KeyFromAuthor(ctx.author)))
        score = 0
        displayString = f'Passed problems: '
        for entry in submissions:
            if entry.IsPass():
                score += self.pointValues[entry.GetProblemNumber()]
                displayString += f'{entry.GetProblemNumber():02}, '
        displayString += f'\nScore: **{score}**'
        await ctx.send(displayString)
    
    @commands.command()
    async def point_values(self, ctx):
        'Show the scores assigned to each problem'
        self.logger.Log('point_values')

        if not await roleUtil.IsValidDMContext(ctx, self.bot):
            return

        displayString = "```\nProblem | Point Value\n"
        for i in range(self.num_problems):
            displayString += f'{i:02}      | {self.pointValues[i]}\n'
        displayString += '```'
        await ctx.send(displayString)