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
from collections import defaultdict
import typing
from humanfriendly import format_timespan

class Moderation(commands.Cog):
    """
    Moderation commands.
    """
    def __init__(self, bot: Heal) -> None:
        self.bot = bot
        self.locks = defaultdict(asyncio.Lock)
        self.role_lock = defaultdict(asyncio.Lock)

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
        usage = ""
    )
    @commands.cooldown(1, 5, BucketType.user)
    @has_permissions(moderate_members=True)
    async def ban(self, ctx: Context, user: Union[discord.Member, discord.User], *, reason: str = "no reason"):
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
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def purge(self, ctx: Context, *, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        purgemsg = await ctx.approve(f"**Successfully** purged {amount} messages.")
        await asyncio.sleep(2)
        await purgemsg.delete()

    @commands.command(name = "role", aliases = ["r"], description = "Adds a role to mentioned user.", usage = "Syntax: role <user> <role> \nExample: role @psutil owner")
    @commands.has_permissions(manage_roles = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
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
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def addemoji(self, ctx: Context, emoji: Union[discord.Emoji, discord.PartialEmoji] = None, *, name: str=None):
        if not emoji:
            return await ctx.send_help(ctx.command)
        if not name: 
            name = emoji.name
            emoji = await ctx.guild.create_custom_emoji(image= await emoji.read(), name=name)
            return await ctx.approve(f"added {emoji} as `{name}`")

    @commands.command(
        name = "pin",
        description = "Pins the message you reply to."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pin(self, ctx: Context, *, link: str = None):
        message = None

        if ctx.message.reference:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        elif link:
            pattern = re.compile(r'https://discord.com/channels/(\d+)/(\d+)/(\d+)')
            match = pattern.match(link)
            if match:
                guild_id, channel_id, message_id = map(int, match.groups())
                if guild_id == ctx.guild.id:
                    channel = ctx.guild.get_channel(channel_id)
                    if channel:
                        message = await channel.fetch_message(message_id)

        if message:
            try:
                await message.pin()
            except discord.Forbidden:
                await ctx.warn("I do not have permission to pin messages.")
            except discord.HTTPException as e:
                await ctx.warn(f"Failed to pin the message: {e}")
        else:
            return await ctx.send_help(ctx.command)
        
    @command(
        name = "roleall",
        description = "Gives a role to all users."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @has_permissions(manage_roles = True)
    async def roleall(self, ctx: Context, *, role: discord.Role = None):
        """
        add a role to all members
        """
        if role is None:
            return await ctx.send_help(ctx.command)
        async with self.role_lock[ctx.guild.id]:
            tasks = [
                m.add_roles(role, reason=f"Role all invoked by {ctx.author}")
                for m in ctx.guild.members
                if not role in m.roles
            ]

            if len(tasks) == 0:
                return await ctx.warn(f"Everyone has this role")

            mes = await ctx.neutral(
                f"Giving {role.mention} to **{len(tasks)}** members. This may take around **{format_timespan(0.3*len(tasks))}**"
            )

            await asyncio.gather(*tasks)
            return await mes.edit(
                embed=discord.Embed(
                    color= Colors.BASE_COLOR,
                    description=f"Added {role.mention} to **{len(tasks)}** members",
                )
            )

    @commands.command(
        name = "nuke",
        description = "Nukes a channel."
    )
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nuke(self, ctx: Context, *, channel: discord.TextChannel = None):
        """
        Clone a channel
        """
        if channel is None:
            return await ctx.send_help(ctx.command)
        new = await ctx.channel.clone()
        await new.edit(position=ctx.channel.position, topic=ctx.channel.topic, overwrites=ctx.channel.overwrites)
        await ctx.channel.delete()
        embed = discord.Embed(description = f"**Nuked** by: **{ctx.author}**", color = self.bot.color)
        await new.send(embed=embed)

    @command(
        name = "imute",
        aliases = ["imgmute", "imagemute"],
        description = "Remove image permissions from a user in a channel."
    )
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def imute(self, ctx: Context, member: discord.Member, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(member)
        overwrite.attach_files = False
        overwrite.embed_links = False
        await channel.set_permissions(member, overwrite=overwrite)
        await ctx.approve(f"Removed media permissions from **{member.mention}** in {channel.mention}.")
    
    @command(
        name = "iunmute",
        aliases = ["imgunmute", "imageunmute"],
        description = "Restore someones image permissions in a channel."
    )
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def iunmute(self, ctx: Context, member: discord.Member, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(member)
        overwrite.attach_files = True
        overwrite.embed_links = True
        await channel.set_permissions(member, overwrite=overwrite)
        await ctx.approve(f"Restored media permissions to **{member.mention}** in {channel.mention}.")

    @commands.group(
        name = "thread",
        aliases = ["thr"],
        description = "Thread settings.",
        invoke_without_command = True
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @has_permissions(manage_threads = True)
    async def thread(self, ctx: Context):
        return await ctx.send_help(ctx.command)

    @thread.command(
        name = "rename",
        aliases = ["name"],
        description = "Renames a thread."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @has_permissions(manage_threads = True)
    async def thread_rename(self, ctx: Context, thread: typing.Optional[discord.Thread], *, name: str = None):
        if thread is None:
            if isinstance(ctx.channel, discord.Thread):
                thread = ctx.channel
            if isinstance(ctx.channel, discord.TextChannel):
                return await ctx.deny(f"This channel is not a **thread**.")
        await thread.edit(name=name, reason=f"{ctx.author} renamed the thread.")
        await ctx.approve(f'Renamed the **thread** to **`{name}`**')
    
    @thread.command(
        name = "delete",
        aliases = ["remove"],
        description = "Deletes a thread."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @has_permissions(manage_threads = True)
    async def thread_delete(self, ctx: Context, *, thread: typing.Optional[discord.Thread] = None):
        if thread is None:
            if isinstance(ctx.channel, discord.Thread):
                thread = ctx.channel
            if isinstance(ctx.channel, discord.TextChannel):
                return await ctx.deny(f"This channel is not a **thread**.")
        await thread.delete()

    @thread.command(
        name = "lock",
        aliases = ["close"],
        description = "Lock a thread."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @has_permissions(manage_threads = True)
    async def thread_lock(self, ctx: Context, *, thread: typing.Optional[discord.Thread] = None):
        if thread is None:
            if isinstance(ctx.channel, discord.Thread):
                thread = ctx.channel
            if isinstance(ctx.channel, discord.TextChannel):
                return await ctx.deny(f"This channel is not a **thread**.")
        await thread.edit(locked=True, reason=f"Locked by {ctx.author}")
        await ctx.approve(f"The **thread** has been **locked**.")

    @thread.command(
        name = "unlock",
        aliases = ["open"],
        description = "Unlocks a thread."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @has_permissions(manage_threads = True)
    async def thread_unlock(self, ctx: Context, *, thread: typing.Optional[discord.Thread] = None):
        if thread is None:
            if isinstance(ctx.channel, discord.Thread):
                thread = ctx.channel
            if isinstance(ctx.channel, discord.TextChannel):
                return await ctx.deny(f"This channel is not a **thread**.")
        await thread.edit(locked=False, reason=f"Unlocked by {ctx.author}")
        await ctx.approve(f"The **thread** has been **unlocked**.")

async def setup(bot: Heal):
    await bot.add_cog(Moderation(bot))
