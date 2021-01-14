def IsJudge(ctxRoles):
    for role in ctxRoles:
        if role.name == "Judge" or role.name == "Volunteer" or role.name == "Admin":
            return True
    return false