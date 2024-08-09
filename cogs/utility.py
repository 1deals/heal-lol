import discord
import sys
import aiohttp

from tools.managers.context     import Context
from discord.ext.commands       import command, group, BucketType, cooldown, has_permissions
from tools.configuration        import Emojis, Colors
from tools.paginator            import Paginator
from discord.utils              import format_dt
from discord.ext                import commands
from tools.heal                 import Heal
from discord.ui import View, Button
from typing import Union
import datetime
import shazamio
from shazamio import Shazam, Serialize

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

    @command(
        name = "bots",
        aliases = ["botlist"],
        usage = "bots"
    )
    @cooldown(1, 5, BucketType.user)
    async def bots(self, ctx: Context):
        bots = [member for member in ctx.guild.members if member.bot]
        count = 0
        embeds = []

        if len(bots) == 0:
            return await ctx.warn('There are no **bots** in this server.')

        entries = [
            f"` {i} `  **{b.name}**  (`{b.id}`)"
            for i, b in enumerate(bots, start=1)
        ]

        embed = discord.Embed(color=Colors.BASE_COLOR, title=f"Bot list ({len(entries)})", description="")

        for entry in entries:
            embed.description += f'{entry}\n'
            count += 1

            if count == 10:
                embeds.append(embed)
                embed = discord.Embed(color=Colors.BASE_COLOR, description="", title=f"Bot list ({len(entries)})")
                count = 0

        if count > 0:
            embeds.append(embed)

        for e in embeds:
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

    @command(
        name = "chatgpt",
        aliases = ["openai", "ai", "ask"],
        description = "Ask chatgpt a question."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chatgpt(self, ctx: Context, *, prompt: str):
        await ctx.typing()

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.kastg.xyz/api/ai/llamaV3?prompt={prompt} ") as r:
                response = await r.json()
                await ctx.send(response["result"][0]["response"])


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
            startTime = int(check["time"])
            embed = discord.Embed(
                description=f"> <:steamhappy:1265787000573792397> **welcome back!** you went away <t:{startTime}:R>",
                color=Colors.BASE_COLOR
            )
            await message.channel.send(embed=embed)
            await self.bot.pool.execute("DELETE FROM afk WHERE user_id = $1", message.author.id)  

        if message.mentions:
            for user in message.mentions:
                check = await self.bot.pool.fetchrow("SELECT * FROM afk WHERE user_id = $1", user.id)
                if check:
                    embed = discord.Embed(
                        color=Colors.BASE_COLOR,
                        description=f'> <:steambored:1265785956930420836> {user.mention} is currently **AFK:** `{check["status"]}` - <t:{int(check["time"])}:R>'
                    )
                    await message.channel.send(embed=embed)

    @commands.command(name="shazam", description="Get a track name from sound", aliases = ["sh", "shzm"])
    async def shazam(self, ctx: Context):
        if not ctx.message.attachments:
            return await ctx.send("Please provide a video")
        attachment = ctx.message.attachments[0]
        audio_data = await attachment.read()
        shazam = Shazam()
        song = await shazam.recognize(audio_data)
        if 'track' not in song or 'share' not in song['track']:
            return await ctx.send("Could not recognize the track")
        song_cover_url = song['track']['images'].get('coverart', '')
        embed = discord.Embed(
            color=Colors.BASE_COLOR,
            description=f"> **[{song['track']['share']['text']}]({song['track']['share']['href']})**"
        )
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar.url)
        if song_cover_url:
            embed.set_thumbnail(url=song_cover_url)
        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if message.content == self.bot.user.mention:
            prefix = await self.bot.pool.fetchval("SELECT prefix FROM guilds WHERE guild_id = $1", message.guild.id) or (';')
            embed = discord.Embed(
                title="",
                description=f"> Your **prefixes** are: `{prefix}`",
                color=Colors.BASE_COLOR)
            await message.channel.send(embed=embed)

async def setup(bot: Heal):
    await bot.add_cog(Utility(bot))