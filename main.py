import discord
import os 
from get_token import token as TOKEN
from discord.ext import commands

elvis = commands.Bot(command_prefix = "!")

for cog in os.listdir("./cogs"):
    if cog.endswith('.py'):
        elvis.load_extension(f"cogs.{cog[:-3]}")

elvis.run(TOKEN)
