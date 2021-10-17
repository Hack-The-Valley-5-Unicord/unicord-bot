from discord.ext import commands
from discord import Invite, Embed


class Search(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.group()
    async def search(self, ctx):
        pass

    @search.command(aliases=["servers"])
    async def serverlist(self, ctx, university: str, category: str = None):
        university = self.bot.get_university_alias(university)
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                if category != None:
                    guild_set = await conn.fetch(
                        """
                        SELECT guild_id, invite FROM servers
                        WHERE approved = $1
                        AND category = $2
                        AND university = $3
                        """,
                        True,
                        category,
                        university,
                    )
                else:
                    guild_set = await conn.fetch(
                        """
                        SELECT guild_id, invite FROM servers
                        WHERE approved = $1
                        AND university = $2
                        """,
                        True,
                        university,
                    )
        invites = [f"discord.gg/{record['invite']}" for record in guild_set]
        guilds = [await self.bot.fetch_guild(int(record[0])) for record in guild_set]
        embed_items = [f'[{record[0].name}]({record[1]})' for record in zip(guilds, invites)]
        to_send = Embed()
        await ctx.send(embed=to_send)

    # fetch_invite

    @search.command()
    async def serverinfo(self, ctx):
        pass

    @search.command()
    async def removemod():
        pass
