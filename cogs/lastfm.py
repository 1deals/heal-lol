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
from tools.managers.lastfm import FMHandler
from tools.managers.context import Context, Emojis, Colors

class LastFM(Cog):
    def __init__(self, bot: Heal) -> None:
        self.bot = bot
        self.handler = FMHandler

    @commands.group(
        name = "lastfm",
        aliases = ["lf", "fm"],
        description = "Interact with LastFM through heal.",
        invoke_without_command = True
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lastfm(self, ctx: Context):
        return await ctx.send_help(ctx.command)
    
    @lastfm.command(
        name = "login",
        aliases = ["link", "set", "connect"],
        description = "Set your LastFM account."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lastfm_login(self, ctx: Context, *, lfuser: str = None):
        if lfuser is None:
            return await ctx.send_help(ctx.command)
        
        data = await self.bot.pool.fetchrow("SELECT user_id, lfuser FROM lastfm WHERE lfuser = $1",lfuser)


        if data:
            user_id = data['user_id']
            user = self.bot.get_user(user_id) or await self.bot.fetch_user(user_id)
            return await ctx.deny(f"**{lfuser}** has been registered by {user.mention}")
        
        msg = await ctx.neutral("⚙️ Connecting to LastFM..")
        await self.bot.pool.execute(
            """
            INSERT INTO lastfm (user_id, lfuser)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET lfuser = $2
            """,
            ctx.author.id, lfuser
        )
        embed = Embed(description = f"{Emojis.APPROVE} {ctx.author.mention}: Set your **LastFM** user to **{lfuser}**.", color = Colors.LAST_FM)
        await msg.edit(embed=embed)

    @lastfm.command(
        name = "nowplaying",
        description = "Get your LastFM now playing."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lastfm_nowplaying(self, ctx: Context, *, user: Union[discord.Member, discord.User]= None):
        if user is None:
            user = ctx.author

        data = await self.bot.pool.fetchval("SELECT * FROM lastfm WHERE user_id", user.id)
        profile = await self.handler.profile("lastfm_username")
        if self.handler.now_playing:
            return await ctx.lastfm(f"{user.mention} is listening to {self.handler.now_playing}")
        else:
            return await ctx.lastfm(f"{user.mention} is not listening to anything.")

async def setup(bot: Heal):
    await bot.add_cog(LastFM(bot))