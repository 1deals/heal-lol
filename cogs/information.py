import discord
import psutil
import sys
import time
import random
from random import choice
from psutil import Process

from tools.managers.context import Context
from discord.ext.commands import (
    command,
    group,
    BucketType,
    cooldown,
    has_permissions,
    hybrid_command,
    hybrid_group,
)
from discord import Embed
from tools.configuration import Emojis, Colors
from tools.paginator import Paginator
from discord.utils import format_dt
from discord.ext import commands
from tools.heal import Heal
from typing import Union
import datetime
import aiohttp
from tools.managers.embedBuilder import EmbedBuilder, EmbedScript
from tools.configuration import api
from tools.models.statistics import BotStatistics
import os
from discord.ui import View, Button
import googletrans
from googletrans import Translator, LANGUAGES
import humanize
from datetime import datetime, timedelta


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
        self.vc_start_times = {}
        self.process = Process()

    def format_size(self, bytes):
        """Convert bytes to a human-readable format."""
        if bytes >= 1024**3:  # GB
            return f"{bytes / (1024 ** 3):.2f}GB"
        elif bytes >= 1024**2:  # MB
            return f"{bytes / (1024 ** 2):.2f}MB"
        elif bytes >= 1024:  # KB
            return f"{bytes / 1024:.2f}KB"
        else:  # Bytes
            return f"{bytes} Bytes"

    @hybrid_command(
        name="botinfo",
        aliases=["info", "bot", "bi", "about"],
        description="Get information about the bot.",
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def botinfo(self, ctx: Context):
        start_time = datetime.now() - timedelta(seconds=self.bot._uptime)
        formatted_uptime = format_dt(start_time, "R")
        embed = Embed(
            description = f"A **free** multipurpose bot, aimed to make your communities thrive.",
            color = Colors.BASE_COLOR
        )
        embed.add_field(name = "System:", value = f"> **Memory:** `{self.format_size(self.process.memory_info().rss)}` \n> **CPU:** `{self.process.cpu_percent()}%` \n> **Booted:** `{self.bot.uptime} ago`", inline = True)
        embed.add_field(name = "Bot:", value = f"> **Users:** `{len(self.bot.users): ,}` \n> **Guilds:** `{len(self.bot.guilds): ,}` \n> **Commands:** `{len([cmd for cmd in self.bot.walk_commands() if cmd.cog_name != 'Jishaku'])}`", inline = True)
        embed.set_thumbnail(url= self.bot.user.avatar.url)
        return await ctx.reply(embed=embed)

    @hybrid_command(
        name="ping",
        aliases=["websocket", "latency"],
        description="View the bot's latency.",
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ping(self, ctx: Context):
        """
        View the bot's latency
        """
        start = time.time()
        latency_ms = int(self.bot.latency * 1000)
        message = await ctx.send(content="ping...")
        finished = time.time() - start
        edit_ms = round(finished * 1000, 1)
        return await message.edit(content=f"... `{latency_ms}ms` (edit: `{edit_ms}ms`)")
        # return await ctx.reply(f"*...* `{round(self.bot.latency * 1000)}ms`")

    @hybrid_command(name="invite", aliases=["inv"], usage="invite")
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx: Context):
        await ctx.send(
            f"{discord.utils.oauth_url(client_id=self.bot.user.id, permissions=discord.Permissions(8))}"
        )

    @hybrid_command(name="uptime", aliases=["up"], usage="uptime")
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @cooldown(1, 5, commands.BucketType.user)
    async def uptime(self, ctx: Context):
        await ctx.neutral(f":alarm_clock: I have been **up** for `{self.bot.uptime}`")

    @hybrid_command(
        name="userinfo", aliases=["ui", "whois"], description="Get info about a user."
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(
        self, ctx: Context, *, user: Union[discord.Member, discord.User] = None
    ):

        if isinstance(user, int):
            try:
                user = await self.bot.fetch_user(user)
            except discord.NotFound:
                return await ctx.warn("User not found.")
        else:
            user = user or ctx.author

        if isinstance(user, discord.User):
            guild = ctx.guild
            if guild:
                member = guild.get_member(user.id)
                if member:
                    user = member

        description = ""
        title = f"{user.name}"

        if isinstance(user, discord.Member):
            if user.desktop_status == discord.Status.online:
                title += " <:status_computer_online:1291119653095080058>"
            if user.desktop_status == discord.Status.idle:
                title += " <:status_computer_idle:1291124408034922587>"
            if user.desktop_status == discord.Status.dnd:
                title += " <:status_computer_dnd:1291124598271774723>"
            if user.mobile_status == discord.Status.online:
                title += " <:status_phone_online:1291120307863687249>"
            if user.mobile_status == discord.Status.idle:
                title += " <:status_phone_idle:1291124866858090548>"
            if user.mobile_status == discord.Status.dnd:
                title += " <:status_phone_dnd:1291124989495607407>"
            if user.web_status == discord.Status.online:
                title += " <:status_web_online:1291120457872838700>"
            if user.web_status == discord.Status.dnd:
                title += " <:status_web_dnd:1291125457412165755>"
            if user.web_status == discord.Status.idle:
                title += " <:status_web_idle:1291125639235113111>"
            if user.status == discord.Status.invisible:
                title += " <:status_z_offline_invisible:1291125818118115330>"

            if user.premium_since is not None:
                title += " <:boosterbadge:1253988282455556146> "


        data = await self.bot.pool.fetchrow(
            "SELECT * FROM lastfm WHERE user_id = $1", user.id
        )
        if data:
            lastfm_username = data["lfuser"]
            async with aiohttp.ClientSession() as session:
                params = {
                    "method": "user.getRecentTracks",
                    "user": lastfm_username,
                    "api_key": "bc8082588489f949216859abba6e52be",
                    "format": "json",
                    "limit": 1,
                }
                async with session.get(
                    "http://ws.audioscrobbler.com/2.0/", params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "recenttracks" in data and "track" in data["recenttracks"]:
                            track_info = data["recenttracks"]["track"][0]
                            now_playing = (
                                track_info.get("@attr", {}).get("nowplaying") == "true"
                            )
                            if now_playing:
                                track_name = track_info["name"]
                                artist_name = track_info["artist"]["#text"]
                                track_url = track_info["url"]
                                description += f"> {Emojis.LASTFM} **Listening to [{track_name}]({track_url}) by {artist_name}**"

        if not data:
            if user.activities:
                for activity in user.activities:
                    if isinstance(activity, discord.Spotify):
                        description += f"<:spotify:1291106261705818123> Listening to **[{activity.title}]({activity.track_url})** by **`{activity.artist}`**"

        embed = discord.Embed(title=title, description=description)
        if isinstance(user, discord.Member):
            embed.add_field(
                name="Joined:",
                value=f"{discord.utils.format_dt(user.joined_at, style= 'f')}",
                inline=True,
            )
            if user.premium_since is not None:
                embed.add_field(
                    name="Boosted:",
                    value=f"{discord.utils.format_dt(user.premium_since, style='f')}",
                    inline=True,
                )
        embed.add_field(
            name="Created:",
            value=f"{discord.utils.format_dt(user.created_at, style = 'f')}",
            inline=True,
        )
        if isinstance(user, discord.Member):
            if len(user.roles) > 5:
                roles_list = (
                    ", ".join(
                        [role.mention for role in list(reversed(user.roles[1:]))[:5]]
                    )
                    + f" + {len(user.roles) - 5} more"
                )
            else:
                roles_list = ", ".join(
                    [role.mention for role in list(reversed(user.roles[1:]))[:5]]
                )
            embed.add_field(name="Roles", value=roles_list, inline=False)

        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)

    @hybrid_command(
        name="instagram",
        aliases=["insta", "ig"],
        description="Get information about an instagram user.",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def instagram(self, ctx: Context, username: str):
        url = "https://api.fulcrum.lol/instagram"
        params = {"username": username}
        headers = {"Authorization": api.luma}

        def humanize_number(value: int) -> str:
            if value >= 1_000_000:
                return f"{value / 1_000_000:.1f}M"
            elif value >= 1_000:
                return f"{value / 1_000:.1f}K"
            return str(value)

        await ctx.typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    profile_name = data.get("username", "None set.")
                    followers = data.get("followers", "N/A")
                    following = data.get("following", "N/A")
                    bio = data.get("bio", "N/A")
                    verified = data.get("is_verified", False)
                    profile_pic = data.get("avatar_url", None)
                    posts = data.get("posts", None)
                    pronouns = data.get("pronouns", "None set")

                    if isinstance(followers, int):
                        followers = humanize_number(followers)
                    if isinstance(following, int):
                        following = humanize_number(following)

                    title = f"{profile_name}'s profile info"
                    if verified:
                        title += " <:verified:1271542657897992373>"

                    embed = discord.Embed(
                        title=title, description=bio, color=Colors.BASE_COLOR
                    )
                    embed.add_field(name="Followers", value=followers, inline=True)
                    embed.add_field(name="Following", value=following, inline=True)
                    embed.add_field(name="Posts", value=posts, inline=True)
                    embed.set_footer(text=f"Pronouns: {pronouns}")
                    if profile_pic:
                        embed.set_thumbnail(url=profile_pic)

                    await ctx.send(embed=embed)
                else:
                    await ctx.warn(
                        "Failed to find info about that user, or API is down."
                    )

    @command(
        name="commandcount",
        aliases=["cc"],
        description="Gets the command count of the bot.",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def commandcount(self, ctx: Context):
        non_jishaku_commands = [
            cmd for cmd in self.bot.walk_commands() if cmd.cog_name != "Jishaku"
        ]
        command_count = len(non_jishaku_commands)
        return await ctx.neutral(f"[+] I have **{command_count}** commands.")

    @command(name="support", description="Join our support server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def support(self, ctx: Context):
        return await ctx.neutral(
            "Join our [**support server**](https://discord.gg/jCPYXFQekB)"
        )

    @hybrid_command(name="avatar", aliases=["av"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def avatar(
        self, ctx: Context, user: Union[discord.Member, discord.User] = None
    ):
        if user is None:
            user = ctx.author

        APIKEY = api.heal
        api_url = "http://localhost:1999/dominantcolor"

        params = {"source": user.avatar.url}
        headers = {"api-key": APIKEY}

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    color = data.get("color")

        embed = discord.Embed(title=f"{user}'s avatar.", color=color)
        embed.set_image(url=user.avatar.url)
        view = View()
        view.add_item(Button(label="avatar", url=user.avatar.url))
        await ctx.send(embed=embed, view=view)

    @hybrid_command(
        name="banner", aliases=["bnr"], description="Get the banner of a user."
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def banner(
        self, ctx: Context, user: Union[discord.Member, discord.User] = None
    ):
        if user is None:
            user = ctx.author
        user = await self.bot.fetch_user(user.id)

        if user.banner:
            embed = discord.Embed(
                title=f"{user.name}'s banner", color=Colors.BASE_COLOR
            )
            embed.set_image(url=user.banner.url)
            view = View()
            view.add_item(Button(label="banner", url=user.banner.url))
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.warn(f"This user does not have a banner set.")

    @command(name="bans", aliases=["banlist"], usage="bans")
    @cooldown(1, 5, BucketType.user)
    async def bans(self, ctx: Context):
        banned = [m async for m in ctx.guild.bans()]
        count = 0
        embeds = []

        if len(banned) == 0:
            return await ctx.warn("there are no **bans** in this server.")

        entries = [
            f"` {i} `  **{m.user.name}**  ({m.user.id})  |  {m.reason if m.reason else 'no reason provided'}"
            for i, m in enumerate(banned, start=1)
        ]

        embed = discord.Embed(
            color=Colors.BASE_COLOR, title=f"ban list ({len(entries)})", description=""
        )

        for entry in entries:
            embed.description += f"{entry}\n"
            count += 1

            if count == 10:
                embeds.append(embed)
                embed = discord.Embed(
                    color=Colors.BASE_COLOR,
                    description="",
                    title=f"ban list ({len(entries)})",
                )
                count = 0

        if count > 0:
            embeds.append(embed)

        await ctx.paginate(embeds)

    @command(name="boosters", aliases=["blist", "boosterlist"], usage="boosters")
    @cooldown(1, 5, BucketType.user)
    async def boosters(self, ctx: Context):
        boosters = ctx.guild.premium_subscriber_role.members

        count = 0
        embeds = []

        if (
            not ctx.guild.premium_subscriber_role
            or len(ctx.guild.premium_subscriber_role.members) == 0
        ):
            return await ctx.warn("there are no **boosters** in this server.")

        entries = [
            f"` {i} `  **{b.name}**  ({b.id})" for i, b in enumerate(boosters, start=1)
        ]

        embed = discord.Embed(
            color=Colors.BASE_COLOR,
            title=f"booster list ({len(entries)})",
            description="",
        )

        for entry in entries:
            embed.description += f"{entry}\n"
            count += 1

            if count == 10:
                embeds.append(embed)
                embed = discord.Embed(
                    color=Colors.BASE_COLOR,
                    description="",
                    title=f"booster list ({len(entries)})",
                )
                count = 0

        if count > 0:
            embeds.append(embed)

        await ctx.paginate(embeds)

    @commands.group(
        name="server",
        aliases=["guild"],
        description="get information about the server.",
        invoke_without_command=True,
    )
    async def server(self, ctx: Context):
        return await ctx.send_help(ctx.command)

    @server.command(
        name="icon",
        aliases=["avatar", "pfp"],
        description="get the server's icon.",
    )
    @cooldown(1, 5, BucketType.user)
    async def server_icon(self, ctx: Context):
        embed = discord.Embed(
            title=f"{ctx.guild.name}'s icon",
            color=Colors.BASE_COLOR,
            url=ctx.guild.icon.url,
        )
        embed.set_image(url=ctx.guild.icon)
        await ctx.reply(embed=embed)

    @server.command(
        name="banner", aliases=["bnr"], description="Get the server's banner."
    )
    @cooldown(1, 5, BucketType.user)
    async def server_banner(self, ctx: Context):
        if not ctx.guild.banner:
            return await ctx.warn(f"this server doesn't have a **banner**.")
        embed = discord.Embed(
            title=f"{ctx.guild.name}'s banner", url=ctx.guild.banner.url
        )
        embed.set_image(url=ctx.guild.banner)
        await ctx.reply(embed=embed)

    @command(
        name="joinposition", aliases=["joinpos"], description="Get your joinposition."
    )
    @cooldown(1, 5, BucketType.user)
    async def joinposition(
        self, ctx: Context, *, user: discord.Member = commands.Author
    ):
        join_position = get_ordinal(
            sorted(ctx.guild.members, key=lambda m: m.joined_at).index(user) + 1
        )
        return await ctx.neutral(
            f"{user.name} was the **{join_position}** member to join"
        )

    @command(
        name="oldnames",
        aliases=["prevnames", "namehistory", "names"],
        description="Get your name history.",
    )
    @cooldown(1, 5, BucketType.user)
    async def oldnames(
        self, ctx: Context, *, user: Union[discord.Member, discord.User] = None
    ):
        if user is None:
            user = ctx.author

        data = await self.bot.pool.fetch(
            "SELECT oldnames, time FROM names WHERE user_id = $1 ORDER BY time DESC",
            user.id,
        )

        if not data:
            return await ctx.deny(f"{user} has no name history recorded.")

        embed = discord.Embed(title=f"{user}'s Name History", color=Colors.BASE_COLOR)

        for entry in data:
            name = entry["name"]
            timestamp = entry["time"]
            time_ago = discord.utils.format_dt(timestamp, style="R")

            embed.add_field(name=name, value=f"Changed: {time_ago}", inline=False)

        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="serverinfo", aliases=["si"])
    @cooldown(1, 5, BucketType.user)
    async def serverinfo(self, ctx: commands.Context):
        """
        Get info about the guild
        """
        guild = ctx.guild

        embed = discord.Embed(
            title=f"{guild.name}",
            description=f"{f'> {guild.description}' if guild.description is not None else ''}\n> Created on <t:{int(guild.created_at.timestamp())}:F> <t:{int(guild.created_at.timestamp())}:R> \n> **{guild.name} is on shard {ctx.guild.shard_id}/{self.bot.shard_count}**",
            color=Colors.BASE_COLOR,
        )
        users = [m for m in guild.members if not m.bot]
        bots = [b for b in guild.members if b.bot]

        embed.add_field(
            name="counts",
            value=f"> stickers: {len(guild.stickers)}/{guild.sticker_limit}\n> emojis: {len(guild.roles)}/{guild.emoji_limit}\n> roles: {len(guild.roles)}/250",
        )
        embed.add_field(
            name=f"channels ({len(guild.channels)})",
            value=f"> text: {len(guild.text_channels)}\n> voice: {len(guild.voice_channels)}\n> categories: {len(guild.categories)}",
        )
        embed.add_field(
            name="information",
            value=f"> vanity: {guild.vanity_url_code}\n> boosts: {guild.premium_subscription_count}\n> verification level: {guild.verification_level}",
        )
        embed.add_field(
            name="members",
            value=f"> users: {len(users)}\n> bots: {len(bots)}\n> total: {len(guild.members)}",
        )
        embed.add_field(
            name="design",
            value=f"> icon: {f'[here]({guild.icon.url})' if guild.icon else 'N/A'}\n> banner: {f'[here]({guild.banner.url})' if guild.banner else 'N/A'}\n> splash: {f'[here]({guild.splash.url})' if guild.splash else 'N/A'}",
        )
        embed.add_field(name="owner", value=f"{guild.owner.name} ({guild.owner.id})")
        features = ", ".join(guild.features)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else "https://none.none")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text=f"ID: {guild.id}")

        return await ctx.send(embed=embed)

    @command(
        name="membercount", aliases=["mc"], description="Get the server's membercount."
    )
    @cooldown(1, 5, BucketType.user)
    async def membercount(self, ctx: Context):
        embed = discord.Embed(
            title=f"{ctx.guild.name}'s member count", color=Colors.BASE_COLOR
        )
        embed.add_field(name="Total:", value=f"{ctx.guild.member_count}", inline=True)
        embed.add_field(
            name="Humans:",
            value=f"{sum(1 for member in ctx.guild.members if not member.bot)}",
            inline=True,
        )
        embed.add_field(
            name="Bots:",
            value=f"{ctx.guild.member_count - sum(1 for member in ctx.guild.members if not member.bot)}",
        )
        return await ctx.reply(embed=embed)

    @hybrid_command(
        name="roblox",
        description="Get information about a roblox user.",
        aliases=["rblx"],
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @cooldown(1, 5, BucketType.user)
    async def roblox(self, ctx: Context, *, username: str):
        url = "https://api.fulcrum.lol/roblox"
        params = {"username": username}
        headers = {"Authorization": api.luma}

        def humanize_number(value: int) -> str:
            if value >= 1_000_000:
                return f"{value / 1_000_000:.1f}M"
            elif value >= 1_000:
                return f"{value / 1_000:.1f}K"
            return str(value)

        await ctx.typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    username = data.get("username")
                    display_name = data.get("display_name", "N/A")
                    bio = data.get("bio", "N/A")
                    avatar = data.get("avatar")
                    friends = data.get("friends", "0")
                    followers = data.get("followers", "0")
                    followings = data.get("followings", "0")
                    url = data.get("url")
                    id = data.get("id")
                    banned = data.get("banned")

                    if isinstance(followers, int):
                        followers = humanize_number(followers)
                    if isinstance(followings, int):
                        followings = humanize_number(followings)
                    if isinstance(friends, int):
                        friends = humanize_number(friends)

                    title = f"{username}"

                    embed = discord.Embed(
                        title=f"{title}",
                        url=url,
                        color=Colors.BASE_COLOR,
                        description=bio,
                    )
                    embed.set_thumbnail(url=avatar)
                    embed.add_field(name="Following:", value=followings, inline=True)
                    embed.add_field(name="Followers:", value=followers)
                    embed.add_field(name="Friends:", value=friends)
                    embed.set_footer(text=f"id: {id}")
                    return await ctx.reply(embed=embed)

                else:
                    await ctx.warn(
                        f"API request failed with status code: {response.status}"
                    )

    @hybrid_command(name="twitter", description="Get info about a user on twitter.")
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @cooldown(1, 5, BucketType.user)
    async def twitter(self, ctx: Context, *, username: str):
        url = "https://api.fulcrum.lol/twitter"
        params = {"username": username}
        headers = {"Authorization": api.luma}

        def humanize_number(value: int) -> str:
            if value >= 1_000_000:
                return f"{value / 1_000_000:.1f}M"
            elif value >= 1_000:
                return f"{value / 1_000:.1f}K"
            return str(value)

        await ctx.typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    username = data.get("username")
                    avatar = data.get("avatar")
                    bio = data.get("bio", "N/A")
                    createat = data.get("created_at")
                    followers = data.get("followers", "0")
                    following = data.get("following", "0")
                    posts = data.get("posts", "0")
                    tweets = data.get("tweets", "0")
                    url = data.get("url")
                    verified = data.get("verified", False)

                    if isinstance(followers, int):
                        followers = humanize_number(followers)
                    if isinstance(following, int):
                        following = humanize_number(following)
                    if isinstance(tweets, int):
                        tweets = humanize_number(tweets)
                    if isinstance(posts, int):
                        posts = humanize_number(posts)

                    created_at_datetime = datetime.datetime.strptime(
                        createat, "%a %b %d %H:%M:%S %z %Y"
                    )
                    created_at_timestamp = int(created_at_datetime.timestamp())
                    created_at_formatted = f"<t:{created_at_timestamp}:R>"
                    footer = ""
                    if verified == True:
                        footer += "Verified account."

                    embed = discord.Embed(
                        title=f"{username}",
                        url=url,
                        color=Colors.BASE_COLOR,
                        description=bio,
                    )
                    embed.add_field(name="Followers:", value=followers, inline=True)
                    embed.add_field(name="Following:", value=following, inline=True)
                    embed.add_field(name="Tweets:", value=tweets, inline=True)
                    embed.add_field(name="Posts:", value=posts, inline=True)
                    embed.add_field(
                        name="Created at:", value=created_at_formatted, inline=True
                    )
                    embed.set_footer(text=footer)
                    embed.set_thumbnail(url=avatar)
                    return await ctx.reply(embed=embed)

                else:
                    await ctx.warn(
                        f"API request failed with status code: {response.status}"
                    )

    @hybrid_command(
        name="dominant", description="Get the dominant color from an image."
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dominant(self, ctx: Context, *, image: str = None):
        if ctx.message.attachments:
            image_url = ctx.message.attachments[0].url
        elif image:
            image_url = image
        else:
            return await ctx.warn("Please provide an image URL or upload an image.")

        await ctx.typing()

        APIKEY = api.heal
        api_url = "http://localhost:1999/dominantcolor"

        params = {"source": image_url}
        headers = {"api-key": APIKEY}

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    color = data.get("color")
                    embed = discord.Embed(
                        description=f"Dominant color - {hex(color)}", color=color
                    )
                    return await ctx.reply(embed=embed)

                if response.status == 422:
                    return await ctx.warn(f"{data.get('detail')}")

    @hybrid_command(name="weather", description="Get weather from a certain location.")
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def weather(self, ctx: Context, *, location: str):
        APIKEY = api.luma
        apiurl = "https://api.fulcrum.lol/weather"

        params = {"location": location}
        headers = {"Authorization": APIKEY}

        async with aiohttp.ClientSession() as session:
            async with session.get(apiurl, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    city = data.get("city")
                    country = data.get("country")
                    time = data.get("time")
                    celsius = data.get("celsius")
                    fahrenheit = data.get("fahrenheit")
                    conditiontxt = data.get("condition_text")
                    conditionicon = data.get("condition_icon")
                    humid = data.get("humidity")
                    windmph = data.get("wind_mph")
                    windkph = data.get("wind_kph")
                    feelslikecels = data.get("feelslike_c")
                    feelslikefahren = data.get("feelslike_f")

                    time_obj = datetime.datetime.fromisoformat(time)

                    humanizedTime = time_obj.strftime("%I:%M %p")

                    embed = discord.Embed(
                        title=f"{country}, {city}",
                        description=f"Right now, it's **{conditiontxt}** in **{city}**, at **{humanizedTime}**. **Humidity is {humid}%**",
                    )
                    embed.add_field(
                        name="Tempurature:",
                        value=f"{celsius}°c / {fahrenheit}°f \n Feels like: {feelslikecels}°c / {feelslikefahren}°f",
                    )
                    embed.add_field(name="Wind:", value=f"{windmph}mph / {windkph}kph")
                    embed.set_thumbnail(url=conditionicon)
                    return await ctx.reply(embed=embed)

    @command(aliases=["trans"], description="Translate a message from any language.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def translate(self, ctx, *, message):
        translator = Translator()
        trans_message = translator.translate(message, dest="en")

        embed = discord.Embed(
            description=f"**Translation from {trans_message.src}:** {trans_message.text}",
            color=Colors.BASE_COLOR,
        )
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def topcmds(self, ctx: Context):
        rows = await self.bot.pool.fetch(
            """
            SELECT command_name, usage_count
            FROM topcmds
            ORDER BY usage_count DESC
            LIMIT 10
        """
        )

        embed = discord.Embed(title="Top 10 Commands", color=Colors.BASE_COLOR)
        for row in rows:
            command_name = row["command_name"]
            usage_count = row["usage_count"]
            embed.add_field(
                name=f"{command_name} - {usage_count}", value=f"", inline=False
            )

        await ctx.send(embed=embed)

    @command(name="bots", description="Get a list of bots.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bots(self, ctx: Context):
        bots = [b for b in ctx.guild.members if b.bot]
        count = 0
        embeds = []

        entries = [
            f"` {i} `  **{m.name}**  ({m.id})" for i, m in enumerate(bots, start=1)
        ]
        embed = discord.Embed(
            color=Colors.BASE_COLOR, title=f"bot list ({len(entries)})", description=""
        )

        for entry in entries:
            embed.description += f"{entry}\n"
            count += 1

            if count == 10:
                embeds.append(embed)
                embed = discord.Embed(
                    color=Colors.BASE_COLOR,
                    description="",
                    title=f"bot list ({len(entries)})",
                )
                count = 0

        if count > 0:
            embeds.append(embed)

        await ctx.paginate(embeds)

    @command(name="inrole", description="Check users in a certain role.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def inrole(self, ctx: Context, *, role: discord.Role = None):
        if role is None:
            return await ctx.send_help(ctx.command)
        inrole = [m for m in ctx.guild.members if role in m.roles]
        embeds = []
        count = 0

        if not inrole:
            return await ctx.warn(f"There is **no one** in the role {role.mention}.")

        entries = [
            f"` {i} `  **{m.name}**  ({m.id})" for i, m in enumerate(inrole, start=1)
        ]

        embed = discord.Embed(
            color=Colors.BASE_COLOR,
            title=f"Members in {role.name} ({len(entries)})",
            description="",
        )
        for entry in entries:
            embed.description += f"{entry}\n"
            count += 1

            if count == 10:
                embeds.append(embed)
                embed = discord.Embed(
                    color=Colors.BASE_COLOR,
                    description="",
                    title=f"Members in {role.name} ({len(entries)})",
                )
                count = 0

        if count > 0:
            embeds.append(embed)

        await ctx.paginate(embeds)

    @command(name="boosters", description="Check the guild's boosters.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boosters(self, ctx: Context):
        boosters = ctx.guild.premium_subscribers
        embeds = []
        count = 0

        if not boosters:
            return await ctx.warn(f"There are no **boosters** in this guild..")

        entries = [
            f"` {i} `  **{m.name}**  ({m.id})" for i, m in enumerate(boosters, start=1)
        ]

        embed = discord.Embed(
            color=Colors.BASE_COLOR, title=f"Boosters ({len(entries)})", description=""
        )
        for entry in entries:
            embed.description += f"{entry}\n"
            count += 1

            if count == 10:
                embeds.append(embed)
                embed = discord.Embed(
                    color=Colors.BASE_COLOR,
                    description="",
                    title=f"Boosters ({len(entries)})",
                )
                count = 0

        if count > 0:
            embeds.append(embed)

        await ctx.paginate(embeds)

    @hybrid_command(
        name="inviteinfo",
        aliases=["ii"],
        description="View information about a server.",
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def inviteinfo(self, ctx: Context, *, invite: discord.Invite = None):
        if invite is None:
            return await ctx.send_help(ctx.command)

        embed = discord.Embed(
            title=f"Invite code: {invite.code}",
            description=f"{invite.guild.description}",
        )
        embed.add_field(
            name=f"Invite:",
            value=f"> **Channel:** {invite.channel.name} \n> **ID:** {invite.channel.id} \n> **Expires:** {f'yes ({(invite.expires_at.replace(tzinfo=None))})' if invite.expires_at else 'no'} \n> **Uses:** {invite.uses or 'None'}",
        )
        embed.add_field(
            name="Server:",
            value=f"> **Name:** {invite.guild.name} \n> **Members:** {invite.approximate_member_count: ,} \n> **Created:** {discord.utils.format_dt(invite.created_at, style='R') if invite.created_at else 'N/A'} \n> **Boosts:** {invite.guild.premium_subscription_count:,}",
        )
        embed.set_thumbnail(url=invite.guild.icon.url)
        return await ctx.send(embed=embed)


async def setup(bot: Heal):
    await bot.add_cog(Information(bot))
