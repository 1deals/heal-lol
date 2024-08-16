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

class Economy(commands.Cog):
    def __init__(self, bot: Heal):
        self.bot = bot

    @command(
        name = "balace",
        aliases = ["bal"],
        description = "Get the balance of a user."
    )
    @cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx: Context, * , user: Union[discord.Member, discord.User] = None):
        if user is None:
            user = ctx.author

        data = self.bot.pool.fetchval("SELECT * FROM economy WHERE user_id = $1", user.id)
        cash = data['cash'] if data and data['cash'] is not None else 0
        bank = data['bank'] if data and data['bank'] is not None else 0
        total = cash + bank

        embed = discord.Embed(title = f"{user.name}'s balance.", description = f"", color = Colors.BASE_COLOR)
        embed.add_field(name = "Total:", value = "$" + total, inline = True)
        embed.add_field(name = "Cash", value = "$" + cash, inline = True)
        embed.add_field(name = "Bank", value= "$" + bank, inline = True)

        await ctx.send(embed=embed)

async def setup(bot: Heal):
    return await bot.add_cog(Economy(bot))