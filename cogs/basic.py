import discord
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, elvis):
        self.elvis = elvis

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Elvis is ready!")




def setup(elvis):
    elvis.add_cog(Basic(elvis))