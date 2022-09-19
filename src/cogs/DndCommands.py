import re
import numpy as np
from discord.ext import commands
from typing import Union, Optional
class DndCommands(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        # self.validDiceSizes: List[int] = [
        #     4, 6, 8, 10, 12, 20, 100
        # ]

        self.maxRolls: int = 20
        self.maxDice: int = 1000

    def parseRoll(self, diceString: str):
        if not re.match(r'[0-9]*d[0-9]+', diceString):
            raise ArgumentError(f"Poorly formatted roll string: {diceString}")

        splitArgs = diceString.split('d')
        return int(splitArgs[0]), int(splitArgs[1])

    @commands.command(name="roll", aliases=['r'], description="roll ndx")
    async def rollDice(self, ctx, dice: Union[int, str], number: Optional[int]):
        if number is not None:
            dice, number = number, dice
        elif isinstance(dice, str):
            number, dice = self.parseRoll(dice)
        else:
            number = 1

        if number > self.maxRolls:
            await ctx.send(f"Number of rolls too high. Max rolls: {self.maxRolls}")
            return
        if dice > self.maxDice:
            await ctx.send(f"Dice value too high. Max dice value: {self.maxDice}")
            return

        output = []
        total = 0
        for i in range(number):
            rand_roll = np.random.randint(low=1, high=dice + 1)
            total += rand_roll
            if number == 1:
                output.append(f"{rand_roll}")
                break
            if i < number - 1:
                output.append(f"{rand_roll} + ")
            else:
                output.append(f"{rand_roll} = {total}" )

        await ctx.send(''.join(output))