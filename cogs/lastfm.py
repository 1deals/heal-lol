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
    hybrid_group,
    is_owner
)
from typing import Union
from discord.ext.tasks import loop
from discord import Member, Guild, Object, User
from asyncio import gather
import traceback

from tools.heal import Heal
from tools.managers.lastfm import FMHandler
from tools.managers.context import Context, Emojis, Colors

class LastFM(Cog):
    def __init__(self, bot: Heal) -> None:
        self.bot = bot
        self.handler = FMHandler

    @hybrid_group(
        name = "lastfm",
        aliases = ["lf", "fm"],
        description = "Interact with LastFM through heal.",
        invoke_without_command = True
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lastfm(self, ctx: Context):
        return await ctx.send_help(ctx.command)
    
    @lastfm.command(
        name = "login",
        aliases = ["link", "set", "connect"],
        description = "Set your LastFM account."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    
    async def lastfm_login(self, ctx: Context, *, lfuser: str = None):
        if lfuser is None:
            return await ctx.send_help(ctx.command)
        
        data = await self.bot.pool.fetchrow("SELECT user_id, lfuser FROM lastfm WHERE lfuser = $1",lfuser)


        if data:
            user_id = data['user_id']
            user = self.bot.get_user(user_id) or await self.bot.fetch_user(user_id)
            return await ctx.deny(f"**{lfuser}** has been registered by {user.mention}")
        
        msg = await ctx.neutral("⚙️ Connecting to LastFM..")
        await self.bot.pool.execute(
            """
            INSERT INTO lastfm (user_id, lfuser)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET lfuser = $2
            """,
            ctx.author.id, lfuser
        )
        embed = Embed(description = f"{Emojis.LASTFM} {ctx.author.mention}: Set your **LastFM** user to **{lfuser}**.", color = Colors.LAST_FM)
        await msg.edit(embed=embed)

    @lastfm.command(
        name = "nowplaying",
        description = "Get your LastFM now playing.",
        aliases = ["np"]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lastfm_nowplaying(self, ctx: Context, *, user: Union[discord.Member, discord.User]= None):
        if user is None:
            user = ctx.author
        await ctx.typing()
        data = await self.bot.pool.fetchrow("SELECT * FROM lastfm WHERE user_id = $1", user.id)
        if not data:
            return await ctx.lastfm(f"**{user.name}** hasn't got their LastFM account linked.")

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

                embed = discord.Embed(
                    color=Colors.BASE_COLOR
                )
                embed.add_field(name = "**Track**", value = f"[{track_name}]({track_url})", inline  = True)
                embed.add_field(name = "**Artist**", value = f"{artist_name}", inline = False)
                embed.set_author(name=f"{lastfm_username}")
                if album_art:
                    embed.set_thumbnail(url=album_art)

                embed.set_footer(text=f"Album: {album_name}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")
                await message.add_reaction("👎")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> Message:
        if message.author.bot:
            return
        data = await self.bot.pool.fetchrow("SELECT command FROM lastfm WHERE user_id = $1", message.author.id)
        if data:
            alias = data['command']
            if message.content.strip().lower() == alias.lower():
                ctx = await self.bot.get_context(message)
                await self.lastfm_nowplaying(ctx, user=message.author)

    @command(
        name = "nowplaying",
        aliases = ["np"]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def nowplaying(self, ctx: Context, *, user: Union[discord.Member, discord.User]= None):
        return await ctx.invoke(self.bot.get_command('lf np'))
    
    @lastfm.command(
        name = "logout",
        aliases = ["remove", "unlink"],
        description = "Unlink your LastFM account from heal."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lastfm_logout(self, ctx: Context):
        data = await self.bot.pool.fetchrow("SELECT * FROM lastfm WHERE user_id = $1", ctx.author.id)
        lfuser = data["lfuser"]
        if not lfuser:
            return await ctx.lastfm(f"You do not have a **LastFM** account linked.")
        
        await self.bot.pool.execute("DELETE FROM lastfm WHERE user_id = $1", ctx.author.id)
        return await ctx.lastfm(f"**Unlinked** your LastFM account successfully")
    
    @lastfm.command(
        name = "variables",
        aliases = ["vars"],
        description = "Get a list of LastFM variables to use in you custom embeds."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lastfm_variables(self, ctx: Context):
        return await ctx.neutral("{track_name} - Gets the name of the track \n{track_url} - Gets the url of the track\n{album_name} - Gets the name of the album \n{artist_name} - Gets the name of the artist(s) \n{album_art} - Gets the album art.")
    
    @lastfm.group(
        name = "customcommand",
        aliases = ["cc"],
        description = "Configure your custom NowPlaying alias."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lastfm_customcommand(self, ctx: Context):
        return await ctx.send_help(ctx.command)
    
    @lastfm_customcommand.command(
        name = "set",
        aliases = ["add"],
        description = "Set your customcommand"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lastfm_customcommand_set(self, ctx: Context, *, customcommand: str = None):
        if customcommand is None:
            return await ctx.send_help(ctx.command)
        
        await self.bot.pool.execute("INSERT INTO lastfm (user_id, command) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET command = $1", ctx.author.id ,customcommand)
        return await ctx.lastfm(f"Set your **custom command** to **`{customcommand}`**")


async def setup(bot: Heal):
    await bot.add_cog(LastFM(bot))