import discord
import os
import asyncpg
import asyncio
import psycopg2
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(verbose=True)
TOKEN = os.getenv("TOKEN")
DB_CONN = os.getenv("DSN")


class UnicordBot(commands.Bot):
    def __init__(self, **kwargs):
        self.pool = None
        self.sync_pool = psycopg2.connect(DB_CONN)
        asyncio.get_event_loop().run_until_complete(self.init_pool(DB_CONN))
        self.university_aliases = {
            frozenset(
                {"Unversity of Toronto Scarborough",
                "UTSC",
                "UofT Scarborough",
                "Scarborough"},
            ): "UTSC",
            frozenset(
                {"University of Toronto St. George",
                "UTSG",
                "UofT St. George",
                "St. George",}
            ): "UTSG",
            frozenset(
                {"University of Toronto Mississauga",
                "UTM",
                "UofT Mississauga",
                "Mississauga",}
            ): "UTM",
            frozenset({"UWaterloo", "UW", "University of Waterloo", "Waterloo"}): "UW",
            frozenset(
                {"University of Western Ontario", "Western", "Western University", "UWO"}
            ): "UWO",
            frozenset(
                {"Ontario Tech University",
                "University of Ontario Institute of Technology",
                "OTech",}
            ): "UOIT",
            frozenset({"McMaster", "McMaster University", "Mac"}): "MAC",
            frozenset({"Ryerson University", "Ryerson", "X University"}): "RU",
            frozenset({"University of Ottawa", "UOttawa", "Ottawa"}): "UOTTAWA",
            frozenset({"Wilfrid Laurier University", "Wilfrid Laurier"}): "WLU",
            frozenset({"York University", "York"}): "YORK",
        }
        super().init(**kwargs)

    async def init_pool(self, dsn: str) -> None:
        self.pool = await asyncpg.create_pool(dsn=dsn)
        print("Pool initialized")

    async def close(self) -> None:
        await self.pool.close()
        await super.close()

    def get_university_alias(self, name: str):
        for key in self.university_aliases.keys():
            if name in key:
                return self.university_aliases[key]
        return -1

bot = UnicordBot(
    command_prefix="u!", owner_ids={291666852533501952, 570392035085910016}
)


@bot.event
async def on_ready():
    print(f"Successfully logged in as {bot.user.name}")
    print("==========================================")


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


extensions = ["moderation", "search", "server"]
if __name__ == "main":
    for extension in extensions:
        try:
            bot.load_extension(f"cogs.{extension}")
        except Exception as e:
            print(f"Could not load extension {extension}")

bot.run(TOKEN)
