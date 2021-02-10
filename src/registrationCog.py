import discord
import registrationDatabase as r
import logger as l
import keyUtil
import roleUtil
import asyncio
from discord.ext import commands

class RegistrationCog(commands.Cog):
    def __init__(self, bot, logger, registrationDb):
        self.bot = bot
        self.logger = logger
        self.registrationDb = registrationDb

    @commands.command()
    async def register(self, ctx, teamNumber: int):
        "Register yourself to a single team, removes any other registrations. Syntax: `$register <teamNumber>`"
        self.logger.Log(f'register {ctx.author} {teamNumber}')
        if await roleUtil.IsValidDMContext(ctx, self.bot):
            currentTeamNumber = await self.registrationDb.GetEntry(keyUtil.KeyFromAuthor(ctx.author))
            if currentTeamNumber is not None:
                await ctx.send(f'{ctx.author} is already registered to #{currentTeamNumber}. If you need to change your registration, DM Matt Grant or a judge')
            else:
                await self.registrationDb.Register(keyUtil.KeyFromAuthor(ctx.author), teamNumber)
                await asyncio.gather(
                    self.registrationDb.AsyncFlush(),
                    ctx.send(f'Registered {ctx.author} to team #{teamNumber}')
                )
        return

    @commands.command()
    async def unregister(self, ctx, author):
        "Remove the author's registration from their. Name must be in the form `username#number`. This command must be run in judge-grading or in judge DMs."
        self.logger.Log(f'unregister {ctx.author}')
        if await roleUtil.IsValidJudgeContext(ctx, self.bot):
            await self.registrationDb.Unregister(author)
            await asyncio.gather(
                self.registrationDb.AsyncFlush(),
                ctx.send(f'unregistered {ctx.author}')
            )
        return

    @commands.command()
    async def check_registration(self, ctx):
        "Check which team you are registered to."
        self.logger.Log(f'check_registration {ctx.author}')
        if await roleUtil.IsValidDMContext(ctx, self.bot):
            teamNumber = await self.registrationDb.GetEntry(keyUtil.KeyFromAuthor(ctx.author))
            if teamNumber is not None:
                await ctx.send(f'{ctx.author} is registered to #{teamNumber}')
            else:
                await ctx.send(f'{ctx.author} is not registered')
        return

    @commands.command()
    async def list_registrations(self, ctx):
        self.logger.Log(f'list _registration {ctx.author}')
        if await roleUtil.IsValidJudgeContext(ctx, self.bot):
            displayString = 'Registrations: \n'
            for k, v in (await self.registrationDb.GetAllRegistrations()).items():
                displayString += f'> User: **{k}**, Team: **{v}**\n'
            await ctx.send(displayString)
