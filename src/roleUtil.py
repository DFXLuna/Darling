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