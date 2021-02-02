import discord
import registrationDatabase as r
import submissionDatabase as s
import logger as l
import registrationCog
import submissionCog
import adminCog
import gradingCog
import scoringCog
import helpCog
import os
import sys
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    log.LogToConsole('Started')
    log.Log(f'Logged in as {bot.user.name}')

log = l.Logger(useStdOut=True)

registrationDbFilename = 'RegistrationDb.csv'
reg = r.RegistrationDatabase(registrationDbFilename, log)

submissionDbFilename =  'SubmissionDb.csv'
sub = s.submissionDatabase(submissionDbFilename, log)

token = os.getenv('BOT_TOKEN')
if token == None:
    log.LogToConsole('BOT_TOKEN environment variable not found')
else:
    
    bot.add_cog(registrationCog.RegistrationCog(bot, log, reg))
    bot.add_cog(submissionCog.SubmissionCog(bot, log, reg, sub))
    bot.add_cog(gradingCog.GradingCog(sub, bot, log))
    bot.add_cog(helpCog.HelpCog(bot, log))
    bot.add_cog(scoringCog.ScoringCog(sub, reg, bot, log))
    #bot.add_cog(adminCog.AdminCog())
    try:
        bot.run(token)
    except:
        reg.Flush()
        sub.SyncFlush()
        sys.exit(1)

reg.Flush()
sub.SyncFlush()

