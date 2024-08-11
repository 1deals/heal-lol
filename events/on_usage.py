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

class on_usage(Cog):
    def __init__(self, bot: Heal):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx: Context):
        check = await self.bot.pool.fetchrow("SELECT * FROM usage")
        amount = check["amount"]

        await self.bot.pool.execute('UPDATE usage SET amount = $1', amount+1)

async def setup(bot: Heal):
    await bot.add_cog(on_usage(bot))