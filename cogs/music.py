import discord
import youtube_dl
import asyncio
import functools
import itertools
import math
import random
from discord.ext import commands
from async_timeout import timeout

class Music(commands.Cog):
    def __init__(self, elvis: commands.Bot):
        self.elvis = elvis
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.elvis, ctx)
            self.voice_states[ctx.guild.id] = state
        
        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.elvis.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage("This command can't be used in DM channels.")

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send(f"An error occurred: {str(error)}")

    @commands.command(name="join", aliases=["j","aaja",])
    async def _join(self, ctx: commands.Context):
        try:
            destination = ctx.author.voice.channel
        except Exception:
            destination = None
        if destination == None:
            await ctx.send("You'll have to join a voice channel before I can do that.")
            await ctx.message.add_reaction("🚫")
        else:
            await ctx.message.add_reaction("🎸")
            if ctx.voice_state.voice:
                await ctx.voice_state.voice.move_to(destination)
                return
            ctx.voice_state.voice = await destination.connect()    
    @commands.command(name="go", aliases=["nikal","leave","disconnect","g"])
    async def _leave(self, ctx: commands.Context):
        if not ctx.voice_state.voice:
            await ctx.message.add_reaction("😥")
            return await ctx.send("I'm not connected to any voice channel!")

        await ctx.voice_state.stop()
        await ctx.message.add_reaction("😓")
        del self.voice_states[ctx.guild.id]

    @commands.command(name="play",aliases=["baja", "p"])
    async def _play(self, ctx: commands.Context, *, search):
        try: 
            if ctx.author.voice.channel == None:
                await ctx.send("You'll have to join a voice channel before I can do that.")
                return await ctx.message.add_reaction("🚫")
        except Exception: 
            await ctx.send("You'll have to join a voice channel before I can do that.")
            return await ctx.message.add_reaction("🚫")
        
        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)
        
        await ctx.send("Just getting the record...")
        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search,loop=self.elvis.loop)
            except Exception:
                await ctx.send("There was a problem 🤔 try again ?")
            else:
                song = Song(source)
                await ctx.voice_state.songs.put(song)
                if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
                    await ctx.send(f"Queued: {str(source)} ! Use `.skip` to skip the current track.")
                else:
                    await ctx.send(f"Time For: {str(source)} !")
            finally:
                await ctx.message.add_reaction("⏯")

    @commands.command(name="stop",aliases=["s","band"])
    async def _stop(self, ctx: commands.Context):
        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction("⏹")  

    @commands.command(name="pause", aliases = ["ruk"])
    async def _pause(self, ctx: commands.Context):
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction("⏸")
        else:
            await ctx.send("But there's nothing to pause.")
    
    @commands.command(name="resume")
    async def _resume(self, ctx: commands.Context):
        try:
            if ctx.voice_state.voice.is_paused():
                ctx.voice_state.voice.resume()
                await ctx.message.add_reaction("▶")
        except Exception:
            await ctx.send("But there's nothing to resume playing.")

    @commands.command(name='skip', aliases=["agla"])
    async def _skip(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing:
            return await ctx.send("Not playing any music right now...")
        else:
            await ctx.message.add_reaction("⏭")
            ctx.voice_state.skip()
    
    @commands.command(name='queue',aliases=["q"])
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("No records lined up! Use `.play` to start!")

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ""
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += f"`{i + 1}.` [**{song.source.title}**]({song.source.url})\n"

        embed = (discord.Embed(
            description=f"There are **{len(ctx.voice_state.songs)}** tracks in queue:\n\n{queue}",
            color = discord.Color.from_rgb(244,66,146)
            ))
        embed.set_footer(text=f"Viewing page {page}/{pages}")
        await ctx.send(embed=embed)
        await ctx.send("To remove a song just say `remove [song number]`")
    
    @commands.command(name="remove",aliases=["delete", "hata"])
    async def _remove(self, ctx: commands.Context, index: int):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("No songs in queue")
        try:
            ctx.voice_state.songs.remove(index - 1)
            await ctx.message.add_reaction("🚮")
        except Exception:
            await ctx.send(f"There aren't {index} songs in queue..")

    @commands.command(name="shuffle",aliases=["randomize","mix"])
    async def _shuffle(self, ctx: commands.Context):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Nothing to randomize!")
        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction("🔀")
    
    @commands.command(name="current", aliases=["abhi", "now", "what"])
    async def _current(self, ctx: commands.Context):
        try:
            await ctx.send(embed=ctx.voice_state.current.create_embed())
        except Exception:
            await ctx.send("Nothing playing at the moment!")

# Incase of YTDL OR FFFMPEGG Erros
youtube_dl.utils.bug_reports_message = lambda: ''

class VoiceError(Exception):
    pass

class YTDLError(Exception):
    pass

# Choosing correct formats for music output in voice channel
class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        "format" : "bestaudio/best",
        "audioformat" : "mp3",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames" : True,
        "extractaudio" : True,
        "noplaylist" : True,
        "nocheckcertificate" : True,
        "ignoreerrors" : False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
    }
    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx : commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5 ):
        super().__init__(source, volume)
        
        self.data = data
        self.requester = ctx.author
        self.channel = ctx.channel

        self.uploader = data.get("uploader")
        self.uploader_url = data.get("uploader_url")
        date = data.get("upload_date")
        self.upload_date = f"{date[6:8]}/{date[4:6]}/{date[0:4]}"
        self.title = data.get("title")
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return f"**{self.title}**"

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError(f"Couldn\'t find anything that matches `{search}`")

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError(f"Couldn\'t find anything that matches `{search}`")

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError(f'Couldn\'t fetch `{webpage_url}`')

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError(f"Couldn\'t retrieve any matches for `{webpage_url}`")

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append(f"{days} days")
        if hours > 0:
            duration.append(f"{hours} hours")
        if minutes > 0:
            duration.append(f"{minutes} minutes")
        if seconds > 0:
            duration.append(f"{seconds} seconds")

        return ', '.join(duration)
    
    
class Song:
    __slots__ = ("source", "requester")

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = discord.Embed(
            title = "Now Playing",
            description = f"```css\n{self.source.title}```",
            color = discord.Color.from_rgb(244,66,146)
        )
        embed.add_field(name="Duration",value=self.source.duration)
        embed.add_field(name="Requested By", value=self.source.requester)
        embed.add_field(name="Uploader",value=f"[{self.source.uploader}]({self.source.uploader_url})")
        embed.add_field(name="URL", value=f"[Click]({self.source.url})")
        embed.set_thumbnail(url=self.source.thumbnail)

        return embed
    
class SongQueue(asyncio.Queue): 
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    # def __iter__(self):
    #     return self._queue.__iter__
    
    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()
    
    def shuffle(self):
        random.shuffle(self._queue)
    
    def remove(self, index: int):
        del self._queue[index]
    

class VoiceState:
    def __init__(self, elvis: commands.Bot, ctx: commands.Context):
        self.elvis = elvis
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next  = asyncio.Event()
        self.songs = SongQueue()
        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()
        self.audio_player = elvis.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop
    
    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                try:
                    async with timeout(240):  # 4 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.elvis.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


def setup(elvis):
    elvis.add_cog(Music(elvis))
