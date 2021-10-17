from discord.ext import commands


class Server(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.group()
    async def server(self, ctx):
        pass

    @server.command()
    async def request(self, ctx, category: str, university: str):
        university_alias = self.bot.get_university_alias(university)
        if university_alias != -1:
            invite = await ctx.channel.create_invite(
                reason="Created for listing in Unicord"
            )
            async with self.bot.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        """
                        INSERT INTO servers VALUES
                        ($1, $2, $3, $4, $5)
                        ON CONFLICT DO NOTHING
                        """,
                        str(ctx.guild.id),
                        str(invite.code),
                        category,
                        university_alias,
                        False,
                    )
            await ctx.send(
                "Your request has been successfully entered. Please wait for a response."
            )
        else:
            await ctx.send(
                "The university name you provided was not recognized. Please make sure it is appropriately capitalized. You may check the Github for a list of currently included names."
            )

    @server.command()
    async def unlist(self, ctx):
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    """
                    DELETE FROM servers
                    WHERE guild_id = $1
                    """.str(
                        ctx.guild.id
                    )
                )
        await ctx.send(
            "Your server has been unlisted from Unicord. Thank you for your time with us!"
        )
