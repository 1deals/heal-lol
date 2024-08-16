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
from random import choice

class Economy(commands.Cog):
    def __init__(self, bot: Heal):
        self.bot = bot

    @commands.command(
        name="balance",
        aliases=["bal"],
        description="Get the balance of a user."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx: commands.Context, *, user: Union[discord.Member, discord.User] = None):
        if user is None:
            user = ctx.author

        data = await self.bot.pool.fetchrow("SELECT cash, bank FROM economy WHERE user_id = $1", user.id)
        cash = data['cash'] if data and data['cash'] is not None else 0
        bank = data['bank'] if data and data['bank'] is not None else 0
        total = cash + bank

        embed = discord.Embed(title=f"{user.name}'s balance", description="", color=Colors.BASE_COLOR)
        embed.add_field(name="Total", value=f"${total:,}", inline=True)
        embed.add_field(name="Cash", value=f"${cash:,}", inline=True)
        embed.add_field(name="Bank", value=f"${bank:,}", inline=True)

        await ctx.send(embed=embed)

    @commands.command(
        name="work",
        description="Work to gain money.",
    )
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def work(self, ctx: Context):
        jobs = ["mcdonalds", "kfc", "pizzahut", "secretary", "fire fighter", "police man", "nurse", "coder", "teacher"]
        randomjob = random.choice(jobs)

       
        data = await self.bot.pool.fetchrow("SELECT cash FROM economy WHERE user_id = $1", ctx.author.id)
        cash = data['cash'] if data and data['cash'] is not None else 0

        
        earnt = random.randint(10, 250)
        newbal = cash + earnt

        await self.bot.pool.execute("UPDATE economy SET cash = $1 WHERE user_id = $2", newbal, ctx.author.id)

        await ctx.neutral(f"You earned **${earnt}** working as a **{randomjob}**. Your new balance is **${newbal:,}**")

async def setup(bot: Heal):
    return await bot.add_cog(Economy(bot))