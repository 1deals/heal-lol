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

def get_ordinal(number):
        if 10 <= number % 100 <= 20:
            suffix = "th"
        else:
            suffixes = {1: "st", 2: "nd", 3: "rd"}
            suffix = suffixes.get(number % 10, "th")
        return f"{number}{suffix}"

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
        try:
            total_channels = 0
            for guild in self.bot.guilds:
                    
                total_channels += len(guild.channels)
            uptime = self.bot.uptime
            embed = discord.Embed(timestamp=ctx.message.created_at, colour=Colors.BASE_COLOR)
            embed.add_field(name = f"**{self.bot.user.name}'s statistics**", value = f"**{len(self.bot.guilds)}** guilds \n**{sum(g.member_count for g in self.bot.guilds)}** users \n**{total_channels}** channels", inline = False)
            embed.add_field(name = "**Bot**", value = f"**{len(set(command for command in self.bot.walk_commands()if not command.cog_name == 'Jishaku'))}** commands \nwebsocket latency: **{round(self.bot.latency * 1000)} ms** \nuptime: **{uptime}**", inline = False)
            embed.set_author(name = self.bot.user.display_name, icon_url = self.bot.user.avatar)
            embed.set_thumbnail(url = self.bot.user.avatar)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e) 

    @command(
        name = "ping",
        aliases = ["heartbeat", "latency", "websocket"],
        usage = "ping"
    )
    @cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx: Context):
        list = ["china", "north korea", "your ip", "localhost", "heal", "discord", "your mom", 'horny asian women', 'discord.com', 'google.com', 'healbot.lol', 'instagram', 'onlyfans.com', '911', 'no one', 'tiktok', 'github', 'lucky bro']

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


    @commands.command(
        name="userinfo",
        aliases=["ui", "whois"],
        description="Get info about a user."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx: Context, *, user: discord.Member = None):
        user = user or ctx.author

        title = f"{user.name}"

        
        if user.id == 187747524646404105: # me
            title += " <:owner:1270728554388394086> <:staff:1270729949686534206> <:dev:1270730817458405468> "
        if user.id == 392300135323009024: #xur
            title += " <:staff:1270729949686534206> <:dev:1270730817458405468>"
        if user.id == 461914901624127489: # logan
            title += " <:zzmilklove2:1270873236841693267> <:staff:1270729949686534206> <:dev:1270730817458405468>"
        if user.id == 1259443225542918218: # menace 
            title += " <a:menacemonkey:1271184769836912680> <:staff:1270729949686534206>"
        if user.id == 1261756025275547719: # neca
            title += " <:staff:1270729949686534206>"

        embed = discord.Embed(
            title=title,
            description=f"",
            color = Colors.BASE_COLOR
        )
        embed.add_field(name="Created", value=format_dt(user.created_at, style='f'), inline=True)

        if user.joined_at:
            all_members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            position = all_members.index(user) + 1

            roles = [role.mention for role in user.roles if role.id != ctx.guild.id]
            roles_list = ", ".join(roles) if roles else "None"

            join_position_ordinal = get_ordinal(position)
            embed.add_field(name=f"Joined {join_position_ordinal}", value=f"{format_dt(user.joined_at, style='f')}", inline=True)
            embed.add_field(name="Roles", value=roles_list, inline=False)
        else:
            embed.add_field(name="Joined", value="N/A", inline=True)
            embed.add_field(name="Roles", value="N/A", inline=False)
        
        embed.set_thumbnail(url=user.avatar.url)

        await ctx.send(embed=embed)

async def setup(bot: Heal):
    await bot.add_cog(Information(bot))
