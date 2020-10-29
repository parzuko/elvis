"""
Created By Jivansh Sharma 
October 2020
@parzuko
"""


import re
import discord
import lavalink
from discord.ext import commands
import random
import math

url_rx = re.compile(r'https?://(?:www\.)?.+')


time_hashmap = {}


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('127.0.0.1', 2333, 'youshallnotpass', 'as', 'default-node')  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        lavalink.add_event_hook(self.track_hook)

    @commands.command(name="search", aliases=["s", "dhundh", "khoj"])
    async def _search(self, ctx, *, query):
        try:
            player = player = self.bot.lavalink.player_manager.get(ctx.guild.id)
            query = f"ytsearch:{query}"
            results = await player.node.get_tracks(query)
            tracks = results['tracks'][0:10]
            i = 0
            query_result = ""
            for track in tracks:
                i += 1
                track_length = track["info"]["length"]
                track_length = self.convert_to_min_and_seconds(track_length)
                query_result = query_result + f'{i}) {track["info"]["title"]} - {track_length}\n'
            await ctx.channel.send(f"```nim\n{query_result}```")

            def check_if_sender_is_requester(reply):
                return reply.author.id == ctx.author.id
            
            response = await self.bot.wait_for('message', check=check_if_sender_is_requester)
            track = tracks[int(response.content)-1]
            
            title = (track["info"]["title"])
            await self._play(ctx, query=title)
            await ctx.send("To remove a song just say `remove [song number]`")

        except Exception as e:
            print(e)

    @commands.command(name="play", aliases=["p", "baja"])
    async def _play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """

        # Get the player for this guild from cache.
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.
        query = query.strip('<>')

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        # Get the results for the query from Lavalink.
        results = await player.node.get_tracks(query)

        # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
        # ALternatively, resullts['tracks'] could be an empty array if the query yielded no tracks.
        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = discord.Embed(color= discord.Color.from_rgb(244,66,146))

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                # Add all of the tracks from the playlist to the queue.
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            who = ctx.author.id
            #print(f"track is {track}")
            if len(player.queue) == 0 and not player.is_playing:
                embed.title = 'Now Playing!'
            else:
                embed.title = "Queued!"
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            embed.add_field(name="Requested By", value = f"<@{who}>")

            track_title = track["info"]["title"]
            track_length = track["info"]["length"]

            if track_title not in time_hashmap:
                time_hashmap[track_title] = track_length

            # You can attach additional information to audiotracks through kwargs, however this involves
            # constructing the AudioTrack class yourself.
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.play()

    @commands.command(name="go", aliases=["disconnect", "leave", "nikal"])
    async def _leave(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            await ctx.message.add_reaction("😥")
            return await ctx.send("I'm not connected to any voice channel!")

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voicechannel!')

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await self.connect_to(ctx.guild.id, None)
        await ctx.message.add_reaction("😓")

    @commands.command(name="join", aliases=["j", "aaja"])
    async def _join(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        
        if not ctx.author.voice:
            await ctx.message.add_reaction("🚫")
            return await ctx.send("You'll have to join a voice channel before I can do that.")

        if player.is_connected and not player.is_playing:
            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
            return await ctx.message.add_reaction("🎸")


    @commands.command(name='queue', aliases=["q"])
    async def _queue(self, ctx, page: int = 1):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if(len(player.queue) == 0):
            return await ctx.send("No records lined up! Use `.play` to start!")

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [{track.title}]({track.uri})\n'

        embed = discord.Embed(colour=discord.Color.from_rgb(244,66,146),
                          description=f'There are **{len(player.queue)} tracks** in queue:\n\n{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.send(embed=embed)
    
    @commands.command(name="pause", aliases=["ruk"])
    async def _pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.paused == False:
            await player.set_pause(True)
            await ctx.message.add_reaction("⏸")

    @commands.command(name="resume", aliases=["wapas"])
    async def _resume(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.paused == True:
            await player.set_pause(False)
            await ctx.message.add_reaction("▶")

    
    @commands.command(name="skip", aliases=["agla", "next"])
    async def _skip(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.is_playing and (len(player.queue) > 0) :
            await player.skip()
            await ctx.message.add_reaction("⏭")
        else:
            await ctx.send("No can do!")

    @commands.command(name="stop", aliases=["band"])
    async def _stop(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.is_playing :
            player.queue.clear()
            await player.stop()
            return await ctx.message.add_reaction("⏹") 

    @commands.command(name="loop", aliases=["phirse", "dobara", "repeat"])
    async def _loop(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.is_playing and player.repeat == False:
            player.repeat = True
            track_name = player.current.title
            await ctx.send(f"Looping {track_name}. Make sure to turn the loop off using the `.loop-off` command!")
            await ctx.message.add_reaction("🔁")

    @commands.command(name="loop-off")
    async def _loopoff(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.is_playing and player.repeat == True:
            player.repeat = False
            track_name = player.current.title
            await ctx.send(f"Wont repeat {track_name} anymore :)")
    

    @commands.command(name="shuffle",aliases=["randomize","mix", "khichdi"])
    async def _shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.is_playing:
            if len(player.queue) > 1 :
                #player.shuffle = not player.shuffle
                random.shuffle(player.queue)
                await ctx.message.add_reaction("🔀")
        else:
            return await ctx.send("Nothing to randomize!")

    @commands.command(name="remove", aliases=["hata", "delete"])
    async def _remove(self, ctx, *, number):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        song_list = player.queue
        if len(song_list) == 0:
            return await ctx.send("No songs in queue")
        index = int(number)  - 1 
        if len(song_list) <= index:
            return await ctx.send("That song doesn't exist!")
        song_list.pop(index)
        await ctx.message.add_reaction("🚮")

    
    @commands.command(name="time", aliases=["kitna", "np", "song", "abhi", "current"])
    async def _time(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.is_playing:
            # Get Current Timestamp
            current_song_position = player.position
            current_song_position_in_min = self.convert_to_min_and_seconds(current_song_position)
            # Get Full Song Length From Memory
            song_name = player.current.title
            song_link = player.current.uri
            song_duration = time_hashmap[song_name]
            song_duration_in_min = self.convert_to_min_and_seconds(song_duration)

            ratio_of_times = (current_song_position/song_duration) * 100
            now_playing_cursor = ""
            ratio_of_times_in_range = ratio_of_times//5 
            # Make The Cursor
            for i in range(20):
                if i == ratio_of_times_in_range:
                    now_playing_cursor += ":small_blue_diamond:"
                else:
                    now_playing_cursor += "▬"


            embed = discord.Embed(color= discord.Color.from_rgb(244,66,146))
            embed.description = f"[{song_name}]({song_link})\n"
            embed.description += f"{now_playing_cursor} {current_song_position_in_min} / {song_duration_in_min}"

            await ctx.send(embed=embed)
        else:
            await ctx.send("Nothings Playing !")


    @commands.command(name="seek", aliases=["goto", "kud"])
    async def _seek(self, ctx, *, time_stamp):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.is_playing:

            if ":" not in time_stamp:
                time_stamp = int(time_stamp)
                time_stamp *= 1000
                return await player.seek(position=time_stamp)
            else:
                the_minute = time_stamp[0]
                the_second = time_stamp[2:]
                time_stamp = self.convert_to_milli(the_minute, the_second)
                return await player.seek(position=time_stamp)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
        should_connect = ctx.command.name in ("play", "join")

        if not ctx.author.voice or not ctx.author.voice.channel:
            # Our cog_command_error handler catches this and sends it to the voicechannel.
            # Exceptions allow us to "short-circuit" command invocation via checks so the
            # execution state of the command goes no further.
            await ctx.message.add_reaction("🚫")
            raise commands.CommandInvokeError("You'll have to join a voice channel before I can do that.")

        if not player.is_connected:
            if not should_connect:
                await ctx.message.add_reaction("🚫")
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                await ctx.message.add_reaction("🚫")
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
            await ctx.message.add_reaction("🎸")
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                await ctx.message.add_reaction("🚫")
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)
    
    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
        # The above looks dirty, we could alternatively use `bot.shards[shard_id].ws` but that assumes
        # the bot instance is an AutoShardedBot.

    def convert_to_min_and_seconds(self, milliseconds: int):
        minutes = milliseconds // 60000
        seconds = round(((milliseconds % 60000) // 1000), 0)
        minutes = int(minutes)
        seconds = int(seconds)
        if len(str(seconds)) == 1:
            seconds = "0" + str(seconds)
        return f"{minutes}:{seconds}"

    def convert_to_milli(self, minute, second):
        minute = int(minute) * 60000
        second = int(second) * 1000
        return minute + second



def setup(bot):
    bot.add_cog(Music(bot))
