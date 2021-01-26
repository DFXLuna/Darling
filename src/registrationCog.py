import discord
import registrationDatabase as r
import logger as l
import keyUtil
import roleUtil
from discord.ext import commands

class RegistrationCog(commands.Cog):
    def __init__(self, bot, logger, registrationDb):
        self.bot = bot
        self.logger = logger
        self.registrationDb = registrationDb

    @commands.command()
    async def register(self, ctx, teamNumber: int):
        "Register yourself to a single team, removes any other registrations. Syntax: `$register <teamNumber>`"
        if await roleUtil.IsValidDMContext(ctx, self.bot):
            self.logger.Log(f'register {ctx.author} {teamNumber}')
            
            currentTeamNumber = await self.registrationDb.GetEntry(keyUtil.KeyFromAuthor(ctx.author))
            if currentTeamNumber is not None:
                await ctx.send(f'{ctx.author} is already registered to #{currentTeamNumber}. Replacing that registration with #{teamNumber}')

            await self.registrationDb.Register(keyUtil.KeyFromAuthor(ctx.author), teamNumber)
            await ctx.send(f'Registered {ctx.author} to team #{teamNumber}')
        return

    @commands.command()
    async def unregister(self, ctx, author):
        "Remove your registration from all teams. Name must be in the form `username#number`. This command must be run in judge-grading or in judge DMs."
        if await roleUtil.IsValidJudgeContext(ctx, self.bot):
            await self.registrationDb.Unregister(author)
            self.logger.Log(f'unregister {ctx.author}')
            await ctx.send(f'unregistered {ctx.author}')
        return 

    @commands.command()
    async def check_registration(self, ctx):
        "Check which team you are registered to."
        if await roleUtil.IsValidDMContext(ctx, self.bot):
            self.logger.Log(f'check_registration {ctx.author}')
            teamNumber = await self.registrationDb.GetEntry(keyUtil.KeyFromAuthor(ctx.author))
            if teamNumber is not None:
                await ctx.send(f'{ctx.author} is registered to #{teamNumber}')
            else:
                await ctx.send(f'{ctx.author} is not registered')
        return
