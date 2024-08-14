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
import aiohttp

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
        try:
            total_channels = 0
            for guild in self.bot.guilds:
                    
                total_channels += len(guild.channels)
            uptime = self.bot.uptime
            embed = discord.Embed(timestamp=ctx.message.created_at, colour=Colors.BASE_COLOR)
            embed.add_field(name = f"**{self.bot.user.name}'s statistics**", value = f"**{len(self.bot.guilds)}** guilds \n**{sum(g.member_count for g in self.bot.guilds): ,}** users \n**{total_channels}** channels", inline = False)
            embed.add_field(name = "**Bot**", value = f"**{len(set(command for command in self.bot.walk_commands()if not command.cog_name == 'Jishaku')): ,}** commands \nwebsocket latency: **{round(self.bot.latency * 1000)} ms** \nuptime: **{uptime}**", inline = False)
            embed.set_author(name = self.bot.user.display_name, icon_url = self.bot.user.avatar)
            embed.set_thumbnail(url = self.bot.user.avatar)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e) 

    @hybrid_command(
        name = "ping",
        aliases = ["heartbeat", "latency", "websocket"],
        usage = "ping"
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx: Context):
        list = ["china", "north korea", "your ip", "localhost", "heal", "discord", "your mom", 'horny asian women', 'discord.com', 'google.com', 'healbot.lol', 'instagram', 'onlyfans.com', '911', 'no one', 'tiktok', 'github', 'lucky bro', 'a connection to the server']

        start = time.time()
        message = await ctx.send(content="pong!")
        finished = time.time() - start

        return await message.edit(
            content=f"it took `{int(self.bot.latency * 1000)}ms` to ping **{choice(list)}** (edit: `{finished:.2f}ms`)"
        )

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
        if not data:
            return None

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
                if response.status != 200:
                    return await ctx.deny("Failed to connect to LastFM API.")

                data = await response.json()
                if 'recenttracks' not in data or 'track' not in data['recenttracks']:
                    return await ctx.warn(f"Could not retrieve data for user: {lastfm_username}")

                track_info = data['recenttracks']['track'][0]

                now_playing = track_info.get('@attr', {}).get('nowplaying') == 'true'

                track_name = track_info['name']
                artist_name = track_info['artist']['#text']
                album_name = track_info.get('album', {}).get('#text', 'Unknown Album')
                track_url = track_info['url']
                album_art = track_info['image'][-1]['#text']

        title = f"{user.name}"
        description=""

        if user.id == 187747524646404105:  # me
            title += " <:owner:1270728554388394086> <:staff:1270729949686534206> <:dev:1270730817458405468> "
        if user.id == 392300135323009024:  # xur
            title += " <:staff:1270729949686534206> <:dev:1270730817458405468>"
        if user.id == 461914901624127489:  # logan
            title += " <:zzmilklove2:1270873236841693267> <:staff:1270729949686534206> <:dev:1270730817458405468>"
        if user.id == 1261756025275547719:  # neca
            title += " <:staff:1270729949686534206>"
        if user.id == 1211110597345812501:
                title += " <:staff:1270729949686534206>"
        
        if now_playing:
            description += f"{Emojis.LASTFM} **Listening to [{track_name}]({track_url}) by {artist_name}**"
        else:
            description = ""
            

        embed = discord.Embed(
            title=title,
            description = description,
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
        else:
            pass

        embed.set_thumbnail(url=user.avatar.url)

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
        headers = {"Authorization": "SfHY8HukqUATXUwm"} 

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


async def setup(bot: Heal):
    await bot.add_cog(Information(bot))
