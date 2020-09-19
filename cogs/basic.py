import discord
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, elvis: commands.Bot):
        self.elvis = elvis

    @commands.Cog.listener()
    async def on_ready(self):
        print("Elvis is ready!")
    
    @commands.command(aliases = ["Elvis", "sun", "hello"], name = "elvis")
    async def _introduce(self, ctx : commands.Context):
        """Elvis says hi."""

        await ctx.send("Hi! I'm Elvis. Here to listen to all your needs 😁. Just type ' .help ' to learn about what I can do! ")
        await ctx.message.add_reaction("👋")

    @commands.command(name = "clear", aliases = ["saaf", "clean", "Clear", "c"])
    async def _clear(self, ctx: commands.Context, amount: int =5):
        owner = str(ctx.message.guild.owner)
        if ctx.message.author == ctx.message.guild.owner:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"Deleted previous {amount} messages! 🧹🧼🧽 ")
        else:
            await ctx.send(f"Sorry! Only `{owner[:-5]}` can ask  me to clean.")

    @commands.command(name = "owner", aliases = ["o", "Owner", "king", "creator", "maalik"])
    async def _who_owner(self, ctx: commands.Context):
        owner = str(ctx.message.guild.owner)[:-5]
        await ctx.send(f"`{owner}` is the creator of this awesome server!")
        await ctx.message.add_reaction("👑")

def setup(elvis):
    elvis.add_cog(Basic(elvis))