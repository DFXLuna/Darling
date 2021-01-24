import discord

def IsJudge(ctxRoles):
    for role in ctxRoles:
        if role.name == "Judge" or role.name == "Volunteer" or role.name == "Admin":
            return True
    return False

# For determining if a user is a judge in the DM context
async def IsJudgeById(bot, id):
    guild = bot.get_guild(780551282317328434)
    member = guild.get_member(id)
    if member == None:
        member = await guild.fetch_member(id)
    return IsJudge(member.roles)

# Returns a user(NOT a member). Will query the API if not in cache
async def GetUserById(bot, id):
    member = bot.get_user(id)
    if member == None:
        member = await bot.fetch_member(id)
    return member

async def IsValidJudgeContext(ctx, bot):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        if not await IsJudgeById(bot, ctx.author.id):
            await ctx.send(f'You do not have permission to use this command.')
            return False
    elif ctx.channel.name != 'judge-grading':
        if IsJudge(ctx.author.roles):
            await ctx.send('This command may only be used in Judge DMs or `judge-grading`')
        else:
            await ctx.send('You do not have permission to use this command')
        return False
    return True

async def IsValidDMContext(ctx, bot):
    if not isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author != bot.user:
        await ctx.send('You must use this command in a direct message to CodeWarsBot')
        return False
    return True