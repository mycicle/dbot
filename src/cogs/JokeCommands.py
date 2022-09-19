import random
from typing import Optional
from discord.ext import commands

class JokeCommands(commands.Cog):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.flameDict = {
            "dan" : [
                "simps for B tier women",
                "ginger"
            ],
            "ryan" : [
                "irish",
            ],
            "angelo" : [
                "white castle",
                "chick-fil-ang",
            ],
            "mike" : [
                "creator"
            ]
        }

        self.failedCommands = []       

    @commands.command(name="flame", aliases=['f', "roast"], description="roasts the input user")
    async def flameUser(self, ctx, *, unfortunate: Optional[str] = None):
        if unfortunate == None:
            unfortunate = random.choice(list(self.flameDict))
        flames = self.flameDict.get(unfortunate, ["I don't know who that is"])
        await ctx.send(random.choice(flames))
