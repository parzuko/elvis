"""
Created By Jivansh Sharma 
September 2020
@parzuko

"""

import discord
import os 
from get_token import token as TOKEN
from discord.ext import commands

elvis = commands.Bot(command_prefix = "+")
elvis.remove_command("help")

@elvis.event
async def on_ready():
    print(f'{elvis.user} has logged in.\nStarting loading')
    elvis.load_extension("cogs.weather")
    elvis.load_extension("cogs.basic")
    elvis.load_extension("cogs.help")
    elvis.load_extension("cogs.music")


elvis.run(TOKEN)
