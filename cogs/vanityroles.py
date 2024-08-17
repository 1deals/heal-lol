import discord, logging
from discord.ext import commands, commands
from discord.ext.commands import group, hybrid_group, hybrid_command
from tools.configuration import Colors, Emojis
from tools.heal import Heal
from discord import Embed

from tools.managers.context import Context

class Vanityroles(commands.Cog):
    def __init__(self, bot: Heal):
        self.bot, self.prev_act, self.whitelist = bot, {}, {1183029663149334579}

    @commands.Cog.listener()
    async def on_presence_update(self, _, a):
        try:
            pa, ca = self.prev_act.get(a.id), a.activity.name if a.activity else ''
            if pa != ca:
                self.prev_act[a.id] = ca
                await self.check(a, ca)
        except Exception as e:
            logging.error(f"Error in on_presence_update: {e}")

    async def check(self, m, ca):
        try:
            async with self.bot.pool.acquire() as c:
                r = await c.fetchrow("SELECT channel_id, text, role_id FROM vanityroles WHERE guild_id = $1", m.guild.id)
                if r:
                    cid, t, rid = r['channel_id'], r['text'], r['role_id']
                    role = m.guild.get_role(rid)
                    if t in ca:
                        if role and role not in m.roles:
                            try:
                                await m.add_roles(role)
                            except:
                                pass
                            await self.send(m, t, cid)
                    elif role in m.roles:
                        await m.remove_roles(role)
        except Exception as e:
            logging.error(f"Error in check: {e}")

    async def send(self, m, t, cid):
        try:
            ch = m.guild.get_channel(cid)
            if ch:
                await ch.send(embed=discord.Embed(color=Colors.BASE_COLOR, description=f'{Emojis.APPROVE} Thanks for repping {t}, {m.mention}! <:1bearKissMilk:1271966989640011940>'))
        except Exception as e:
            logging.error(f"Error in send: {e}")


    @hybrid_group(
        name = 'vanityroles',
        description = 'Give roles based on a users status',
        invoke_without_command = True,
        aliases = [
            'vr',
            'vroles'
        ]
    )
    @commands.has_permissions(manage_guild = True)
    async def vanityroles(self, ctx: Context):
        return await ctx.send_help(ctx.command.qualified_name)
    
    @vanityroles.command(
        name = "channel",
        description = "Set the channel to send award logs."
    )
    @commands.has_permissions(manage_guild = True)
    async def vanityroles_channel(self, ctx: Context, *, channel: discord.TextChannel = None):

        if not channel:
            return await ctx.warn(f"You need to mention a **channel**.")
        
        else:

            await self.bot.pool.execute(
                """
                INSERT INTO vanityroles (guild_id, channel_id)
                VALUES ($1, $2)
                ON CONFLICT (guild_id)
                DO UPDATE SET channel_id = $2
                """,
                ctx.guild.id, channel.id
            )
            await ctx.approve(f"Set the vanity channel to {channel.mention}.")

    @vanityroles.command(
        name = "role",
        description = "Set the role to award members."
    )
    @commands.has_permissions(manage_guild = True)
    async def vanityroles_role(self, ctx: Context, *, role: discord.Role = None):

        if not role:
            return await ctx.warn(f"You need to mention a **role**.")
        else:

            await self.bot.pool.execute(
                """
                INSERT INTO vanityroles (guild_id, role_id)
                VALUES ($1, $2)
                ON CONFLICT(guild_id)
                DO UPDATE SET role_id =  $2
                """,
                ctx.guild.id, role.id
            )
            await ctx.approve(f"Set the vanity award role to {role.mention}!")

    @vanityroles.command(
        name = "text",
        aliases = ["vanity", "string"],
        description = "Set the text you want the bot to look for."
    )
    @commands.has_permissions(manage_guild = True)
    async def vanityroles_text(self, ctx: Context, *, text: str = None):

        if not text:
            await ctx.warn(f"A string is needed.")
        else:

            await self.bot.pool.execute(
                """
                INSERT INTO vanityroles (guild_id, text)
                VALUES ($1, $2)
                ON CONFLICT(guild_id)
                DO UPDATE SET text = $2
                """,
                ctx.guild.id, text
            )
            await ctx.approve(f"Set the text to **{text}**!")

    @vanityroles.command(
        name = "test",
        description = "Test the vanityrole system."
    )
    @commands.has_permissions(manage_guild = True)
    async def vanityroles_test(self, ctx: Context):

        data = await self.bot.pool.fetchrow("SELECT role_id, channel_id FROM vanityroles WHERE guild_id = $1", ctx.guild.id)

        if data is None:
            await ctx.warn(f"Vanityrole system has not been set up for this server.")
            return

        role_id = data["role_id"]
        channel_id = data["channel_id"]

        drole = ctx.guild.get_role(role_id)
        dchannel = ctx.guild.get_channel(channel_id)

        if not drole or not dchannel:
            await ctx.warn(f"Vanityrole system has not been set up correctly.")
        else:
            emb = Embed(description = f"{ctx.author.mention} Thanks for repping us! <:pocoyo_shrug:1244434508334235658>", color = Colors.BASE_COLOR)
            await ctx.approve(f"Successfully sent vanity message and gave the role to you!")
            await ctx.author.add_roles(drole)
            await dchannel.send(embed=emb)

    @vanityroles.command(
        name = "disable",
        description = "Disable the vanity role awards.",
        aliases = ["dis", "stop", "remove"]
    )
    @commands.has_permissions(manage_guild = True)
    async def vanityroles_disable(self, ctx: Context):

        data = await self.bot.pool.fetchrow("SELECT guild_id FROM vanityroles WHERE guild_id = $1", ctx.guild.id)

        if data:

            await self.bot.pool.execute(
                """
                DELETE FROM vanityroles
                WHERE guild_id = $1
                """,
                ctx.guild.id
            )

            return await ctx.approve(f"Vanity role has been disabled.")
        
        else:

            return await ctx.deny(f"Vanityroles haven't been setup yet.")

async def setup(bot: Heal):
    await bot.add_cog(Vanityroles(bot))
