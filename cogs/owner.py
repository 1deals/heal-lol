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
    is_owner
)
from typing import Union
from discord.ext.tasks import loop
from discord import Member, Guild, Object, User
from asyncio import gather
import traceback

from tools.heal import Heal
from tools.managers.context import Context, Emojis, Colors

class Owner(Cog):
    def __init__(self, bot: Heal) -> None:
        self.bot = bot

    @hybrid_command(
        name = "activity",
        aliases = ["status"],
        description = "Change the bots activity status."
    )
    @is_owner()
    
    async def activity(self, ctx: Context, *, activity: str):
        activity = discord.CustomActivity(name=activity)
        await self.bot.change_presence(activity=activity)
        await ctx.approve(f"**Activity** has been set to - `{activity}`")

    @hybrid_command(
        name = "say",
        aliases = ["repeat", "rp"],
        description = "Make the bot repeat the text"
    )
    @is_owner()
    async def say(self, ctx, *, msg: str):
        await ctx.message.delete()
        await ctx.send(msg)


    @commands.group(
        name = "system",
        aliases = ["sys"],
        description = "System commands.",
        invoke_without_command = True
    )
    @is_owner()
    async def system(self, ctx: Context):
        return await ctx.send_help(ctx.command.qualified_name)
    
    @system.command(
        name = "restart",
        aliases = ["rs", "reboot"],
        description = "restarts the bot."
    )
    @is_owner()
    async def system_restart(self, ctx: Context):
        await ctx.approve(f"Restarting bot...")
        os.system("pm2 restart 0")


    @system.command(
        name = "pfp",
        aliases = ["av", "changeav"]
    )
    @is_owner()
    async def system_avatar(self, ctx: Context, *, image: str= None):

        if ctx.message.attachments:
            image_url = ctx.message.attachments[0].url
        elif image:
            image_url = image
        else:
            return await ctx.warn(f"Please provide an image URL or upload an image.")

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    return await ctx.deny(f"Failed to fetch the image.")
                data = await resp.read()

        try:
            await self.bot.user.edit(avatar=data)
            await ctx.approve(f"Changed my **pfp** successfully!")
        except discord.HTTPException as e:
            await ctx.deny(f"Failed to change profile picture: {e}")

    @system.command(
        name = "banner",
        aliases = ["bnr", "changebanner"]
    )
    @is_owner()
    async def system_banner(self, ctx: Context, *, image: str= None):

        if ctx.message.attachments:
            image_url = ctx.message.attachments[0].url
        elif image:
            image_url = image
        else:
            return await ctx.warn(f"Please provide an image URL or upload an image.")

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    return await ctx.deny(f"Failed to fetch the image.")
                data = await resp.read()

        try:
            await self.bot.user.edit(banner=data)
            await ctx.approve(f"Changed my **banner** successfully!")
        except discord.HTTPException as e:
            await ctx.deny(f"Failed to change profile picture: {e}")


    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: Context):

        await ctx.message.add_reaction("⌛")
        await self.bot.tree.sync()
        await ctx.message.clear_reactions()
        return await ctx.message.add_reaction("✅")
    
    @commands.command(
        name = "unblacklist",
        aliases =["unbl"],
        description = "Unblacklist a user."
    )
    @commands.is_owner()
    async def unblacklist(self, ctx: Context, *, user: Union[discord.User, discord.Member]):

        await self.bot.pool.execute(
            """
            DELETE FROM blacklist 
            WHERE user_id = $1
            """,
            user.id
        )

        return await ctx.approve(f"**Unblacklisted** {user.name}")

    @commands.command(
        name = "blacklist",
        aliases =["bl"],
        description = "Blacklist a user."
    )
    @commands.is_owner()
    async def blacklist(self, ctx: Context, *, user: Union[discord.User, discord.Member]):

        await self.bot.pool.execute(
            """
            INSERT INTO blacklist (user_id)
            VALUES ($1)
            ON CONFLICT (user_id)
            DO NOTHING
            """,
            user.id
        )

        return await ctx.approve(f"**Blacklisted** {user.name}")

    @commands.command()
    @commands.is_owner()
    async def gi(self, ctx, identifier: str):
        guild = None

        if identifier.isdigit():
            guild = self.bot.get_guild(int(identifier))
        else:
            guild = discord.utils.get(self.bot.guilds, name=identifier)

        if guild:
            invite = await ctx.send(f"guild > {guild.name}, inv > {await self.generate_invite(guild)}")
        else:
            await ctx.send(f"not in the guild, no perms or wrong id. {identifier}")

    async def generate_invite(self, guild):
        invite = await guild.text_channels[0].create_invite()
        return invite.url

    @commands.command(name="leaveguild", description="Force the bot to leave a guild by its ID.")
    @commands.is_owner() 
    async def leaveguild(self, ctx: Context, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        if guild:
            await guild.leave()
            await ctx.approve(f"Successfully left the guild: {guild.name} (ID: {guild.id})")
        else:
            await ctx.warn(f"Guild with ID {guild_id} not found.")

    @commands.command(
        name = "globalban",
        aliases = ["gban"],
        description = "Global bans a user."
    )
    @commands.is_owner()
    async def globalban(self, ctx: Context, *, member: discord.User):
        if member.id in self.bot.owner_ids:
            return await ctx.deny("You can't global ban a bot owner.")
        if member.id == self.bot.user.id:
            return await ctx.deny(f"Bro tried global banning me from {len(self.bot.guilds)} 💀")

       
        check = await self.bot.pool.fetchrow("SELECT * FROM globalban WHERE user_id = $1", member.id)
        if check is not None:
            return await ctx.warn(f"{member.mention} is already globalbanned.")

       
        guild_ids = [guild.id for guild in self.bot.guilds]

       
        initial_message = await ctx.neutral(f"Globally banning {member.mention}...")

   
        ban_count = 0

      
        for guild in self.bot.guilds:
            if guild.id not in guild_ids:
                continue

            try:
                await guild.ban(member, reason='Globally banned by a bot owner.')
                ban_count += 1
            except Exception as e:
                await ctx.warn(f"Failed to ban in {guild.name}: {e}")


        if ban_count > 0:
            await self.bot.pool.execute("INSERT INTO globalban (user_id) VALUES ($1)", member.id)
            embed = discord.Embed(description = f"Globally banned *{member}** in **{ban_count} guild(s)**!", color = Colors.BASE_COLOR)
            await initial_message.edit(embed=embed)
        else:
            embed = discord.Embed(description=f"Failed to ban **{member}** globally.", color=Colors.BASE_COLOR)
            await initial_message.edit(embed=embed)


async def setup(bot: Heal) -> None:
    await bot.add_cog(Owner(bot))
