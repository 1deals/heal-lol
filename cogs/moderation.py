import discord
import sys
import humanfriendly
import re 
import datetime

from tools.managers.context     import Context
from discord.ext.commands       import command, group, BucketType, has_permissions
from tools.configuration        import Emojis, Colors
from tools.paginator            import Paginator
from discord.utils              import format_dt
from discord.ext                import commands
from tools.heal                 import Heal
import asyncio
from typing import Union

class Moderation(commands.Cog):
    def __init__(self, bot: Heal) -> None:
        self.bot = bot

    @command(
        name = "lock",
        usage = "lock #channel"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @has_permissions(manage_channels = True)
    async def lock(self, ctx: Context, *, channel: discord.TextChannel = None):

        if channel is None:
            channel = ctx.channel

        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.approve('Channel has been locked.')

    @command(
        name = "unlock",
        usage = "unlock #channel"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @has_permissions(manage_channels = True)
    async def unlock(self, ctx: Context, *, channel: discord.TextChannel = None):

        if channel is None:
            channel = ctx.channel

        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.approve('Channel has been unlocked.')

    @command(
        name = "kick",
        aliases = ["getout", "bye"],
        usage = "kick @fetchrow rule breaker"
    )
    @commands.cooldown(1, 5, BucketType.user)
    @has_permissions(moderate_members=True)
    async def kick(self, ctx: Context, user: discord.Member, *, reason: str = "no reason"):
        reason += ' | executed by {}'.format(ctx.author)
        await ctx.typing()

        try:
            if ctx.author is ctx.guild.owner:
                await user.kick(reason=reason)
                return await ctx.approve(f'Successfully kicked {user.mention} for {reason.split(' |')[0]}')
            if user is ctx.guild.owner:
                return await ctx.warn(f"You're unable to kick the **server owner**.")
            if user is ctx.author:
                return await ctx.warn(f"You're unable to kick **yourself**.")
            if ctx.author.top_role.position <= user.top_role.position:
                return await ctx.warn(f"You're unable to kick a user with a **higher role** than **yourself**.")
            
            await user.kick(reason=reason)
            return await ctx.approve(f'Successfully kicked {user.mention} for {reason.split(' |')[0]}')
        except:
            return await ctx.deny(f'Failed to kick {user.mention}.')
        
    @command(
        name = "ban",
        aliases = ["fuckoff", "banish"],
        usage = "ban @fetchrow raider"
    )
    @commands.cooldown(1, 5, BucketType.user)
    @has_permissions(moderate_members=True)
    async def ban(self, ctx: Context, user: discord.Member, *, reason: str = "no reason"):
        reason += ' | executed by {}'.format(ctx.author)
        await ctx.typing()

        try:
            if user is ctx.guild.owner:
                return await ctx.warn(f"You're unable to ban the **server owner**.")
            if user is ctx.author:
                return await ctx.warn(f"You're unable to ban **yourself**.")
            if ctx.author.top_role.position <= user.top_role.position:
                return await ctx.warn(f"You're unable to ban a user with a **higher role** than **yourself**.")
            
            await user.ban(reason=reason)
            return await ctx.approve(f'Successfully banned {user.mention} for {reason.split(' |')[0]}')
        except:
            return await ctx.deny(f'Failed to ban {user.mention}.')
        
    @commands.command(name='mute', description='mute a user in your server', brief='-mute <user> <time> <reason>')
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mute(self, ctx: Context, user: discord.Member, time: str="60s", *, reason: str = "No reason provided"):
        
        if user.id == self.bot.user.id:
            return await ctx.deny("I cannot **mute** myself.")

        if user.id == ctx.author.id:
            return await ctx.deny("You cannot **mute** yourself.")


        member = ctx.guild.get_member(user.id)
        if member:

            if ctx.author.id != ctx.guild.owner_id:
                if member.top_role.position >= ctx.guild.me.top_role.position:
                    return await ctx.warn("You cannot **mute** a member with a higher role than me.")
                if member.top_role.position >= ctx.author.top_role.position:
                    return await ctx.warn("You cannot **mute** a member with a higher role than you.")
        else:
            pass
        
        time = humanfriendly.parse_timespan(time)

        await user.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)

        if reason:

            await ctx.approve(f"Muted **{user}** for `{humanfriendly.format_timespan(time)}` - **{reason}**")
    
    @commands.command(name='unmute', description='ummute a user in your server', brief='-ummute <user> <reason>')
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unmute(self, ctx: commands.Context, user: discord.Member, *, reason: str = "No reason provided"):
        
        if user.id == self.bot.user.id:
            return await ctx.deny("I cannot **mute** myself.")

        if user.id == ctx.author.id:
            return await ctx.deny("You cannot **mute** yourself.")


        member = ctx.guild.get_member(user.id)
        if member:

            if ctx.author.id != ctx.guild.owner_id:
                if member.top_role.position >= ctx.guild.me.top_role.position:
                    return await ctx.warn("You cannot **mute** a member with a higher role than me.")
                if member.top_role.position >= ctx.author.top_role.position:
                    return await ctx.warn("You cannot **mute** a member with a higher role than you.")
        else:
            pass
        

        await user.timeout(None, reason=reason)

        if reason:

            await ctx.approve(f"Unmuted **{user}**")
    
    @commands.command(
    name="forcenickname",
    aliases=["fn"],
    description="force a nickname upon a user."
    )
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def forcenickname(self, ctx: Context, user: discord.Member, *, name: str = None):
        if name is None:
            check = await self.bot.pool.fetchrow(
                "SELECT name FROM forcenick WHERE guild_id = $1 AND user_id = $2",
                ctx.guild.id, user.id
            )
            if check and check["name"]:
                await self.bot.pool.execute(
                    "DELETE FROM forcenick WHERE guild_id = $1 AND user_id = $2",
                    ctx.guild.id, user.id
                )
                await user.edit(nick=None)
                return await ctx.approve(f"Removed the **forced nickname** from {user.mention}!")
            else:
                return await ctx.deny(f"No forced nickname found for {user.mention}.")
        else:
            check = await self.bot.pool.fetchrow("SELECT * FROM forcenick WHERE user_id = $1 AND guild_id = $2", user.id, ctx.guild.id)               
            if check is None: 
                await self.bot.pool.execute("INSERT INTO forcenick VALUES ($1,$2,$3)", ctx.guild.id, user.id, name)
            else: 
                await self.bot.pool.execute("UPDATE forcenick SET name = $1 WHERE user_id = $2 AND guild_id = $3", name, user.id, ctx.guild.id)  
            await user.edit(nick=name)
            return await ctx.approve(f"Forced **{user.name}'s** nickname to be **`{name}`**!")

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
      if str(before.nick) != str(after.nick): 
        check = await self.bot.pool.fetchrow("SELECT name FROM forcenick WHERE user_id = $1 AND guild_id = $2", before.id, before.guild.id)   
        if check: 
            return await before.edit(nick=check['name'])

    @commands.command(
        name = "purge",
        description = "Purge messages."
    )
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx: Context, *, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        purgemsg = await ctx.approve(f"**Successfully** purged {amount} messages.")
        await asyncio.sleep(2)
        await purgemsg.delete()

    @commands.command(name = "role", aliases = ["r"], description = "Adds a role to mentioned user.", usage = "Syntax: role <user> <role> \nExample: role @psutil owner")
    @commands.has_permissions(manage_roles = True)
    async def role(self, ctx:Context, member: discord.Member = None, *, role: discord.Role = None):
        if member is None or role is None:
            await ctx.send_help(ctx.command)
            return

        if role in member.roles:
            await member.remove_roles(role)
            await ctx.approve(f"**Removed** {role.mention} from **{member.name}**")
        else:
            await member.add_roles(role)
            await ctx.approve(f"**Added** {role.mention} to **{member.name}**")
    
    @commands.command(description="Adds an emoji to your server", usage="steal [emoji] <name>", aliases = ["steal"])
    @commands.has_permissions(manage_expressions = True)
    async def addemoji(self, ctx: Context, emoji: Union[discord.Emoji, discord.PartialEmoji] = None, *, name: str=None):
        if not emoji:
            return await ctx.send_help(ctx.command)
        if not name: 
            name = emoji.name
            emoji = await ctx.guild.create_custom_emoji(image= await emoji.read(), name=name)
            return await ctx.approve(f"added {emoji} as `{name}`")


        

async def setup(bot: Heal):
    await bot.add_cog(Moderation(bot))
