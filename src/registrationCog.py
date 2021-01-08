import discord
import registrationDatabase as r
import logger as l
from discord.ext import commands

class RegistrationCog(commands.Cog):
    def __init__(self, bot, logger, registrationDb):
        self.bot = bot
        self.logger = logger
        self.registrationDb = registrationDb

    def KeyFromAuthor(self, ctxAuthor):
        return ctxAuthor.name + '#' + ctxAuthor.discriminator

    @commands.command()
    async def register(self, ctx, teamNumber: int):
        "Register yourself to a team, removes any other registration"
        if isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author != self.bot.user:
            try:
                self.logger.Log(f'register {ctx.author}')
                
                val = self.registrationDb.GetEntry(self.KeyFromAuthor(ctx.author))
                if val is not None:
                    await ctx.send(f'{ctx.author} is already registered to {val}. Replacing that registration with {teamNumber}')

                self.registrationDb.Register(self.KeyFromAuthor(ctx.author), teamNumber)
                await ctx.send(f'Registered {ctx.author}')
            except Exception as e:
                await ctx.send('USAGE: $register [teamNumber]\ne.g. $register 1234')
                await ctx.send(e.args)
            return
        else:
            await ctx.send(f'You must direct message CodeWarsBot to use that command')

    @commands.command()
    async def unregister(self, ctx):
        "Remove your registration from a team"
        if isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author != self.bot.user:
            try:
                self.registrationDb.Unregister(self.KeyFromAuthor(ctx.author))
                self.logger.Log(f'unregister {ctx.author}')
                await ctx.send(f'unregistered {ctx.author}')
            except Exception as e:
                await ctx.send(e.args)
            return
        else:
            await ctx.send(f'You must direct message CodeWarsBot to use that command')

    @commands.command()
    async def check_registration(self, ctx):
        "Check which team you are registered to"
        if isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author != self.bot.user:
            self.logger.Log(f'check_registration {ctx.author}')
            try:
                val = self.registrationDb.GetEntry(self.KeyFromAuthor(ctx.author))
                if val is not None:
                    await ctx.send(f'{ctx.author} is registered to {val}')
                else:
                    await ctx.send(f'{ctx.author} is not registered')
            except Exception as e:
                await ctx.send(e.args)
            return
        else:
            await ctx.send(f'You must direct message CodeWarsBot to use that command')