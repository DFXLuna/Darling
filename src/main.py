import discord
import registrationDatabase as r
import logger as l
import registrationCog
import submissionCog
import os

from discord.ext import commands
bot = commands.Bot(command_prefix="$")
log = l.Logger(useStdOut=True)
dbFilename = "db.csv"
reg = r.RegistrationDatabase(dbFilename, log)

@bot.event
async def on_ready():
    log.LogToConsole("Started")
    log.Log(f'Logged in as {bot.user.name}')

# @bot.command()
# async def flush(ctx):
#     reg.Flush()
#     await ctx.send("Flushed to disk")

token = os.getenv('BOT_TOKEN')
if token == None:
    log.LogToConsole("BOT_TOKEN environment variable not found")
else:
    bot.add_cog(registrationCog.RegistrationCog(bot, log, reg))
    bot.add_cog(submissionCog.SubmissionCog(bot, log, reg))
    bot.run(token)

reg.Flush()