import discord 
from get_token import token as TOKEN
from discord.ext import commands

elvis = commands.Bot(command_prefix = "!")

@elvis.event
async def on_ready():
    print("Elvis is up and running!")

elvis.run(TOKEN)



