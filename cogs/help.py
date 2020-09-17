import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, elvis):
        self.elvis = elvis
    
    @commands.command(name = "help")
    async def _help(self, ctx):
        embed = discord.Embed(
            color = discord.Color.from_rgb(244,66,146)
        )
        embed.set_author(name = "Elvis Commands",icon_url="https://media.giphy.com/media/be4QJiw3XbkioIsYbR/giphy.gif")
        embed.set_thumbnail(url="https://media.giphy.com/media/be4QJiw3XbkioIsYbR/giphy.gif")
        embed.add_field(name = "Basic", value = "`.help-basic`")
        embed.add_field(name = "Weather", value = " `.help-weather`")
        embed.add_field(name = "Music", value = "`.help-music`")
        embed.add_field(name = "Leveling", value = "`.help-xp`")
        await ctx.send(embed=embed)
    
    @commands.command(name = "help-basic", aliases = ["helpbasic", "hb", "helpb"])
    async def _help_basic(self, ctx):
        embed = discord.Embed(
            title = "Basic Commands",
            color = discord.Color.from_rgb(244,66,146)
        )
        embed.add_field(name = "`.elvis`", value = "Elvis says hi.", inline = False)
        embed.add_field(name = "`.owner`", value = "Responds with name of the owner of the guild.", inline = False)
        embed.add_field(name = "`.clear [number]`", value = "Owner can delete input number of messages.", inline = False)
        await ctx.send(embed=embed)
    
    

def setup(elvis):
    elvis.add_cog(Help(elvis))