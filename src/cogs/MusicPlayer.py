import asyncio
import discord
from async_timeout import timeout
from cogs.YTDLSource import YTDLSource

"""
Massive Cudos to Aditya Tomar for the Stackoverflow post that made this possible 
https://stackoverflow.com/questions/66610012/discord-py-streaming-youtube-live-into-voice
https://stackoverflow.com/users/14940355/aditya-tomar
"""

class MusicPlayer:
    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None # Now playing message
        self.volume = 0.5
        self.current = None
        
        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()
            try:
                async with timeout(300):
                    source = await self.queue.get()

            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # source was probably a stream and not downloaded
                # so we should regather to prevent stream expiration
                try:
                    (proc, source) = await YTDLSource.regather_stream(source, loop=self.bot.loop)

                except Exception as e:
                    await self._channel.send(f"There was an error processing your song.\n"
                                             f"```css\n[{e}]\n```")
                    continue
            
            source.volume = self.volume
            self.current = source
            
            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            embed = discord.Embed(title="Now playing", description=f"[{source.title}]({source.web_url}) [{source.requester.mention}]", color=discord.Color.green())
            self.np = await self._channel.send(embed=embed)
            await self.next.wait()

            # make sure the FFMpeg process is cleaned up
            proc.kill()
            self.current = None
        
    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))

