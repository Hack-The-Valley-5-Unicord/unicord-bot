from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.group()
    async def owner(self, ctx):
        pass

    @owner.command()
    @commands.is_owner()
    async def logout():
        pass

    @owner.command()
    @commands.is_owner()
    async def addmod():
        pass

    @owner.command()
    @commands.is_owner()
    async def removemod():
        pass