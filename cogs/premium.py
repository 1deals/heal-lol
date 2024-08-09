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
    is_owner,
    group
)
from typing import Union
from discord.ext.tasks import loop
from discord import Member, Guild, Object, User
from asyncio import gather
import uwuipy
import logging

from tools.heal import Heal
from tools.managers.context import Context, Emojis, Colors


class Premium(Cog):
    def __init__(self, bot: Heal) -> None:
        self.bot = bot

    @group(
        name = "selfprefix",
        description = "Selfprefix settings.",
        invoke_without_command = True
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def selfprefix(self, ctx: Context):
        return await ctx.send_help(ctx.command)
    
    @selfprefix.command(
        name = "set",
        aliases = ["add", "use"],
        description = "Set your selfprefix"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def selfprefix_set(self, ctx: Context, *, prefix: str = None):
        if prefix is None:
            return await ctx.send_help(ctx.command)
        
        if len(prefix) > 10:
            return await ctx.deny(f"Your **selfprefix** cannot be more than `10` characters long.")

        await self.bot.pool.execute(
            """
            INSERT INTO selfprefix (user_id, prefix)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET prefix = $2
            """,
            ctx.author.id, prefix
        )
        await ctx.approve(f"Your **selfprefix** has been set to **`{prefix}`**")

    @selfprefix.command(
        name = "remove",
        aliases = ["delete", "del", "clear"],
        description = "Delete your selfprefix."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def selfprefix_remove(self, ctx: Context):
        check = await self.bot.pool.fetchval("SELECT prefix FROM selfprefix WHERE user_id = $1", ctx.author.id)
        if not check:
            return await ctx.deny(f"You dont have a **selfprefix** setup.")
        else:
            await self.bot.pool.execute("DELETE FROM selfprefix WHERE user_id = $1", ctx.author.id)
            return await ctx.approve("Removed your **selfprefix**.")



    
    
async def setup(bot: Heal) -> None:
    await bot.add_cog(Premium(bot))