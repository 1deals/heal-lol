import importlib
import jishaku
import logging
import asyncpg
import asyncio
import aiohttp
import discord
import secrets
import string
import glob
import json
import sys
import os
import re
import datetime
import time
import discord_ios
import socket
import pathlib

from asyncpg import Pool
from typing import Dict, Set
from collections import defaultdict
from loguru import logger
from discord.ext.commands import BadArgument

from tools.managers.help import HealHelp
from tools.managers.cache import Cache
from tools.managers.context import Context
from tools.managers.lastfm import FMHandler
from tools.configuration import Colors, Emojis
from discord.ext import commands
from discord import Message, Embed, File
from pyppeteer import launch
from nudenet import NudeDetector

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()


class Heal(commands.AutoShardedBot):
    def __init__(self):
        self.cache = Cache()
        self.errors = Dict[str, commands.CommandError]
        self._uptime = time.time()
        self.proxy_password = "7sqgncj8hiz3"
        self.proxy_username = "oxwlfyfl"

        super().__init__(
            command_prefix=";",
            help_command=HealHelp(),
            intents=intents,
            shard_count=2,
            activity=discord.CustomActivity(name=f"🔗discord.gg/healbot"),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=False, replied_user=False
            ),
            case_insensitive=True,
            owner_ids=[187747524646404105, 1208472692337020999, 1272545050102071460],
        )

        self.uptime2 = time.time()
        self.message_cache = defaultdict(list)
        self.cache_expiry_seconds = 30
        self.add_check(self.disabled_command)
        self.browser = None

    async def load_modules(self, directory: str) -> None:
        for module in glob.glob(f"{directory}/**/*.py", recursive=True):
            if module.endswith("__init__.py"):
                continue
            try:
                await self.load_extension(module.replace("/", ".").replace(".py", ""))
                logger.info(f"Loaded module: {module}")
            except commands.ExtensionFailed:
                logger.warning(f"Extension failed to load: {module}")
            except Exception as e:
                logger.error(f"Error loading module {module}: {e}")

    async def load_patches(self) -> None:
        for module in glob.glob("tools/patches/**/*.py", recursive=True):
            if module.endswith("__init__.py"):
                continue

            module_name = (
                module.replace(os.path.sep, ".").replace("/", ".").replace(".py", "")
            )

            try:
                importlib.import_module(module_name)
                print(f"Patched: {module}")
            except ModuleNotFoundError as e:
                print(f"Error importing {module_name}: {e}")

    async def _load_database(self) -> Pool:
        try:
            pool = await asyncpg.create_pool(
                **{
                    var: os.environ[
                        f"DATABASE_{var.upper()}" if var != "database" else "DATABASE"
                    ]
                    for var in ["database", "user", "password", "host"]
                },
                max_size=30,
                min_size=10,
            )
            logger.info("Database connection established")

            with open("tools/schema/schema.sql", "r") as file:
                schema = file.read()
                if schema.strip():  # Check if schema is not empty
                    await pool.execute(schema)
                    logger.info("Database schema loaded")
                else:
                    log.warning("Database schema file is empty")
                file.close()

            return pool
        except Exception as e:
            logger.error(f"Error loading database: {e}")
            raise e

    async def get_prefix(self, message: Message) -> tuple:
        """
        Get the command prefixes for a message, considering both self-prefix and guild prefix.
        """
        if message.guild is None:
            return

        guild_prefix = await self.cache.get(f"prefix-{message.guild.id}")
        if guild_prefix is None:
            guild_prefix = (
                await self.pool.fetchval(
                    "SELECT prefix FROM guilds WHERE guild_id = $1", message.guild.id
                )
                or ";"
            )
            await self.cache.set(f"prefix-{message.guild.id}", guild_prefix)

        self_prefix = await self.cache.get(f"selfprefix-{message.author.id}")
        if self_prefix is None:
            self_prefix = await self.pool.fetchval(
                "SELECT prefix FROM selfprefix WHERE user_id = $1", message.author.id
            )
            if self_prefix:
                await self.cache.set(f"selfprefix-{message.author.id}", self_prefix)

        return (self_prefix or guild_prefix, guild_prefix)

    async def on_ready(self) -> None:
        logger.info(
            f"Logged in as {self.user.name}#{self.user.discriminator} ({self.user.id})"
        )
        logger.info(f"Connected to {len(self.guilds)} guilds")
        logger.info(f"Connected to {len(self.users)} users")

        await self.cogs["Music"].start_nodes()
        logger.info("Lavalink Nodes Loaded.")

    async def setup_hook(self) -> None:
        self.pool = await self._load_database()
        self.session = aiohttp.ClientSession()
        await self.load_modules("cogs")
        await self.load_modules("events")
        await self.load_extension("jishaku")

        from tools.ui import Interface

        self.add_view(Interface(self))

        return await super().setup_hook()

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        self._connection.http.connector = aiohttp.TCPConnector(
            limit=0, family=socket.AF_INET, local_addr=("216.105.170.101", 0)
        )
        return await super().start(token, reconnect=reconnect)

    async def get_context(self, message: Message, *, cls=Context):
        return await super().get_context(message, cls=cls)

    def humanize_number(self, number: int) -> str:
        suffixes = ["", "k", "m", "b", "t"]
        magnitude = min(len(suffixes) - 1, (len(str(abs(number))) - 1) // 3)
        formatted_number = (
            "{:.1f}".format(number / 10 ** (3 * magnitude)).rstrip("0").rstrip(".")
        )
        return "{}{}".format(formatted_number, suffixes[magnitude])

    def humanize_time(self, start_time: float) -> str:
        uptime_seconds = abs(time.time() - start_time)
        intervals = (
            ("year", 31556952),
            ("month", 2629746),
            ("day", 86400),
            ("hour", 3600),
            ("minute", 60),
            ("second", 1),
        )

        result = []
        for name, count in intervals:
            value = uptime_seconds // count
            if value:
                uptime_seconds -= value * count
                result.append(f"{int(value)} {name}{'s' if value > 1 else ''}")

        return ", ".join(result)

    @property
    def uptime(self) -> str:
        return self.humanize_time(self._uptime)

    @property
    def linecount(self) -> int:
        return sum(
            [
                len(f.open("r").readlines())
                for f in [
                    f
                    for f in pathlib.Path("/root/heal-lol/").glob("**/*.py")
                    if f.is_file()
                ]
            ]
        )

    async def on_command_error(
        self, ctx: Context, exception: commands.CommandError
    ) -> None:
        if type(exception) in [
            commands.CommandNotFound,
            commands.NotOwner,
            commands.CheckFailure,
        ]:
            return
        elif isinstance(exception, commands.BadColourArgument):
            return await ctx.warn(f"I was **unable** to find that **color**.")
        elif isinstance(exception, commands.RoleNotFound):
            return await ctx.warn(
                f"I was unable to find the role **{exception.argument}**."
            )
        elif isinstance(exception, commands.ChannelNotFound):
            return await ctx.warn(
                f"I was unable to find the channel **{exception.argument}**"
            )
        elif isinstance(exception, commands.ThreadNotFound):
            return await ctx.warn(
                f"I was unable to find the thread **{exception.argument}**"
            )
        elif isinstance(exception, commands.BadUnionArgument):
            if (
                discord.Emoji in exception.converters
                or discord.PartialEmoji in exception.converters
            ):
                return await ctx.warn(f"Invalid **emoji** provided.")
            elif (
                discord.User in exception.converters
                or discord.Member in exception.converters
            ):
                return await ctx.warn(
                    f"I was unable to find that **member** or the provided **ID** is invalid."
                )
            return await ctx.warn(
                f"Could not convert **{exception.param.name}** to **{exception.converters}**"
            )
        elif isinstance(exception, commands.CommandInvokeError):
            if isinstance(exception.original, ValueError):
                return await ctx.warn(exception.original)
            elif isinstance(exception.original, discord.HTTPException):
                return await ctx.warn(f"**Invalid code**\n```{exception.original}```")
            elif isinstance(exception.original, aiohttp.ClientConnectorError):
                return await ctx.warn(
                    f"**Failed** to connect to the **URL** - Possibly invalid."
                )
            elif isinstance(exception.original, aiohttp.ClientResponseError):
                if exception.original.status == 522:
                    return await ctx.warn(
                        f"**Timed out** while requesting data - probably the API's fault"
                    )
                return await ctx.warn(
                    f"**API** returned a **{exception.original.status}** status - try again later."
                )
            elif isinstance(exception.original, discord.Forbidden):
                return await ctx.warn(
                    f"I'm **missing** permission: `{exception.original.missing_perms[0]}`"
                )
            elif isinstance(exception.original, discord.NotFound):
                return await ctx.warn(f"**Not found** - the **ID** is invalid")
            elif isinstance(exception.original, aiohttp.ContentTypeError):
                return await ctx.warn(
                    f"**Invalid content** - the **API** returned an unexpected response"
                )
            elif isinstance(exception.original, aiohttp.InvalidURL):
                return await ctx.warn(f"The provided **url** is invalid")
            elif isinstance(exception.original, asyncpg.StringDataRightTruncationError):
                return await ctx.warn(
                    f"**Data** is too **long** - try again with a shorter message"
                )
            return await ctx.warn(exception.original)
        elif isinstance(exception, commands.UserNotFound):
            return await ctx.warn(
                "I was unable to find that **member** or the **ID** is invalid"
            )
        elif isinstance(exception, commands.MemberNotFound):
            return await ctx.warn(
                f"I was unable to find a member with the name: **{exception.argument}**"
            )
        elif isinstance(exception, commands.MissingPermissions):
            return await ctx.warn(
                f"You're **missing** permission: `{exception.missing_permissions[0]}`"
            )
        elif isinstance(exception, commands.BotMissingPermissions):
            return await ctx.warn(
                f"I'm **missing** permission: `{exception.missing_permissions[0]}`"
            )
        elif isinstance(exception, commands.GuildNotFound):
            return await ctx.warn(
                f"I was unable to find that **server** or the **ID** is invalid"
            )
        elif isinstance(exception, commands.BadInviteArgument):
            return await ctx.warn(f"Invalid **invite code** given")
        elif isinstance(exception, commands.UserInputError):
            return await ctx.warn(f"**Invalid Input Given**: \n`{exception}`")
        elif isinstance(exception, commands.CommandOnCooldown):
            return await ctx.neutral(
                f"<:cooldown:1293327736219111508> Please wait **{exception.retry_after:.2f} seconds** before using this command again."
            )
        if isinstance(exception, commands.errors.NotOwner):
            return await ctx.deny(f"You are not an owner of {self.user.mention}.")

        code = "".join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(13)
        )
        self.errors[code] = exception
        return await ctx.warn(
            message=f"Error occurred whilst performing command **{ctx.command.qualified_name}**. Use the given error code to report it to the developers in the [support server](https://discord.gg/tCZDT7YdUF)",
            content=f"`{code}`",
        )

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        check = await self.pool.fetchrow(
            "SELECT * FROM blacklist WHERE user_id = $1", message.author.id
        )
        if check:
            return

        prefix = await self.get_prefix(message)
        if not message.content.startswith(tuple(prefix)):
            return

        now = time.time()
        author_id = message.author.id

        self.message_cache[author_id] = [
            timestamp
            for timestamp in self.message_cache[author_id]
            if now - timestamp < self.cache_expiry_seconds
        ]

        if len(self.message_cache[author_id]) >= 10:
            await self.pool.execute("INSERT INTO blacklist VALUES ($1)", author_id)
            await message.channel.send(
                embed=discord.Embed(
                    color=Colors.BASE_COLOR,
                    description=f"> {message.author.mention}: You are now **blacklisted**, join the support [server](https://discord.gg/healbot) for support.",
                )
            )
        else:
            self.message_cache[author_id].append(now)
            await self.process_commands(message)

    async def disabled_command(self, ctx: Context) -> bool:
        if ctx.guild is None:
            return True
        cmd = self.get_command(ctx.invoked_with)
        if not cmd:
            return True

        check = await self.pool.fetchrow(
            "SELECT * FROM disablecommand WHERE command = $1 AND guild_id = $2",
            cmd.name,
            ctx.guild.id,
        )

        if check:
            await ctx.warn(f"The command **{cmd.name}** is **disabled** in this guild")

        return check is None

    async def screenshot(self, url: str):
        filename = f"{url.replace('https://', '').replace('/', '')}.png"
        directory = "./screenshots/"
        path = os.path.join(directory, filename)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if os.path.exists(path):
            return File(path)

        if not self.browser:
            self.browser = await launch(
                headless=True,
                args=["--no-sandbox", "--force-dark-mode"],
                defaultViewport={"width": 1980, "height": 1080},
            )

        page = await self.browser.newPage()
        await page.authenticate(
            credentials=[
                {"username": self.proxy_username, "password": self.proxy_password}
            ]
        )
        keywords = ["pussy", "tits", "porn", "cock", "dick"]
        try:
            p = await page.goto(url, load=True, timeout=5000)
        except:
            await page.close()
            raise BadArgument("I'm unable to screenshot this page.")

        if not p:
            await page.close()
            raise BadArgument("This page didn't send a response.")

        if content_type := p.headers.get("content-type"):
            if not any((i in content_type for i in ("text/html", "application/json"))):
                await page.close()
                raise BadArgument("This page contains content I cannot screenshot.")
        content = await page.content()

        if any(
            re.search(r"\b{}\b".format(keyword), content, re.IGNORECASE)
            for keyword in keywords
        ):
            await page.close()
            raise BadArgument("This website contains explicit content.")

        await page.screenshot(path=path)

        filters = [
            "BUTTOCKS_EXPOSED",
            "FEMALE_BREAST_EXPOSED",
            "ANUS_EXPOSED",
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
        ]
        detections = NudeDetector().detect(path)
        if any([prediction["class"] in filters for prediction in detections]):
            raise BadArgument("This website contains explicit content.")

        await page.close()
        return File(path)

    async def on_command(self: "Heal", ctx) -> None:
        logger.info(
            f"{ctx.author} ({ctx.author.id}) executed {ctx.command} in {ctx.guild} ({ctx.guild.id})."
        )

    async def on_shard_resumed(self, shard_id: int) -> None:
        channelid = 1275776609944862850
        channel = self.get_channel(channelid)

        shard_guild_count = len([guild for guild in self.guilds if guild.shard_id == shard_id])
        shard_user_count = len([user for guild in self.guilds for user in guild.members if guild.shard_id == shard_id])

        embed = Embed(
            description= f"Shard {shard_id} has resumed, serving **{shard_guild_count}** guilds and **{shard_user_count}** users.",
        )
        logger.info(
            f"Shard {shard_id} has resumed."
        )
        try:
            await channel.send(embed=embed)
        except:
            return
