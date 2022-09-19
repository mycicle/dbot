# import os
import re
import sys
import traceback
import discord
import numpy as np
from typing import Dict, Callable

class dbot(discord.Client):

    def __init__(self):
        super().__init__()
        self.commands = {
            "play" : self.playURL,
            "flame" : self.flameUser,
            "roll" : self.rollDice
        }
        self.validDiceSizes = [
            4,
            6,
            8,
            10,
            12,
            20,
            100
        ]

        self.maxRolls = 20
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
        
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        print(message.channel)
        if message.author == self.user:
            return
        if message.content == "angelo":
            await message.channel.send("echo")
        if message.content.startswith('!'):
            try:
                command, kwargs = await self.validateCommand(message)
                await self.commands[command](message, **kwargs)

            except:
                traceback.print_exception(*sys.exc_info())
                # self.failedCommands.append()

    async def validateCommand(self, message):
        output = {}
        content = message.content
        splitContent = re.split("\\s", content[1:])
        command = splitContent[0]
        args = splitContent[1:]
        if command not in self.commands.keys():
            raise ValueError(f"Invalid Command: {content}")


        if command == "flame":
            if args[0] not in self.flameDict.keys():
                await message.channel.send(f"I only know how to flame {self.flameDict.keys()}")
                raise ValueError(f"Invalid flame target: {args}")
            
            output["unfortunateSoul"] = args[0]

        if command == "roll":
            if not re.match(r'[0-9]*d[0-9]+', args[0]):
                await message.channel.send(f"Invalid dice args: {args}")
                raise ValueError(f"Invalid dice command: {args}")
            
            try:
                splitArgs = args[0].split('d')
                number_of_dice = int(splitArgs[0])
                dice_to_roll = int(splitArgs[1])

                if number_of_dice == 69 and dice_to_roll == 420:
                    await message.channel.send("nice")
                    raise ValueError("nice")

            except Exception as e:
                raise ValueError(f"Roll Parsing Error: {e}")

            if dice_to_roll not in self.validDiceSizes:
                await message.channel.send(f"Invalid dice size: {dice_to_roll}\nExpected: {self.validDiceSizes}")
                raise ValueError(f"Invalid dice command: {args}")
            if number_of_dice > self.maxRolls:
                await message.channel.send(f"Too many rolls: {args[0]}\nMaximum number of allowed rolls: {self.maxRolls}")
                raise ValueError(f"Invalid dice command: {args}")   

            output["number_of_dice"] = number_of_dice
            output["dice_to_roll"] = dice_to_roll

        return command, output
        
    async def playURL(self, message, **kwargs):
        print(f"playURL called with arg {kwargs}")

    async def flameUser(self, message, **kwargs):
        flames = self.flameDict.get(kwargs.get('unfortunateSoul'))
        flameIndex = np.random.randint(low=0, high=len(flames))

        await message.channel.send(flames[flameIndex])

    async def rollDice(self, message, **kwargs):
        print(type(message.author))
        if str(message.author) == "Mycicle#1857":
            await message.channel.send(f"{kwargs.get('number_of_dice') * kwargs.get('dice_to_roll')}")
            return
        print(kwargs)
        output = []
        total = 0
        number_of_dice = kwargs.get("number_of_dice") 
        for i in range(number_of_dice):

            rand_roll = np.random.randint(low=1, high=kwargs.get('dice_to_roll') + 1)
            total += rand_roll
            if number_of_dice == 1:
                output.append(f"{rand_roll}")
                break
            if i < number_of_dice - 1:
                output.append(f"{rand_roll} + ")
            else:
                output.append(f"{rand_roll} = {total}" )

        await message.channel.send(''.join(output))

    async def goodbye(self):
        await client.get_channel('general').send("Squard shutting down")



if __name__ == "__main__":
    # try:
    client = dbot()
    client.run('')
    # except KeyboardInterrupt:
    #     try:
    #         sys.exit(0)
    #     except SystemExit:
    #         os._exit(0)