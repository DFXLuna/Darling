import discord
import registration as r
import datetime
import os

from discord.ext import commands
bot = commands.Bot(command_prefix="$")
reg = r.Registration()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def register(ctx, teamNumber: int):
    "Register yourself to a team, removes any other registration"
    try:
        ts = datetime.datetime.now()
        print(f'[{ts}]: register {ctx.author}')
        reg.Register(ctx.author, teamNumber)
        await ctx.send(f'Registered {ctx.author}')
    except Exception as e:
        await ctx.send('USAGE: $register [teamNumber]\ne.g. $register 1234')
        await ctx.send(e.args)
    return

@bot.command()
async def unregister(ctx):
    "Remove your registration from a team"
    try:
        ts = datetime.datetime.now()
        reg.Unregister(ctx.author)
        await ctx.send(f'unregistered {ctx.author}')
    except Exception as e:
        await ctx.send(e.args)
    return

@bot.command()
async def check_registration(ctx):
    "Check which team you are registered to"
    ts = datetime.datetime.now()
    print(f'[{ts}]: check_registration {ctx.author}')
    try:
        val = reg.GetEntry(ctx.author)
        if val is not None:
            await ctx.send(f'{ctx.author} is registered to {val}')
        else:
            await ctx.send(f'{ctx.author} is not registered')
    except Exception as e:
        await ctx.send(e.args)
    return


bot.run(os.getenv('BOT_TOKEN'))