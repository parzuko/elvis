import discord
import youtube_dl
from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass

class YTDLError(Exception):
    pass

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
        "logtostderr"": False,
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
