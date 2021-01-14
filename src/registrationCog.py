import discord
import registrationDatabase as r
import logger as l
import keyUtil
from discord.ext import commands

class RegistrationCog(commands.Cog):
    def __init__(self, bot, logger, registrationDb):
        self.bot = bot
        self.logger = logger
        self.registrationDb = registrationDb

    @commands.command()
    async def register(self, ctx, teamNumber: int):
        "Register yourself to a single team, removes any other registrations. Syntax: `$register <teamNumber>`"
        if isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author != self.bot.user:
            try:
                self.logger.Log(f'register {ctx.author} {teamNumber}')
                
                currentTeamNumber = await self.registrationDb.GetEntry(keyUtil.KeyFromAuthor(ctx.author))
                if currentTeamNumber is not None:
                    await ctx.send(f'{ctx.author} is already registered to #{currentTeamNumber}. Replacing that registration with #{teamNumber}')

                await self.registrationDb.Register(keyUtil.KeyFromAuthor(ctx.author), teamNumber)
                await ctx.send(f'Registered {ctx.author} to team #{teamNumber}')
            except Exception as e:
                await ctx.send('USAGE: $register [teamNumber]\ne.g. $register 1234')
                await ctx.send(e.args)
            return
        else:
            await ctx.send(f'You must direct message CodeWarsBot to use that command')

    @commands.command()
    async def unregister(self, ctx):
        "Remove your registration from all teams."
        if isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author != self.bot.user:
            try:
                await self.registrationDb.Unregister(keyUtil.KeyFromAuthor(ctx.author))
                self.logger.Log(f'unregister {ctx.author} from all teams')
                await ctx.send(f'unregistered {ctx.author}')
            except Exception as e:
                await ctx.send(e.args)
            return
        else:
            await ctx.send(f'You must direct message CodeWarsBot to use that command')

    @commands.command()
    async def check_registration(self, ctx):
        "Check which team you are registered to."
        if isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author != self.bot.user:
            self.logger.Log(f'check_registration {ctx.author}')
            try:
                teamNumber = await self.registrationDb.GetEntry(keyUtil.KeyFromAuthor(ctx.author))
                if teamNumber is not None:
                    await ctx.send(f'{ctx.author} is registered to #{teamNumber}')
                else:
                    await ctx.send(f'{ctx.author} is not registered')
            except Exception as e:
                await ctx.send(e.args)
            return
        else:
            await ctx.send(f'You must direct message CodeWarsBot to use that command')
