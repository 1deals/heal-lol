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
import uwuipy
import logging

from tools.heal import Heal
from tools.managers.context import Context, Emojis, Colors

def uwuify_text(text: str) -> str: 
    uwu_converter = uwuipy.uwuipy()
    return uwu_converter.uwuify(text)

class Premium(Cog):
    def __init__(self, bot: Heal) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message): 
        if not message.guild: 
            return
        if isinstance(message.author, discord.User): 
            return
        
        check = await self.bot.pool.fetchrow(
            "SELECT * FROM uwulock WHERE guild_id = $1 AND user_id = $2", 
            message.guild.id, message.author.id
        )
        
        if check: 
            try: 
                await message.delete()


                uwuified_content = uwuify_text(message.clean_content)
                webhooks = await message.channel.webhooks()

                if not webhooks:
                    webhook = await message.channel.create_webhook(
                        name=f"heal UwUlock", reason="UwUlocked"
                    )
                else:
                    webhook = webhooks[0]

                await webhook.send(
                    content=uwuified_content, 
                    username=message.author.name, 
                    avatar_url=message.author.display_avatar.url
                )

            except Exception as e:
                logging.error(f"Failed to process uwulock message: {e}")

    @commands.command(
        name = "uwulock",
        description = "UwUlock a user."
        )
    @commands.has_permissions(manage_messages = True)
    async def uwulock(self, ctx: Context, *, member: discord.Member): 
        if member.bot: 
            return await ctx.warn("You can't **uwulock** a bot")
        check = await self.bot.pool.fetchrow("SELECT user_id FROM uwulock WHERE user_id = $1 AND guild_id = $2", member.id, ctx.guild.id)    
        if check is None: 
            await self.bot.pool.execute("INSERT INTO uwulock VALUES ($1,$2)", ctx.guild.id, member.id)
            return await ctx.approve(f"{member.mention} is now **uwulocked**!") 
        else: 
            await self.bot.pool.execute("DELETE FROM uwulock WHERE user_id = $1 AND guild_id = $2", member.id, ctx.guild.id)    
        return await ctx.approve(f"{member.mention} is no longer **uwulocked**!") 

    
async def setup(bot: Heal) -> None:
    await bot.add_cog(Premium(bot))