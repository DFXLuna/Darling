import discord
import keyUtil
from discord.ext import commands


class AdminCog(commands.Cog):
    def __init__(self, adminRoles=['@admin','@judge', '@volunteer']):
        self.adminRoles = adminRoles