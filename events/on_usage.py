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
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        ctx = await self.bot.get_context(message)

        if ctx.command is not None:
            await self.bot.pool.execute("UPDATE usage SET amount = amount + 1")
            await self.bot.process_commands(message)

async def setup(bot: Heal):
    await bot.add_cog(on_usage(bot))