import discord
import keyUtil
from discord.ext import commands

class SubmissionCog(commands.Cog):
    def __init__(self, bot, logger, registrationDb):
        self.bot = bot
        self.logger = logger
        self.registrationDb = registrationDb

    @commands.command()
    async def submit(self, ctx, problemNumber: int):
        'Submit a solution to the given problem number. You must attach your submission file to the message. Mutiple files may be submitted as a zip archive. Syntax: `$submit <problemNumber>`'
        if isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author != self.bot.user:
            self.logger.Log(f'submit {ctx.author} {problemNumber}')
            
            teamNumber = self.registrationDb.GetEntry(keyUtil.KeyFromAuthor(ctx.author))
            if teamNumber is None:
                await ctx.send(f'{ctx.author} is not registered to a team. Please use the `$register <teamNumber>` command to register yourself to your team.')
                return
            if len(ctx.message.attachments) == 0:
                await ctx.send(f'No attachment found, please attach your submission files to the command message. Multiple files may be submitted as a zip archive.')
                return
            await ctx.send(f'Submission of problem {problemNumber} for team #{teamNumber} received, processing...')
        else:
            await ctx.send(f'You must direct message CodeWarsBot to use that command')