def IsJudge(ctxRoles):
    for role in ctxRoles:
        if ctxRoles.name == "Judge" or ctxRoles.name == "Volunteer" or ctxRoles.name == "Admin":
            return True
    return false