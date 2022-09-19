import asyncio
import discord
import youtube_dl

from typing import Dict
from functools import partial

"""
Massive Cudos to Aditya Tomar for the Stackoverflow post that made this possible 
https://stackoverflow.com/questions/66610012/discord-py-streaming-youtube-live-into-voice
https://stackoverflow.com/users/14940355/aditya-tomar
"""
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdlopts: Dict[str, str] = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts: Dict[str, str] = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdlopts)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester
        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.duration = data.get('duration')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()
        
        # https://www.geeksforgeeks.org/partial-functions-python/
        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if "entries" in data:
            # take the first item from a playlist
            data = data["entries"][0]

        embed = discord.Embed(title="", description=f"Queued [{data['title']}]({data['webpage_url']}) [{ctx.author.mention}]", color=discord.Color.green())
        await ctx.send(embed=embed)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {
                "webpage_url" : data["webpage_url"], 
                "requester" : ctx.author, 
                "title": data["title"]
            }
        
        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data["requester"]
        to_run = partial(ytdl.extract_info, url=data["webpage_url"], download=False)
        data = await loop.run_in_executor(None, to_run)
        ffmpeg = discord.FFmpegPCMAudio(data["url"])

        return cls(ffmpeg, data=data, requester=requester)
