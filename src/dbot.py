import discord
from discord.ext import commands

from cogs.DndCommands import DndCommands
from cogs.JokeCommands import JokeCommands
from cogs.MusicCommands import MusicCommands


class dbot(commands.Bot):
    def __init__(self, command_prefix: str):
        super().__init__(command_prefix, intents=discord.Intents.all())

    async def setup_hook(self):
        await self.add_cog(JokeCommands(self))
        await self.add_cog(DndCommands(self))
        await self.add_cog(MusicCommands(self))
    
    async def on_ready(self):
        print("dbot ready")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content == "nice":
            await message.channel.send("heck yeah it is")
        elif message.content == "awesome":
            await message.channel.send("late 16th century (in the sense ‘filled with awe’): from awe + -some")

        await self.process_commands(message)

if __name__ == "__main__":
    client = dbot('!')
    client.run('')