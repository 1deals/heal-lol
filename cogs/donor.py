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

async def uwulocktext(bot, text: str) -> str:
    uwu = uwuipy.uwuipy()
    return uwu.uwuify(text)

def has_perks():
  async def predicate(ctx: Context):
    check = await ctx.bot.pool.fetchrow(
      "SELECT * FROM premium WHERE user_id = $1",
      ctx.author.id
    )
    if not check:
      await ctx.warn("You need to be a premium user to use this command.")
      return False
    return True
  return commands.check(predicate)

class Donor(commands.Cog):
    def __init__(self, bot: Heal):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def uwuwebhook(self, message: discord.Message):
        if not message.guild: 
            return
        if isinstance(message.author, discord.User):
            return
        
        check = await self.bot.pool.fetchrow("SELECT * FROM uwulock WHERE guild_id = $1 AND user_id = $2", message.guild.id, message.author.id)
        if check:
            try: 
                uwumsg = await uwulocktext(self.bot, message.clean_content)
                await message.delete() 
                
                webhooks = await message.channel.webhooks()
                if len(webhooks) == 0:
                    webhook = await message.channel.create_webhook(name="heal", reason="uwulock")
                else:
                    webhook = webhooks[0]
                
                
                await webhook.send(content=uwumsg, username=message.author.name, avatar_url=message.author.display_avatar.url)
            
            except Exception as e: 
                print(f"Error in uwuwebhook: {e}")

    @command(
        name = "uwulock",
        description = "Uwulocks a user."
    )
    @has_perks()
    @cooldown(1, 5, commands.BucketType.user)
    async def uwulock(self, ctx: Context, *, user: discord.Member):
        if user.bot:
            return await ctx.warn("I cannot **uwulock** a bot.")
        
        check = await self.bot.pool.fetchrow("SELECT user_id FROM uwulock WHERE user_id = $1 AND guild_id = $2", user.id, ctx.guild.id)
        if check is None:
            await self.bot.pool.execute("INSERT INTO uwulock VALUES ($1,$2)", ctx.guild.id, user.id)
            return await ctx.approve(f"I have **uwulocked** {user.mention}!")
        else:
            await self.bot.pool.execute("DELETE FROM uwulock WHERE user_id = $1 AND guild_id = $2", user.id, ctx.guild.id)
            return await ctx.approve(f"{user.mention} is no longer **uwulocked**.")
        
async def setup(bot: Heal):
    return await bot.add_cog(Donor(bot))