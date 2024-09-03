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
import asyncio
from tools.managers.embedBuilder import EmbedBuilder, EmbedScript
import logging
import random
import string
from tools.managers.cache import Cache

class Server(Cog):
    def __init__(self, bot: Heal):
        self.bot = bot

        
    @hybrid_group(
        description='View guild prefix',
        invoke_without_command=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
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
    @commands.cooldown(1, 5, commands.BucketType.user)
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
        await self.bot.cache.set(f"prefix-{ctx.guild.id}", prefix)
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
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix_remove(self, ctx: Context) -> Message:
        await self.bot.pool.execute(
            """
            DELETE FROM guilds
            WHERE guild_id = $1
            """,
            ctx.guild.id
        )
        await self.bot.cache.remove(f"prefix-{ctx.guild.id}")
        return await ctx.approve(f"Your server's prefix has been **removed**. You can set a **new prefix** using `;prefix set <prefix>`")

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
            description = "Set a welcome channel for the guild."
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
            DO UPDATE SET channel_id = $2
            """,
            ctx.guild.id, channel.id
        )
        await ctx.approve(f"Set the **welcome channel** to {channel.mention}")

    @welcome.command(
            name = "message",
            description = "Set a welcome message for the guild."
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_message(self, ctx: Context, *, message: str = None):
        if message is None:
            return await ctx.send_help(ctx.command)
        
        await self.bot.pool.execute(
                """
                INSERT INTO welcome (guild_id, message)
                VALUES ($1,$2)
                ON CONFLICT (guild_id)
                DO UPDATE SET message = $2
                """,
                ctx.guild.id, message
            )

        processed_message = EmbedBuilder.embed_replacement(ctx.author, message)
        content, embed, view = await EmbedBuilder.to_object(processed_message)
            
        await ctx.approve(f"Set the **welcome** message to:")
        if content or embed:
            await ctx.send(content=content, embed=embed, view=view)
        else:
            await ctx.send(content=processed_message)

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
    name="test",
    description="Test your set welcome message."
    )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcome_test(self, ctx: Context):
        res = await self.bot.pool.fetchrow("SELECT * from welcome WHERE guild_id = $1", ctx.guild.id)

        if res:
            channel_id = res["channel_id"]
            channel = ctx.guild.get_channel(channel_id)

            if channel is None:
                return
            
            message = res["message"]
            processed_message = EmbedBuilder.embed_replacement(ctx.author, message)
            content, embed, view = await EmbedBuilder.to_object(processed_message)
            
            if content or embed:
                await channel.send(content=content, embed=embed, view=view)
            else:
                await channel.send(content=processed_message)
            
            await ctx.approve("Welcome message sent.")
        else:
            return
        

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        res = await self.bot.pool.fetchrow("SELECT * from welcome WHERE guild_id = $1", member.guild.id)

        if res:
            channel_id = res["channel_id"]
            channel = member.guild.get_channel(channel_id)

            if channel is None:
                return
            
            message = res["message"]
            processed_message = EmbedBuilder.embed_replacement(member, message)
            content, embed, view = await EmbedBuilder.to_object(processed_message)
            
            if content or embed:
                await channel.send(content=content, embed=embed, view=view)
            else:
                await channel.send(content=processed_message)

        data = await self.bot.pool.fetch("SELECT channel_id FROM joinping WHERE guild_id = $1", member.guild.id)
        for data in data:
             channel = member.guild.get_channel(data[0])
             if channel:
                message = await channel.send(f"<@{member.id}>")
                await asyncio.sleep(1)
                await message.delete()

    @commands.group(
        name = "joinping",
        aliases = ["poj", "ghostping", "pingonjoin"],
        invoke_without_command=True,
        description = "Add join pings to your server!"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def joinping(self, ctx):
        return await ctx.send_help(ctx.command)
        
    @joinping.command(name="channel", description="Adds or removes a joinping from your guild.", aliases=["chan"])
    @commands.has_permissions(manage_channels = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def joinpingchannel(self, ctx: Context, channel: discord.TextChannel = None):
        if channel is None:
            return await ctx.send_help(ctx.command)

        data = await self.bot.pool.fetchrow("SELECT * FROM joinping WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, channel.id)
        if data:
            await self.bot.pool.execute("DELETE FROM joinping WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, channel.id)
            await ctx.approve(f"Joinping has been disabled from {channel.mention}")
        else:
            await self.bot.pool.execute("INSERT INTO joinping (guild_id, channel_id) VALUES ($1, $2)", ctx.guild.id, channel.id)
            await ctx.approve(f"Joinping has been enabled for {channel.mention}")

    @joinping.command(name="list", description="Get a list of channels which have joinping enabled.")
    @commands.has_permissions(manage_channels = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def joinpinglist(self, ctx: Context):
        data = await self.bot.pool.fetch("SELECT channel_id FROM joinping WHERE guild_id = $1", ctx.guild.id)
        channels = [ctx.guild.get_channel(record['channel_id']).mention for record in data]
        if channels:
            embed = discord.Embed(description=f"Joinping is enabled for:\n" + "\n".join(channels), color= Colors.BASE_COLOR)
            await ctx.send(embed=embed)
        else:
            await ctx.warn(f"Joinping is not set up.")

    @group(
        name = "autorole",
        description = "Enable / disable autorole in your guild.",
        invoke_without_command = True
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_roles = True)
    async def autorole(self, ctx: Context):
        return await ctx.send_help(ctx.command)
    
    @autorole.command(
        name = "enable",
        aliases = ["set", "add"],
        description = "Set an autorole in your guild."
    )
    @commands.has_permissions(manage_roles = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def autorole_enable(self, ctx: Context, *, role: discord.Role = None):
        if role is None:
            return await ctx.send_help(ctx.command)
        
        await self.bot.pool.execute("INSERT INTO autorole (guild_id, role_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET role_id = $2", ctx.guild.id, role.id)
        return await ctx.approve(f"{role.mention} will now be **assigned** upon joining.")

    @autorole.command(
        name = "disable",
        aliases = ["remove", "delete"],
        description = "Disable autorole in your guild."
    )
    @commands.has_permissions(manage_roles = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def autorole_disable(self, ctx: Context, *, role: discord.Role = None):
        if role is None:
            return await ctx.send_help(ctx.command)
        
        await self.bot.pool.execute("DELETE FROM autorole WHERE guild_id = $1 AND role_id = $2", ctx.guild.id, role.id)
        return await ctx.approve(f"{role.mention} will no longer be assigned upon joining.")
    
    @group(
        name = "autoresponder",
        aliases =["autorespond", "ar"],
        description = "Configure autoresponders for your guild.",
        invoke_without_command= True
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def autoresponder(self, ctx: Context):
        return await ctx.send_help(ctx.command)

    @autoresponder.command(
        name = "add",
        aliases = ["set"],
        description = "Setup an autoresponder"
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def autoresponder_add(self, ctx: Context, *, input: str):
        trigger, response = map(str.strip, input.split(",", 1))
        
        existing_entry = await self.bot.pool.fetchrow(
            "SELECT * FROM autoresponder WHERE guild_id = $1 AND trigger = $2",
            ctx.guild.id, trigger
        )

        if existing_entry:
            await ctx.warn(f"An autoresponder for **{trigger}** already exists.")
        else:
            characters = string.ascii_letters
            randomid = ''.join(random.choice(characters) for _ in range(10))
            await self.bot.pool.execute(
                "INSERT INTO autoresponder (guild_id, trigger, response, id) VALUES ($1, $2, $3, $4)",
                ctx.guild.id, trigger, response, randomid
            )
        return await ctx.approve(f"I will respond to **{trigger}** with **{response}**")
    
    @autoresponder.command(
        name = "remove",
        aliases = ["delete"],
        description = "Removes an autoresponder."
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def autoresponder_remove(self, ctx: Context, *, trigger: str):
        await self.bot.pool.execute(
            "DELETE FROM autoresponder WHERE guild_id = $1 AND trigger = $2",
            ctx.guild.id, trigger
        )
        return await ctx.approve(f"I will no longer respond to **{trigger}**")

    @group(
        name = "boostmessage",
        aliases = ["boostmsg"],
        description = "Configure boost messages for your guild.",
        invoke_without_command = True
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boostmessage(self, ctx: Context):
        return await ctx.send_help(ctx.command)

    @boostmessage.command(
        name = "channel",
        aliases = ["chan", "chnl"],
        description = "Set the boost message channel."
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boostmessage_channel(self, ctx: Context, *, channel: discord.TextChannel):
        await self.bot.pool.execute("INSERT INTO boostmessage (guild_id, channel_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET channel_id = $2", ctx.guild.id, channel.id)
        await self.bot.cache.set(f"boostchannel-{ctx.guild.id}", channel.id)
        return await ctx.approve(f"Set the **boost message** channel to {channel.mention}")

    @boostmessage.command(
        name = "message",
        aliases = ["mes", "msg"],
        description = "Set the boost message message."
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boostmessage_message(self, ctx: Context, *, message: str):
        await self.bot.pool.execute("INSERT INTO boostmessage (guild_id, message) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET message = $2", ctx.guild.id, message)
        await self.bot.cache.set(f"boostmessage-{ctx.guild.id}", message)
        processed_message = EmbedBuilder.embed_replacement(ctx.author, message)
        content, embed, view = await EmbedBuilder.to_object(processed_message)
            
        await ctx.approve(f"Set the **boost message** message to:")
        if content or embed:
            await ctx.send(content=content, embed=embed, view=view)
        else:
            await ctx.send(content=processed_message)

    @boostmessage.command(
        name = "test",
        description = "Test the booster message config."
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boostmessage_test(self, ctx: Context):
        message = await self.bot.cache.get(f"boostmessage-{ctx.guild.id}")
        channel_id = await self.bot.cache.get(f"boostchannel-{ctx.guild.id}")

        if message is None or channel_id is None:
            data = await self.bot.pool.fetchrow(
                "SELECT * FROM boostmessage WHERE guild_id = $1", ctx.guild.id
            )
            if data:
                message = message or data["message"]
                channel_id = channel_id or data["channel_id"]

            if message is None or channel_id is None:
                await ctx.warn("Boost message configuration not found.")
                return

            await self.bot.cache.set(f"boostmessage-{ctx.guild.id}", message)
            await self.bot.cache.set(f"boostchannel-{ctx.guild.id}", channel_id)

        channel = ctx.guild.get_channel(channel_id)
        if channel is None:
            await ctx.deny("Channel not found.")
            return

        processed_message = EmbedBuilder.embed_replacement(ctx.author, message)
        content, embed, view = await EmbedBuilder.to_object(processed_message)
        if content or embed:
            await channel.send(content=content, embed=embed, view=view)
        else:
            await channel.send(content=processed_message)


    @boostmessage.command(
        name = "remove",
        description = "Remove the boost message."
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boostmessage_remove(self, ctx: Context):
        data = await self.bot.pool.fetchrow("SELECT * FROM boostmessage WHERE guild_id = $1", ctx.guild.id)
        if data is None:
            return await ctx.warn("There is no boost message setup for this guild.")
        await self.bot.pool.execute("DELETE FROM boostmessage WHERE guild_id = $1", ctx.guild.id)
        return await ctx.approve("Boost message has been disabled.")

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.guild.premium_subscriber_role not in before.roles and after.guild.premium_subscriber_role in after.roles:
            channel = before.guild.system_channel
            if channel is None:
                channel_id = await self.bot.cache.get(f"boostchannel-{before.guild.id}")

                if channel_id is None:
                    res = await self.bot.pool.fetchrow("SELECT * FROM boostmessage WHERE guild_id = $1", before.guild.id)
                    if res:
                        channel_id = res['channel_id']
                        message = res['message']
                        await self.bot.cache.set(f"boostchannel-{before.guild.id}", channel_id)
                        await self.bot.cache.set(f"boostmessage-{before.guild.id}", message)
                    else:
                        return

                channel = before.guild.get_channel(channel_id)

            if channel:
                message = await self.bot.cache.get(f"boostmessage-{before.guild.id}")

                if message is None:
                    res = await self.bot.pool.fetchrow("SELECT * FROM boostmessage WHERE guild_id = $1", before.guild.id)
                    if res:
                        message = res["message"]
                        await self.bot.cache.set(f"boostmessage-{before.guild.id}", message)
                    else:
                        return

                processed_message = EmbedBuilder.embed_replacement(after, message)
                content, embed, view = await EmbedBuilder.to_object(processed_message)

                if content or embed:
                    await channel.send(content=content, embed=embed, view=view)
                else:
                    await channel.send(content=processed_message)
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message): 
        if "MessageType.premium_guild" in str(message.type):
            res = await self.bot.pool.fetchrow("SELECT * FROM boostmessage WHERE guild_id = $1", message.guild.id)
            if res:
                channel = message.guild.get_channel(res['channel_id'])
            
                if channel:

                    boost_message = res["message"]
                    boost_message = await self.bot.cache.get(f"boostmessage-{message.guild.id}", message.id)
                    processed_message = EmbedBuilder.embed_replacement(message.author, boost_message)
                    content, embed, view = await EmbedBuilder.to_object(processed_message)

                    if content or embed:
                        await channel.send(content=content, embed=embed, view=view)
                    else:
                        await channel.send(content=processed_message)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        if before.name != after.name:
            for guild in self.bot.guilds:
                channel_id = await self.bot.cache.get(f"usernames-{guild.id}")
                try:
                    if channel_id:
                        channel = guild.get_channel(channel_id)
                        try:
                            if channel is not None:
                                await channel.send(f"The user **{before.name}** is now available.")
                                await asyncio.sleep(1)
                        except:
                            continue
                except Exception as E:
                    logging.warning(f"Failed to send username tracking in {guild.id}: {E}")


    @group(
        name = "tracker",
        aliases = ["track", "trackers"],
        description = "Configure tracker settings.",
        invoke_without_command = True
    )
    @commands.has_permissions(manage_guild = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tracker(self, ctx: Context):
        return await ctx.send_help(ctx.command)

    @tracker.command(
        name = "usernames",
        aliases = ["users", "names"],
        description = "Configure the username trackings"
    )
    @commands.has_permissions(manage_guild = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tracker_usernames(self, ctx: Context, *, channel: discord.TextChannel):
        existing_channel_id = await self.bot.pool.fetchval("SELECT channel_id FROM usertracker WHERE guild_id = $1", ctx.guild.id)

        if existing_channel_id:
            await self.bot.pool.execute("DELETE FROM usertracker WHERE guild_id = $1", ctx.guild.id)
            await self.bot.cache.remove(f"usernames-{ctx.guild.id}")
            return await ctx.approve("Username tracking will not be sent from now on.")

        if channel:
            await self.bot.pool.execute(
                "INSERT INTO usertracker (guild_id, channel_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET channel_id = EXCLUDED.channel_id",
                ctx.guild.id, channel.id
            )
            await self.bot.cache.set(f"usernames-{ctx.guild.id}", channel.id)
            return await ctx.approve(f"Username tracking will now be sent into {channel.mention}.")

    @tracker.command(
        name = "vanity",
        aliases = ["van", "vanities"],
        description = "Configure vanity tracker."
    )
    @commands.has_permissions(manage_guild = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trackers_vanity(self, ctx: Context, *, channel: discord.TextChannel):
        existing_channel_id = await self.bot.pool.fetchval("SELECT channel_id FROM vanitytracker WHERE guild_id = $1", ctx.guild.id)

        if existing_channel_id:
            await self.bot.pool.execute("DELETE FROM vanitytracker WHERE guild_id = $1", ctx.guild.id)
            await self.bot.cache.remove(f"vanities-{ctx.guild.id}")
            return await ctx.approve("Vanity tracking will not be sent from now on.")

        if channel:
            await self.bot.pool.execute(
                "INSERT INTO vanitytracker (guild_id, channel_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET channel_id = EXCLUDED.channel_id",
                ctx.guild.id, channel.id
            )
            await self.bot.cache.set(f"vanities-{ctx.guild.id}", channel.id)
            return await ctx.approve(f"Vanity tracking will now be sent into {channel.mention}.")

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        if before.vanity_url_code != after.vanity_url_code:
            for guild in self.bot.guilds:
                channel_id = await self.bot.cache.get(f"vanities-{guild.id}")
                try:
                    if channel_id:
                        channel = guild.get_channel(channel_id)
                        try:
                            if channel is not None:
                                if after.vanity_url_code:
                                    message = f"The vanity **{after.vanity_url_code}** is available!"
                                    await channel.send(message)
                                await asyncio.sleep(1)
                        except Exception as e:
                            logging.warning(f"Failed to send vanity URL update in {guild.id}: {e}")
                except Exception as e:
                    logging.warning(f"Failed to fetch vanity channel for {guild.id}: {e}")

    
async def setup(bot: Heal) -> None:
    await bot.add_cog(Server(bot))
    
