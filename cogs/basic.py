import discord
import sys, os
from discord.ext import commands
import requests

class Basic(commands.Cog):
    def __init__(self, elvis):
        self.elvis = elvis

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Elvis is ready!")

    # Commmands
    @commands.command(aliases = ["Elvis", "sun", "hello"], name = "elvis")
    async def _introduce(self, ctx):
        """Elvis says hi."""

        await ctx.send("Hi! I'm Elvis. Here to listen to all your needs😁. Just type ' .help ' to learn about what I can do! ")

def setup(elvis):
    elvis.add_cog(Basic(elvis))