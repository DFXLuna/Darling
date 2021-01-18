def IsJudge(ctxRoles):
    for role in ctxRoles:
        if role.name == "Judge" or role.name == "Volunteer" or role.name == "Admin":
            return True
    return False

# For determining if a user is a judge in the DM context
def IsJudgeById(bot, id):
    return IsJudge(bot.get_guild(780551282317328434).get_member(id).roles)