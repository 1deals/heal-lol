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

class onready(Cog):
    def __init__(self, bot: Heal):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): 
      online = "<:MobileOnline:1274794338366263296>"
      log = self.bot.get_channel(1271137690649231423)
      embed = discord.Embed(color=Colors.BASE_COLOR, description=f"{online} {self.bot.user.name} is back up, serving `{len(self.bot.guilds)}` servers with about `{len(set(self.bot.get_all_members()))}` members at `{round(self.bot.latency * 1000)}ms`")
      await log.send(embed=embed) 

async def setup(bot: Heal) -> None:
    await bot.add_cog(onready(bot))