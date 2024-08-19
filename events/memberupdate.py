import discord

from discord import Message
from discord.ext import commands
from discord.ext.commands import (
    Cog,
    hybrid_group,
    group
)
from tools.heal import Heal
from tools.managers.context import Context
from tools.configuration import Colors, Emojis
from typing import Union
import asyncio
from tools.managers.embedBuilder import EmbedBuilder, EmbedScript
import logging
import datetime

class memberupdate(Cog):
    def __init__(self, bot: Heal):
        self.bot = bot

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        if before.name == after.name:
            return
        
        timestamp = int(datetime.datetime.now().timestamp())
        
        await self.bot.pool.execute(
            "INSERT INTO names (user_id, oldnames, timestamp) VALUES ($1, $2, $3)",
            before.id, before.name, timestamp
        )

async def setup(bot: Heal) -> None:
    await bot.add_cog(memberupdate(bot))