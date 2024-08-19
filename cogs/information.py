import discord
import psutil
import sys
import time
import random
from random import choice

from tools.managers.context     import Context
from discord.ext.commands       import command, group, BucketType, cooldown, has_permissions, hybrid_command, hybrid_group
from tools.configuration        import Emojis, Colors
from tools.paginator            import Paginator
from discord.utils              import format_dt
from discord.ext                import commands
from tools.heal                 import Heal
from typing import Union
import datetime
import aiohttp
from tools.managers.embedBuilder import EmbedBuilder, EmbedScript
from tools.configuration import api
from tools.models.statistics import BotStatistics
import os
from discord.ui import View, Button

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

    @hybrid_command(
        name = "botinfo",
        aliases = ["bi", "bot"],
        description = "Get information about the bot."
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @cooldown(1, 5, commands.BucketType.user)
    async def botinfo(self, ctx: Context):
        total_channels = 0
        for guild in self.bot.guilds:
                    
            total_channels += len(guild.channels)
        availableMem = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
        embed = discord.Embed(description =f"An all-in-one, aesthetically pleasing multipurpose bot, aimed to keep communities safe and thriving. Created by the [**Heal Team**](https://discord.gg/jCPYXFQekB)", color= Colors.BASE_COLOR)
        embed.add_field(name= "__Statistics:__", value = f"**Guilds:** {len(self.bot.guilds)} \n**Users:** {len(self.bot.users): ,} \n**Channels:** {total_channels}", inline = True)
        embed.add_field(name = "__Bot:__", value= f"**Uptime:** {self.bot.uptime} \n**Latency:** {round(self.bot.latency * 1000)}ms \n**Commands:** {len([cmd for cmd in self.bot.walk_commands() if cmd.cog_name != 'Jishaku'])}", inline = True)
        embed.add_field(name = "__Usage:__", value = f"**Memory:** {psutil.virtual_memory().percent}% \n**Available:** {availableMem}% \n**CPU:** {psutil.cpu_percent()}%", inline = True)
        embed.set_thumbnail(url= self.bot.user.avatar.url)
        return await ctx.send(embed=embed)

    @hybrid_command(
    name="ping",
    aliases=["heartbeat", "latency", "websocket"],
    usage="ping"

    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @cooldown(1, 5, BucketType.user)
    async def ping(self, ctx: Context):
            return await ctx.neutral(f"> :satellite: **Ping:** `{int(self.bot.latency * 1000)}ms`")
            

    @hybrid_command(
        name = "invite",
        aliases = ["inv"],
        usage = "invite"
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx: Context):
        await ctx.send(f"{discord.utils.oauth_url(client_id=self.bot.user.id, permissions=discord.Permissions(8))}")

    @hybrid_command(
        name = "uptime",
        aliases = ["up"],
        usage = "uptime"
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @cooldown(1, 5, commands.BucketType.user)
    async def uptime(self, ctx: Context):
        await ctx.neutral(f":alarm_clock: I have been **up** for `{self.bot.uptime}`")


    @hybrid_command(
    name="userinfo",
    aliases=["ui", "whois"],
    description="Get info about a user."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx: Context, *, user: Union[discord.Member, discord.User] = None):

        if isinstance(user, int):
            try:
                user = await self.bot.fetch_user(user)
            except discord.NotFound:
                return await ctx.warn("User not found.")
        else:
            user = user or ctx.author


        data = await self.bot.pool.fetchrow("SELECT * FROM lastfm WHERE user_id = $1", user.id)
        
        title = f"{user.name}"
        description = ""


        if user.id == 187747524646404105:  # me
            title += " <:owner:1270728554388394086> <:staff:1270729949686534206> <:dev:1270730817458405468> "
        if user.id == 392300135323009024:  # xur
            title += " <:staff:1270729949686534206> <:dev:1270730817458405468>"
        if user.id == 461914901624127489:  # logan
            title += " <:zzmilklove2:1270873236841693267> <:staff:1270729949686534206> <:dev:1270730817458405468>"
        if user.id == 1261756025275547719:  # neca
            title += " <:staff:1270729949686534206>"

        embed = discord.Embed(
            title=title,
            color=Colors.BASE_COLOR
        )
        embed.add_field(name="Created", value=format_dt(user.created_at, style='f'), inline=True)

        if isinstance(user, discord.Member) and user.joined_at:
            all_members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            position = all_members.index(user) + 1

            roles = [role.mention for role in user.roles if role.id != ctx.guild.id]
            roles_list = ", ".join(roles) if roles else "None"

            join_position_ordinal = get_ordinal(position)
            embed.add_field(name=f"Joined {join_position_ordinal}", value=f"{format_dt(user.joined_at, style='f')}", inline=True)
            embed.add_field(name="Roles", value=roles_list, inline=False)

        embed.set_thumbnail(url=user.avatar.url)

        if data:
            lastfm_username = data["lfuser"]
            async with aiohttp.ClientSession() as session:
                params = {
                    'method': 'user.getRecentTracks',
                    'user': lastfm_username,
                    'api_key': "bc8082588489f949216859abba6e52be",
                    'format': 'json',
                    'limit': 1
                }
                async with session.get('http://ws.audioscrobbler.com/2.0/', params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'recenttracks' in data and 'track' in data['recenttracks']:
                            track_info = data['recenttracks']['track'][0]
                            now_playing = track_info.get('@attr', {}).get('nowplaying') == 'true'
                            if now_playing:
                                track_name = track_info['name']
                                artist_name = track_info['artist']['#text']
                                track_url = track_info['url']
                                description += f"> {Emojis.LASTFM} **Listening to [{track_name}]({track_url}) by {artist_name}**"
                                embed.description = description
                                album_art = track_info['image'][-1]['#text']
                                if album_art:
                                    embed.set_thumbnail(url=album_art)

        await ctx.send(embed=embed)

    @hybrid_command(
        name = "instagram",
        aliases = ["insta", "ig"],
        description = "Get information about an instagram user."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def instagram(self, ctx:Context, username: str):
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
                        title=title,
                        description=bio,
                        color=Colors.BASE_COLOR
                    )
                    embed.add_field(name="Followers", value=followers, inline=True)
                    embed.add_field(name="Following", value=following, inline=True)
                    embed.add_field(name="Posts", value= posts, inline = True)
                    embed.set_footer(text=f"Pronouns: {pronouns}")
                    if profile_pic:
                        embed.set_thumbnail(url=profile_pic)

                    await ctx.send(embed=embed)
                else:
                    await ctx.warn("Failed to find info about that user, or API is down.")

    @command(
        name = "commandcount",
        aliases = ["cc"],
        description = "Gets the command count of the bot."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def commandcount(self, ctx: Context):
        non_jishaku_commands = [cmd for cmd in self.bot.walk_commands() if cmd.cog_name != "Jishaku"]
        command_count = len(non_jishaku_commands)
        return await ctx.neutral(f"[+] I have **{command_count}** commands.")

    @command(
        name = "support",
        description = "Join our support server."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def support(self, ctx: Context):
        return await ctx.neutral("Join our [**support server**](https://discord.gg/jCPYXFQekB)")

    @commands.command(name = "avatar", aliases = ["av"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx: Context, user: Union[discord.Member, discord.User] = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(title = f"{user}'s avatar.", color = Colors.BASE_COLOR)
        embed.set_image(url = user.avatar.url)
        view = View()
        view.add_item(Button(label="avatar", url=user.avatar.url))
        await ctx.send(embed=embed, view=view)
    
    @command(
        name = "banner",
        aliases = ["bnr"],
        description = "Get the banner of a user."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def banner(self, ctx: Context, user: Union[discord.Member, discord.User] = None):
        if user is None:
            user = ctx.author
        user = await self.bot.fetch_user(user.id)

        if user.banner:
            embed = discord.Embed(title=f"{user.name}'s banner", color=Colors.BASE_COLOR)
            embed.set_image(url=user.banner.url)
            view = View()
            view.add_item(Button(label="banner", url=user.banner.url))
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.warn(f"This user does not have a banner set.")

    @command(
        name="bans",
        aliases=["banlist"],
        usage="bans"
    )
    @cooldown(1, 5, BucketType.user)
    async def bans(self, ctx: Context):
        banned = [m async for m in ctx.guild.bans()]
        count = 0
        embeds = []

        if len(banned) == 0:
            return await ctx.warn('there are no **bans** in this server.')

        entries = [
            f"` {i} `  **{m.user.name}**  ({m.user.id})  |  {m.reason if m.reason else 'no reason provided'}"
            for i, m in enumerate(banned, start=1)
        ]

        embed = discord.Embed(color=Colors.BASE_COLOR, title=f"ban list ({len(entries)})", description="")

        for entry in entries:
            embed.description += f'{entry}\n'
            count += 1

            if count == 10:
                embeds.append(embed)
                embed = discord.Embed(color=Colors.BASE_COLOR, description="", title=f"ban list ({len(entries)})")
                count = 0

        if count > 0:
            embeds.append(embed)

        await ctx.paginate(embeds)

    @command(
        name = "boosters",
        aliases = ["blist", "boosterlist"],
        usage = "boosters"
    )
    @cooldown(1, 5, BucketType.user)
    async def boosters(self, ctx: Context):
        boosters = ctx.guild.premium_subscriber_role.members

        count    = 0
        embeds   = []

        if not ctx.guild.premium_subscriber_role or len(ctx.guild.premium_subscriber_role.members) == 0:
            return await ctx.warn('there are no **boosters** in this server.')
        
        entries = [
            f"` {i} `  **{b.name}**  ({b.id})"
            for i, b in enumerate(boosters, start=1)
        ]

        embed = discord.Embed(color=Colors.BASE_COLOR, title=f"booster list ({len(entries)})", description="")

        for entry in entries:
            embed.description += f'{entry}\n'
            count += 1

            if count == 10:
                embeds.append(embed)
                embed = discord.Embed(color=Colors.BASE_COLOR, description="", title=f"booster list ({len(entries)})")
                count = 0

        if count > 0:
            embeds.append(embed)

        await ctx.paginate(embeds)

    @command(
        name = "roles",
        aliases = ["rlist", "rolelist"],
        usage = "roles"
    )
    @cooldown(1, 5, BucketType.user)
    async def roles(self, ctx: Context):
        roles    = ctx.guild.roles
        count    = 0
        embeds   = []

        if len(ctx.guild.roles) == 0:
            return await ctx.warn('there are no **roles** in this server.')
        
        entries = [
            f"` {i} `  {r.mention}  -  {discord.utils.format_dt(r.created_at, style="R")}  |  ({len(r.members)} members)"
            for i, r in enumerate(roles, start=1)
        ]

        embed = discord.Embed(color=Colors.BASE_COLOR, title=f"role list ({len(entries)})", description="")

        for entry in entries:
            embed.description += f'{entry}\n'
            count += 1

            if count == 10:
                embeds.append(embed)
                embed = discord.Embed(color=Colors.BASE_COLOR, description="", title=f"role list ({len(entries)})")
                count = 0

        if count > 0:
            embeds.append(embed)

        await ctx.paginate(embeds)

    @commands.group(
        name='server',
        aliases=['guild'],
        description='get information about the server.',
        invoke_without_command=True
    )
    async def server(self, ctx: Context):
        return await ctx.send_help(ctx.command)
    
    @server.command(
        name = "icon",
        aliases = ["avatar", "pfp"],
        description="get the server's icon.",
    )
    @cooldown(1, 5, BucketType.user)
    async def server_icon(self, ctx: Context):
        embed = discord.Embed(title = f"{ctx.guild.name}'s icon", color = Colors.BASE_COLOR, url = ctx.guild.icon.url)
        embed.set_image(url=ctx.guild.icon)
        await ctx.reply(embed=embed)

    @server.command(
        name = "banner",
        aliases = ["bnr"],
        description = "Get the server's banner."
    )
    @cooldown(1, 5, BucketType.user)
    async def server_banner(self, ctx: Context):
        if not ctx.guild.banner:
                return await ctx.warn(f"this server doesn't have a **banner**.")
        embed = discord.Embed(title = f"{ctx.guild.name}'s banner", url = ctx.guild.banner.url)
        embed.set_image(url=ctx.guild.banner)
        await ctx.reply(embed=embed)

    @command(
        name = "joinposition",
        aliases = ["joinpos"],
        description = "Get your joinposition."
    )
    @cooldown(1, 5, BucketType.user)
    async def joinposition(self, ctx: Context, *, user: discord.Member = commands.Author):
        join_position = get_ordinal(sorted(ctx.guild.members, key=lambda m: m.joined_at).index(user) + 1)
        return await ctx.neutral(f'{user.name} was the **{join_position}** member to join')

    @command(
        name = "oldnames",
        aliases = ["prevnames", "namehistory", "names"],
        description = "Get your name history."
    )
    @cooldown(1, 5, BucketType.user)
    async def oldnames(self, ctx: Context, *, user: Union[discord.Member, discord.User]= None):
        if user is None:
            user = ctx.author
        
        data = await self.bot.pool.fetch(
            "SELECT oldnames, time FROM names WHERE user_id = $1 ORDER BY time DESC", user.id
        )

        if not data:
            return await ctx.deny(f"{user} has no name history recorded.")

        embed = discord.Embed(
            title=f"{user}'s Name History",
            color=Colors.BASE_COLOR
        )
        
        for entry in data:
            name = entry["name"]
            timestamp = entry["time"]
            time_ago = discord.utils.format_dt(timestamp, style='R')  

            embed.add_field(name=name, value=f"Changed: {time_ago}", inline=False)

        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        await ctx.send(embed=embed)
        

async def setup(bot: Heal):
    await bot.add_cog(Information(bot))
