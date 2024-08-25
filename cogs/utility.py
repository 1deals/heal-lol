import discord
import sys
import aiohttp

from tools.managers.context     import Context
from discord.ext.commands       import command, group, BucketType, cooldown, has_permissions, hybrid_command, hybrid_group
from tools.configuration        import Emojis, Colors
from tools.paginator            import Paginator
from discord.utils              import format_dt
from discord.ext                import commands
from tools.heal                 import Heal
from discord.ui import View, Button
from typing import Union, List
from datetime import datetime, timedelta
import humanize
import datetime
import requests
import io, re
import shazamio
from shazamio import Shazam, Serialize
from PIL import Image, ImageDraw, ImageFont
import random 
from random import choice
from tools.managers.embedBuilder import EmbedBuilder, EmbedScript
from tools.configuration import api
from io import BytesIO
from rembg import remove

class Utility(commands.Cog):
    def __init__(self, bot: Heal) -> None:
        self.bot = bot
        self.deleted_messages = {}



    @commands.Cog.listener("on_message_edit")
    async def process_edits(self, before: discord.Message, after: discord.Message) -> discord.Message:

            if before.content != after.content:
                await self.bot.process_commands(after)


    @hybrid_command(
        name = "chatgpt",
        aliases = ["openai", "ai", "ask"],
        description = "Ask chatgpt a question."
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chatgpt(self, ctx: Context, *, prompt: str):
        await ctx.typing()

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.kastg.xyz/api/ai/llamaV3-large?prompt={prompt}&key=Kastg_OEq0gEfVZzWhVBqV3ghm_free") as r:
                response = await r.json()
                em = discord.Embed(title = f"{prompt}", description = response["result"][0]["response"], color = Colors.BASE_COLOR)
                await ctx.send(embed=em)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild:
            channel_id = message.channel.id
            if channel_id not in self.deleted_messages:
                self.deleted_messages[channel_id] = []
            self.deleted_messages[channel_id].append(message)

    @commands.command(aliases=['s'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def snipe(self, ctx, index: int = 1):
        channel_id = ctx.channel.id
        sniped_messages = self.deleted_messages.get(channel_id, [])

        if sniped_messages:
            if 1 <= index <= len(sniped_messages):
                deleted_message = sniped_messages[-index]

                deleting_user = ctx.guild.get_member(int(deleted_message.author.id))

                message_user = ctx.guild.get_member(int(deleted_message.author.id))

                user_pfp = message_user.avatar.url if message_user.avatar else message_user.default_avatar.url

                embed = discord.Embed(
                    title=f'',
                    description=deleted_message.content,
                    color=Colors.BASE_COLOR
                )
                embed.set_author(name=message_user.display_name, icon_url=user_pfp)
                embed.set_footer(text=f'Page {index} of {len(sniped_messages)}')

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'> {Emojis.WARN} {ctx.author.mention}: Invalid snipe index', color=Colors.BASE_COLOR)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'> {Emojis.DENY} {ctx.author.mention}: No deleted messages to snipe', color=Colors.BASE_COLOR)
            await ctx.send(embed=embed)

    @commands.command(aliases=["cs"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def clearsnipe(self, ctx: Context):
        channel_id = ctx.channel.id
        if channel_id in self.deleted_messages:
            del self.deleted_messages[channel_id]
            await ctx.message.add_reaction("<:1267453852295102495:1270312226816921610>")
        else:
            await ctx.message.add_reaction("<:1267454139592347721:1270312225449447465>")
                
    @commands.command(
        name = "afk",
        aliases = ["away"],
        description = "Let members know your AFK."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def afk(self, ctx: Context, *, status: str = None):

        if status is None:
            status = "AFK"

        await self.bot.pool.execute(
            """
            INSERT INTO afk (user_id, status, time)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id)
            DO NOTHING
            """,
            ctx.author.id, status, int(datetime.datetime.now().timestamp())
        )

        embed = discord.Embed(description= f":zzz: You are now **AFK** - `{status}`", color = Colors.BASE_COLOR)
        await ctx.reply(embed=embed)

    TIKTOK_URL_PATTERN = re.compile(r'(https?://)?(www\.)?(vm\.tiktok\.com|t\.tiktok\.com|www\.tiktok\.com/@[A-Za-z0-9_.-]+/video|www\.tiktok\.com/t)/[A-Za-z0-9_/]+')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        c = await self.bot.pool.fetchval("SELECT prefix FROM guilds WHERE guild_id = $1", message.guild.id) or (';')
        prefix = c

        if message.content.strip().startswith(prefix + "afk"):
            return

        check = await self.bot.pool.fetchrow("SELECT * from afk WHERE user_id = $1", message.author.id)
        if check:
            startTime = datetime.datetime.fromtimestamp(check["time"])  
            now = datetime.datetime.now()
            time_away = humanize.precisedelta(now - startTime)
            
            embed = discord.Embed(
                description=f"> <:steamhappy:1265787000573792397> **welcome back!** you went away **{time_away} ago**",
                color=Colors.BASE_COLOR
            )
            await message.channel.send(embed=embed)
            await self.bot.pool.execute("DELETE FROM afk WHERE user_id = $1", message.author.id)  

        if message.mentions:
            for user in message.mentions:
                check = await self.bot.pool.fetchrow("SELECT * FROM afk WHERE user_id = $1", user.id)
                if check:
                    startTime = datetime.datetime.fromtimestamp(check["time"])  
                    now = datetime.datetime.now()
                    time_away = humanize.precisedelta(now - startTime)
                    embed = discord.Embed(
                        color=Colors.BASE_COLOR,
                        description=f'> <:steambored:1265785956930420836> {user.mention} is currently **AFK:** `{check["status"]}` - **{time_away} ago**'
                    )
                    await message.channel.send(embed=embed)

        if message.author == self.bot.user:
            return
        
        if message.content == self.bot.user.mention:
            guild_prefix = await self.bot.pool.fetchval("SELECT prefix FROM guilds WHERE guild_id = $1", message.guild.id) or (';')
            self_prefix = await self.bot.pool.fetchval("SELECT prefix FROM selfprefix WHERE user_id = $1", message.author.id)
            if not self_prefix:
                embed = discord.Embed(
                    title="",
                    description=f"> Your **prefix** is: `{guild_prefix}`",
                    color=Colors.BASE_COLOR)
                await message.channel.send(embed=embed)
            if self_prefix:
                embed = discord.Embed(
                    title="",
                    description=f"> Your **prefix** is: `{self_prefix}`",
                    color=Colors.BASE_COLOR)
                await message.channel.send(embed=embed)

        # TIKTOK 
        if message.content.lower().startswith('heal '):
            tiktok_link = message.content[5:].strip()
            if self.TIKTOK_URL_PATTERN.match(tiktok_link):
                api_url = f"https://tikwm.com/api/?url={tiktok_link}"

                async with aiohttp.ClientSession() as cs:
                    async with cs.get(api_url) as r:
                        data = await r.json()

                        video_url = data['data']['play']
                        likes = data['data']['digg_count']
                        comments = data['data']['comment_count']
                        shares = data['data']['share_count']
                        description = data['data']['title']
                        username = data["data"]["author"]["unique_id"]
                        avatar = data["data"]["author"]["avatar"]

                        async with cs.get(video_url) as video_response:
                            video_data = await video_response.read()

                            video_file = io.BytesIO(video_data)

                            await message.delete()

                            embed = discord.Embed(description=f"{description}", color=Colors.BASE_COLOR)
                            embed.set_footer(text=f"❤️ {int(likes)} | 💬 {int(comments)} | 🔗 {int(shares)}")
                            embed.set_author(name=f"{username}", icon_url=avatar)

                            await message.channel.send(file=discord.File(fp=video_file, filename="video.mp4"), embed=embed)

            

    @group(
        name = "selfprefix",
        description = "Selfprefix settings.",
        invoke_without_command = True
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def selfprefix(self, ctx: Context):
        return await ctx.send_help(ctx.command)
    
    @selfprefix.command(
        name = "set",
        aliases = ["add", "use"],
        description = "Set your selfprefix"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def selfprefix_set(self, ctx: Context, *, prefix: str):

        if len(prefix) > 7:
            return await ctx.deny("Prefix is too long!")

        try:
            await self.bot.pool.execute(
                "INSERT INTO selfprefix VALUES ($1,$2)", ctx.author.id, prefix
            )
        except:
            await self.bot.pool.execute(
                "UPDATE selfprefix SET prefix = $1 WHERE user_id = $2",
                prefix,
                ctx.author.id,
            )
        finally:
            return await ctx.approve(
                f"Selfprefix **set** to `{prefix}`", reference=ctx.message
            )

    @selfprefix.command(
        name = "remove",
        aliases = ["delete", "del", "clear"],
        description = "Delete your selfprefix."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def selfprefix_remove(self, ctx: Context):
        check = await self.bot.pool.fetchval("SELECT prefix FROM selfprefix WHERE user_id = $1", ctx.author.id)
        if not check:
            return await ctx.deny(f"You dont have a **selfprefix** setup.")
        else:
            await self.bot.pool.execute("DELETE FROM selfprefix WHERE user_id = $1", ctx.author.id)
            return await ctx.approve("Removed your **selfprefix**.")
        
    @hybrid_group(
        name = "tiktok",
        aliases = ["tt"],
        description = "Tiktok commands",
        usage = "tiktok <command>",
        invoke_without_command=True
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tiktok(self, ctx: Context):
        await ctx.send_help(ctx.command)


    @tiktok.command(
        name = "reposter",
        description = "Repost a tiktok video"
    )
    async def tiktok_reposter(self, ctx: Context, *, url: str):
        if self.TIKTOK_URL_PATTERN.match(url):
            api_url = f"https://tikwm.com/api/?url={url}"

            async with aiohttp.ClientSession() as cs:
                async with cs.get(api_url) as r:
                    data = await r.json()

                    video_url = data['data']['play']
                    likes = data['data']['digg_count']
                    comments = data['data']['comment_count']
                    shares = data['data']['share_count']
                    description = data['data']['title']
                    username = data["data"]["author"]["unique_id"]
                    avatar = data["data"]["author"]["avatar"]

                    if 'images' in data['data']:
                        images = data['data']['images']
                        embeds = self.create_slideshow_embeds(description, likes, comments, shares, username, avatar, images)
                        await ctx.paginate(embeds) 
                    else:
                        async with cs.get(video_url) as video_response:
                            video_data = await video_response.read()

                            video_file = io.BytesIO(video_data)
                            embed = discord.Embed(description=f"{description}", color=Colors.BASE_COLOR)
                            embed.set_footer(text=f"❤️ {int(likes)} | 💬 {int(comments)} | 🔗 {int(shares)}")
                            embed.set_author(name=f"{username}", icon_url=avatar)

                            await ctx.send(file=discord.File(fp=video_file, filename="video.mp4"), embed=embed)

    def create_slideshow_embeds(self, description: str, likes: int, comments: int, shares: int, username: str, avatar: str, images: List[str]) -> List[discord.Embed]:
        embeds = []
        for image_url in images:
            embed = discord.Embed(description=f"{description}", color=Colors.BASE_COLOR)
            embed.set_footer(text=f"❤️ {int(likes)} | 💬 {int(comments)} | 🔗 {int(shares)}")
            embed.set_author(name=f"{username}", icon_url=avatar)
            embed.set_image(url=image_url)
            embeds.append(embed)
        return embeds

    @command(
        name = "gif",
        description = "Turns an image into a gif."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gif(self, ctx: Context):
        await ctx.typing()
        if ctx.message.attachments:
            image_url = ctx.message.attachments[0].url
        else:
            try:
                image_url = ctx.message.content.split(" ")[1]
            except IndexError:
                return await ctx.send_help(ctx.command)

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    with io.BytesIO(image_data) as image_binary:
                        image = Image.open(image_binary)

                    
                        gif_buffer = io.BytesIO()
                        image.save(gif_buffer, format='GIF')
                        gif_buffer.seek(0)
                        await ctx.send(file=discord.File(gif_buffer, filename="output.gif"))

    @hybrid_command(
        name = "screenshot",
        aliases = ["ss"],
        description = "Screenshot a website."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def screenshot(self, ctx: Context, *, url: str = None):
        APIKEY = api.luma  
        api_url = "https://api.fulcrum.lol/screenshot"

        params = {"url": url}
        headers = {"Authorization": APIKEY} 

        await ctx.typing()

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, headers=headers) as response:
                if response.status == 200:
                    screenshot_bytes = await response.read()

                    file = discord.File(
                        io.BytesIO(screenshot_bytes), 
                        filename="screenshot.png"
                    )

                    await ctx.send(file=file)
                else:
                    await ctx.deny("Failed to screenshot. Try again later.")
        

    @commands.command(
        name = "createembed",
        aliases = ["ce"],
        description = "Create an embed."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def createembed(self, ctx: Context,  *, code: EmbedScript = None):
        if code is None:
            return await ctx.neutral(f"Create embed code [**here**](https://healbot.lol/embed)")
        await ctx.send(**code)

    @command(
        name = "firstmsg",
        description = "Get the first message in the channel."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def firstmessage(self, ctx: Context):
        await ctx.typing()
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            await ctx.reply(
                view=discord.ui.View().add_item(
                    discord.ui.Button(
                        style=discord.ButtonStyle.link,
                        label="first message",
                        url=message.jump_url,
                    )
                )
            )
    
    @commands.command(name="shazam", description="Get a track name from sound", aliases = ["sh", "shzm"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def shazam(self, ctx: Context):
        if not ctx.message.attachments:
            return await ctx.warn("Please provide a video")
        msg = await ctx.neutral(f"> <:shazam:1273688697753047070> Searching for song..")
        attachment = ctx.message.attachments[0]
        audio_data = await attachment.read()
        shazam = Shazam()

        try:
            song = await shazam.recognize(audio_data)
            if 'track' not in song or 'share' not in song['track']:
                return await ctx.send("Could not recognize the track")
            song_cover_url = song['track']['images'].get('coverart', '')
            embed = discord.Embed(
                color=0x31333b,
                description=f"> <:shazam:1273688697753047070> **[{song['track']['share']['text']}]({song['track']['share']['href']})**"
            )
            embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar.url)
            await msg.edit(embed=embed)
        
        finally:
            if hasattr(shazam, '_session') and shazam._session:
                await shazam._session.close()

    @command(
        name = "poll",
        aliases = ["quickpoll", "qp"],
        description = "Create a poll."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def poll(self, ctx: Context, *, question: str = None):
        await ctx.message.delete()
        emb = discord.Embed(description=question, color = Colors.BASE_COLOR)
        emb.set_author(name=f"{ctx.author.name}")
        message = await ctx.send(embed=emb)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    @hybrid_command(
        name = "removebg",
        aliases = ["rembg", "transparent", "tp"],
        description = "Removes a background from an image."
    )
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def removebg(self, ctx: Context, *, image: str = None):
        if ctx.message.attachments:
            image_url = ctx.message.attachments[0].url
        elif image:
            image_url = image
        else:
            return await ctx.warn("Please provide an image URL or upload an image.")
        
        await ctx.typing()

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    return await ctx.warn("Failed to fetch the image.")
                image_data = await resp.read()

        try:
            input_image = BytesIO(image_data) 
            input_image_bytes = input_image.getvalue() 

            output_image_data = remove(input_image_bytes, force_return_bytes=True)

            output_image = BytesIO(output_image_data)
            output_image.seek(0)

            await ctx.reply(file=discord.File(fp=output_image, filename="output.png"))
        except Exception as e:
            await ctx.deny(f"Failed to remove background: {e}")


async def setup(bot: Heal):
    await bot.add_cog(Utility(bot))