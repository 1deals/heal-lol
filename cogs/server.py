import discord

from discord import Message
from discord.ext import commands
from discord.ext.commands import (
    Cog,
    hybrid_group,
    group
)
from tools.heal import Heal
from tools.managers.context import Context
from tools.configuration import Colors, Emojis
from typing import Union

class Server(Cog):
    def __init__(self, bot: Heal):
        self.bot = bot

    def variable_replace(self, message, member):
        message = message.replace('{user.mention}', str(member.mention))
        message = message.replace('{user.id}', str(member.id))
        message = message.replace('{guild.name}', (member.guild.name))
        message = message.replace('{guild.count}', str(len(member.guild.members)))
        return message
        
    @hybrid_group(
        description='View guild prefix',
        invoke_without_command=False,
    )
    async def prefix(self, ctx: Context) -> Message:
        return await ctx.neutral(f'**Server Prefix** is set to `{ctx.clean_prefix}`')
        
    @prefix.command(
        name = "set",
        description = "Set command prefix for server",
        aliases=[
            'update',
            'edit',
            'add'
        ]
    )
    @commands.has_permissions(administrator=True)
    async def prefix_edit(self, ctx: Context, prefix: str) -> Message:
        await self.bot.pool.execute(
            """
            INSERT INTO guilds (guild_id, prefix)
            VALUES ($1, $2)
            ON CONFLICT (guild_id)
            DO UPDATE SET prefix = $2
            """,
            ctx.guild.id, prefix
        )
        return await ctx.approve(f"**Server Prefix** updated to `{prefix}`")
    
    @prefix.command(
        name = "remove",
        description = "Remove command prefix for server",
        aliases=[
            'delete',
            'del',
            'clear'
        ]
    )
    @commands.has_permissions(administrator=True)
    async def prefix_remove(self, ctx: Context) -> Message:
        await self.bot.pool.execute(
            """
            DELETE FROM guilds
            WHERE guild_id = $1
            """,
            ctx.guild.id
        )
        return await ctx.approve(f"Your server's prefix has been **removed**. You can set a **new prefix** using `,prefix set <prefix>`")

    @group(
        name = "welcome",
        aliases = ["welcomer", "welc"],
        description = "Toggle the welcome module.",
        invoke_without_command = True
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome(self, ctx: Context):
        return await ctx.send_help(ctx.command)

    @welcome.command(
        name = "channel",
        aliases = ["chan", "chnl"],
        description = "Add the welcome channel."
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_channel(self, ctx: Context, *, channel: discord.TextChannel = None):
        if channel is None:
            return await ctx.send_help(ctx.command)
        
        await self.bot.pool.execute(
            """
            INSERT INTO welcome (guild_id, channel_id) 
            VALUES ($1, $2) 
            ON CONFLICT (guild_id) 
            DO UPDATE SET channel_id = EXCLUDED.channel_id
            """,
            ctx.guild.id, channel.id
        )
        await ctx.approve(f"**Welcome** channel has been configured to: {channel.mention}")

    @welcome.command(
        name = "message",
        aliases = ["msg", "mes"],
        description = "Set the welcome message."
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_message(self, ctx: Context, *, message: str = None):
        if message is None:
            return await ctx.send_help(ctx.command)
        
        await self.bot.pool.execute(
            """
            INSERT INTO welcome (guild_id, message) 
            VALUES ($1, $2) 
            ON CONFLICT (guild_id) 
            DO UPDATE SET message = EXCLUDED.message
            """,
            ctx.guild.id, message
        )
        await ctx.approve(f"Set the **welcome message** to:")
        message_content = self.variable_replace(message, ctx.author)
        await ctx.channel.send(content=message_content)

    @welcome.command(
        name = "remove",
        aliases = ["delete", "del"],
        description = "Delete a welcome message from a channel."
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_remove(self, ctx: Context, *, channel: discord.TextChannel):

        data = await self.bot.pool.fetchrow("SELECT * FROM welcome WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, channel.id)

        if data:
            message = data["message"]

            await self.bot.pool.execute(
                """
                DELETE FROM welcome
                WHERE guild_id = $1 AND channel_id = $2
                """,
                ctx.guild.id, channel.id
            )
            await ctx.approve(f"Removed the **welcome settings** from {channel.mention}!")
        else:
            return await ctx.warn(f"There are no **welcome settings** saved for {channel.mention}.")
        
    @welcome.command(
        name = "test",
        description = "Test your set welcome message."
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_test(self, ctx: Context, channel: discord.TextChannel):
        res = await self.bot.pool.fetchrow("SELECT * from welcome WHERE guild_id = $1", ctx.guild.id)
        if res:
            channel_id = res["channel_id"]
            channel = ctx.guild.get_channel(channel_id)
            if channel is None:
                return await ctx.warn("The channel set for welcome messages does not exist.")
            
            message = res["message"]
            
            message_content = self.variable_replace(message, ctx.author)
            await channel.send(content=message_content)
        

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        res = await self.bot.pool.fetchrow("SELECT * from welcome WHERE guild_id = $1", member.guild.id)
        
        if res:
            channel_id = res['channel_id']
            channel = member.guild.get_channel(channel_id)
            if channel is None:
                return
            message_content = self.variable_replace(res['message'], member)
            await channel.send(content=message_content)
        else:
            return

    
async def setup(bot: Heal) -> None:
    await bot.add_cog(Server(bot))
    