import discord
import asyncio
import random
import aiohttp
import uwuipy
import requests

from discord.ext import commands
from discord.ext.commands       import command, group, BucketType, cooldown, has_permissions, hybrid_command, hybrid_group

from tools.managers.context import Context, Colors
from tools.heal import Heal
from typing import Union

class Donor(commands.Cog):
    def __init__(self, bot: Heal):
        self.bot = bot

    @command(
        name = "uwulock",
        description = "Uwulocks a user."
    )
    @cooldown(1, 5, commands.BucketType.user)
    async def uwulock(self, ctx: Context, *, user: discord.Member):
        if user.bot:
            return await ctx.warn("I cannot **uwulock** a bot.")
        
        check = await self.bot.pool.fetchrow("SELECT user_id FROM uwulock WHERE user_id = $1 AND guild_id = $2")