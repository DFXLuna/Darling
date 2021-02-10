import numProblems
import discord
import keyUtil
import roleUtil
import asyncio
from discord.ext import commands

class ScoringCog(commands.Cog):
    def __init__(self, submissionDb, registrationDb, bot, logger):
        self.num_problems = numProblems.num_problems
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
        
        score, passedProblems = await self.GetTeamScore(await self.registrationDb.GetEntry(keyUtil.KeyFromAuthor(ctx.author)))
       
        displayString = f'Passed problems: '
        for entry in passedProblems:
            displayString += f'{entry:02}, '
        
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

    @commands.command()
    async def change_point_value(self, ctx, problemNumber, pointValue):
        'Change the point value of a given problem. This only persists through the current session.'
        self.logger.Log(f'change_point_value')

        if not await roleUtil.IsValidJudgeContext(ctx, self.bot):
            return
        name = keyUtil.KeyFromAuthor(ctx.author)

        if name != 'DFXLuna#4329' and name != 'MattGrant117#1885':
            await ctx.send("You are not authorized to use this command. Contact Matt Grant if you think there is an error.")
            return

        self.pointValues[int(problemNumber)] = int(pointValue)
        await ctx.send(f'Point value of problem #**{problemNumber}** is now **{self.pointValues[int(problemNumber)]}**')

    @commands.command()
    async def event_scores(self, ctx):
        'Shows the current scores for all teams.'
        self.logger.Log('event_scores')

        if not await roleUtil.IsValidDMContext(ctx, self.bot):
            return

        teamScores = {}
        for team in await self.registrationDb.GetAllTeamNumbers():
            teamScores[team] = await self.GetTeamScore(team)

        sortedEntries = sorted(teamScores.items(), key=lambda item: item[1][0], reverse=True)

        displayString = f'```\nTeam | Score | Problems\n'
        for entry in sortedEntries:
            displayString += f'{entry[0]:04} | {entry[1][0]: 03}   | {entry[1][1]}\n'
        displayString += '```'
        await ctx.send(displayString)

    # returns (score, passed problem numbers)
    async def GetTeamScore(self, team):
        score = 0
        passedProblems = []
        submissions = await self.submissionDb.GetTeamSubmissions(team)

        for entry in submissions:
            if entry.IsPass():
                score += self.pointValues[entry.GetProblemNumber()]
                passedProblems.append(entry.GetProblemNumber())
        return (score, passedProblems)

