import discord
import psutil
import sys
import time
import random
from random import choice

from tools.managers.context     import Context
from discord.ext.commands       import command, group, BucketType, cooldown, has_permissions
from tools.configuration        import Emojis, Colors
from tools.paginator            import Paginator
from discord.utils              import format_dt
from discord.ext                import commands
from tools.heal                 import Heal
from typing import Union

class Information(commands.Cog):
    def __init__(self, bot: Heal) -> None:
        self.bot = bot

    @command(
        name = "botinfo",
        aliases = ["bi", "bot"],
        description = "Get information about the bot."
    )
    @cooldown(1, 5, commands.BucketType.user)
    async def botinfo(self, ctx: Context):
        commands = [command for command in set(self.bot.walk_commands()) if command.cog_name != 'Jishaku']

        embed = discord.Embed(
            title = f"heal",
            color = Colors.BASE_COLOR
        )
        embed.add_field(name="statistics", value=f"> guilds: `{len(self.bot.guilds):,}`\n> users: `{len(self.bot.users):,}`\n> commands: `{len(commands):,}`", inline=False)
        embed.add_field(name="system", value=f"> cpu usage: `{psutil.cpu_percent()}%`\n> ram usage: `{psutil.virtual_memory().percent}%`\n> python version: `{sys.version.split(" (")[0]}`", inline=False)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    @command(
        name = "ping",
        aliases = ["heartbeat", "latency", "websocket"],
        usage = "ping"
    )
    @cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx: Context):
        list = ["china", "north korea", "your ip", "localhost", "heal", "discord", "your mom", 'horny asian women', 'discord.com', 'google.com', 'healbot.lol', 'instagram', 'onlyfans.com', '911', 'no one', 'tiktok', 'github']

        start = time.time()
        message = await ctx.send(content="pong!")
        finished = time.time() - start

        return await message.edit(
            content=f"it took `{int(self.bot.latency * 1000)}ms` to ping **{choice(list)}** (edit: `{finished:.2f}ms`)"
        )

    @command(
        name = "invite",
        aliases = ["inv"],
        usage = "invite"
    )
    @cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx: Context):
        await ctx.send(f"{discord.utils.oauth_url(client_id=self.bot.user.id, permissions=discord.Permissions(8))}")

    @command(
        name = "uptime",
        aliases = ["up"],
        usage = "uptime"
    )
    @cooldown(1, 5, commands.BucketType.user)
    async def uptime(self, ctx: Context):
        await ctx.neutral(f":alarm_clock: I have been **up** for `{self.bot.uptime}`")

    def get_ordinal(number):
        if 10 <= number % 100 <= 20:
            suffix = "th"
        else:
            suffixes = {1: "st", 2: "nd", 3: "rd"}
            suffix = suffixes.get(number % 10, "th")

        return f"{number}{suffix}"
    
    @commands.command(
        name = "userinfo",
        aliases = ["ui", "whois"],
        description = "Get info about a user."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx: Context, *, user: Union[discord.User, discord.Member] = None):
        user = user or ctx.author

        if isinstance(user, discord.User):
            member = ctx.guild.get_member(user.id)
        else:
            member = user

       
        title = f"{user.name}"

        
        if user.id == 187747524646404105:  
            title += " <:owner:1270728554388394086> <:staff:1270729949686534206> <:dev:1270730817458405468> "
        if user.id == 392300135323009024:
            title += " <:staff:1270729949686534206> <:dev:1270730817458405468>"
        if user.id == 461914901624127489:
            title += " <:staff:1270729949686534206> <:dev:1270730817458405468>"

        embed = discord.Embed(
            title=title,
            description=f"{user.name} / {user.display_name}",
            color=Colors.BASE_COLOR 
        )
        embed.add_field(name="Created", value=format_dt(user.created_at, style='f'), inline=True)

        if member is None:
            embed.add_field(name="Joined", value="N/A", inline=True)
            embed.add_field(name="Join Position", value="N/A", inline=False)
            embed.add_field(name="Roles", value="N/A", inline=False)
        else:
            all_members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            position = all_members.index(member) + 1

            roles = [role.mention for role in member.roles if role.id != ctx.guild.id]
            roles_list = ", ".join(roles) if roles else "None"

            embed.add_field(name="Joined", value=f"{format_dt(member.joined_at, style='f')} ({self.get_ordinal(position)})", inline=True)
            embed.add_field(name="Roles", value=roles_list, inline=False)

        embed.set_thumbnail(url=user.avatar.url)

        await ctx.send(embed=embed)

async def setup(bot: Heal):
    await bot.add_cog(Information(bot))
