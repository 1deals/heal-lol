import discord
import sys
import aiohttp

from tools.managers.context     import Context
from discord.ext.commands       import command, group, BucketType, cooldown, has_permissions, hybrid_command
from tools.configuration        import Emojis, Colors
from tools.paginator            import Paginator
from discord.utils              import format_dt
from discord.ext                import commands
from tools.heal                 import Heal
from discord.ui import View, Button
from typing import Union
from datetime import datetime, timedelta
import humanize
import datetime
import requests


class Utility(commands.Cog):
    def __init__(self, bot: Heal) -> None:
        self.bot = bot
        self.deleted_messages = {}

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


    @commands.Cog.listener("on_message_edit")
    async def process_edits(self, before: discord.Message, after: discord.Message) -> discord.Message:

            if before.content != after.content:
                await self.bot.process_commands(after)


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
            async with session.get(f"https://api.kastg.xyz/api/ai/chatgpt?prompt={prompt}&key=Kastg_OEq0gEfVZzWhVBqV3ghm_free") as r:
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
                    description=f"> Your **prefixes** are: `{guild_prefix}` & `{self_prefix}`",
                    color=Colors.BASE_COLOR)
                await message.channel.send(embed=embed)

        content = message.content.lower()

        
        if "heal" in content and "https://www.tiktok.com" in content:
            words = content.split()
            tiktok_link = None
            for word in words:
                if "tiktok.com" in word:
                    tiktok_link = word
                    break

            if not tiktok_link:
                return

            api_url = f"https://tikwm.com/api/?url={tiktok_link}"
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        
                        viddata = data.get("data")
                        video_url = viddata.get("wmplay")

                        if video_url:
                            await message.channel.send(video_url)
                            await message.delete()
                        else:
                            embed = discord.Embed(
                                description=f"{Emojis.WARN} {message.author.mention}: Failed to retrieve the video from the API.",
                                color=Colors.BASE_COLOR,
                            )
                            await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            description=f"{Emojis.WARN} {message.author.mention}: An error occurred while accessing the API.",
                            color=Colors.BASE_COLOR,
                        )
                        await message.channel.send(embed=embed)

            

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
    async def selfprefix_set(self, ctx: Context, *, prefix: str = None):
        if prefix is None:
            return await ctx.send_help(ctx.command)

        if len(prefix) > 10:
            return await ctx.deny(f"Your **selfprefix** cannot be more than `10` characters long.")

        await self.bot.pool.execute(
            """
            INSERT INTO selfprefix (user_id, prefix)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET prefix = $2
            """,
            ctx.author.id, prefix
        )
        await ctx.approve(f"Your **selfprefix** has been set to **`{prefix}`**")

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
        
    @commands.group(
        name = "tiktok",
        aliases = ["tt"],
        description = "Tiktok commands",
        usage = "tiktok <command>",
        invoke_without_command=True
    )
    async def tiktok(self, ctx: Context):
        await ctx.send_help(ctx.command)


    @tiktok.command(
        name = "user",
        aliases = ["creator"],
        description="get info about a tiktok creator",
    )
    async def tiktok_user(self, ctx: Context, *, user=None):
        if user is None: 
           return await ctx.send_help(ctx.command)
        
        res = requests.get(url=f'https://edgabot.akiomae.com/api/tiktokAPI/index.php?user={user}')
        data = res.json()
        user = data["user"]
        stats = data["stats"]

        embed = discord.Embed(
            title = f"@{user["username"]}",
            url = f'https://tiktok.com/@{user["profileName"]}',
            description = f"Followers: {stats["follower"]} \nFollowing: {stats["following"]} \nVideos posted: {stats["video"]} \nLikes: {stats["like"]}",
            color = Colors.BASE_COLOR
        )
        embed.set_thumbnail(url=user["avatar"])
        await ctx.send(embed=embed)

    

async def setup(bot: Heal):
    await bot.add_cog(Utility(bot))