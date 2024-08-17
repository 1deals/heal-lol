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

class healboost(Cog):
    def __init__(self, bot: Heal):
        self.bot = bot

    @commands.Cog.listener("on_member_update")
    async def on_member_boost(self, before: discord.Member, after: discord.Member): 
        if before.guild.id == 1244403114447212564:
            if before.guild.premium_subscriber_role not in before.roles and after.guild.premium_subscriber_role in after.roles:  
                await self.bot.pool.execute("INSERT INTO premium (user_id) VALUES ($1)", before.id)
                await before.add_roles(1273953446831325206)
                embed= discord.Embed(description=f"> You have been granted premium for the duration of your boost(s), when you unboost your premium will be automatically removed.", color=Colors.BASE_COLOR)
                await before.send(embed=embed)
    
    @commands.Cog.listener("on_member_update")
    async def on_boost_moved(self, before: discord.Member, after: discord.Member):
        if before.guild.id ==1244403114447212564:
            if before.guild.premium_subscriber_role in before.roles and after.guild.premium_subscriber_role not in after.roles:
                await self.bot.pool.execute("DELETE FROM premium WHERE user_id = $1", after.id)
                await after.remove_roles(1273953446831325206)
                embed= discord.Embed(description=f"> Your premium access has been revoked for transferring your boosts.", color=Colors.BASE_COLOR)
                await before.send(embed=embed)

async def setup(bot: Heal) -> None:
    await bot.add_cog(healboost(bot))