import discord
import os
import sys
import aiohttp

from discord import Message, Embed
from discord.ext import commands
from discord.ext.commands import (
    Cog,
    command,
    hybrid_command,
    is_owner
)
from typing import Union
from discord.ext.tasks import loop
from discord import Member, Guild, Object, User
from asyncio import gather
import traceback

from tools.heal import Heal
from tools.managers.context import Context, Emojis, Colors

class Owner(Cog):
    def __init__(self, bot: Heal) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, guild: discord.Guild, user: Union[discord.Member, discord.User]):

        if isinstance(user, discord.User):
            return
                
        for role in user.roles:
            await self.bot.pool.execute('INSERT INTO restore (guild_id, user_id, role) VALUES ($1, $2, $3)', user.guild.id, user.id, role.id)

async def setup(bot: Heal):
    await bot.add_cog(Member(bot))