from importlib.abc import ResourceLoader
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def is_user_moderator():
        async def predicate(ctx):
            return await check_moderator(ctx)
        return commands.check(predicate)

    @commands.group()
    async def moderation(self, ctx):
        pass

    @moderation.command(aliases=['servers'])
    @is_user_moderator()
    async def serverlist():
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                guild_set = await conn.fetch(
                    """
                    SELECT guild_id, invite FROM servers
                    WHERE approved = $1
                    """,
                    True
                )
        embed_items = [f'{record}' for record in enumerate(guild_set, 1)]


    @moderation.command(aliases=['uservers, unapproved'])
    @is_user_moderator()
    async def unapprovedserverlist():
        pass

    @moderation.command()
    @is_user_moderator()
    async def approve():
        pass

    @moderation.command()
    @is_user_moderator()
    async def reject():
        pass
    
    @moderation.command()
    @is_user_moderator()
    async def remove():
        pass

async def check_moderator(ctx) -> bool:
    async with ctx.bot.pool.acquire() as conn:
        async with conn.transaction():
            is_moderator = await conn.fetchval("""SELECT EXISTS 
                                                  (SELECT 1 FROM moderators 
                                                  WHERE username=$2)""", 
                                                  str(ctx.author.id)
                                              )
            return is_moderator

def setup(bot):
    bot.add_cog(Moderation(bot))
