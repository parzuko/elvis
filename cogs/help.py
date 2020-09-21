import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, elvis: commands.Bot):
        self.elvis = elvis
    
    @commands.command(name = "help")
    async def _help(self, ctx : commands.Context):
        embed = discord.Embed(
            color = discord.Color.from_rgb(244,66,146)
        )
        embed.set_author(name = "Elvis Commands",icon_url="https://media.giphy.com/media/be4QJiw3XbkioIsYbR/giphy.gif")
        embed.set_thumbnail(url="https://media.giphy.com/media/be4QJiw3XbkioIsYbR/giphy.gif")
        embed.add_field(name = "Basic", value = "`.help-basic`")
        embed.add_field(name = "Weather", value = " `.help-weather`")
        embed.add_field(name = "Music", value = "`.help-music`")
        embed.add_field(name = "??", value = "`.help-easter`")
        embed.add_field(name = "Elvis", value = "`.help-elvis`")
        await ctx.send(embed=embed)
    
    @commands.command(name = "help-elvis", aliases = ["jivansh", "parzuko"])
    async def _help_elvis(self, ctx: commands.Context):
        desc = "Hey there I'm @[Parzuko](https://github.com/parzuko) also known as @[jivansh](https://github.com/parzuko) on most social platforms.\n Have a feature you'd like implemented? Get in touch. "
        embed = discord.Embed(
            title = "Who made Elvis?",
            color = discord.Color.from_rgb(244,66,146),
            description = f"{desc}" 
        )
        await ctx.send(embed=embed)

    @commands.command(name = "help-basic", aliases = ["helpbasic", "hb", "helpb"])
    async def _help_basic(self, ctx: commands.Context):
        embed = discord.Embed(
            title = "Basic Commands",
            color = discord.Color.from_rgb(244,66,146)
        )
        embed.add_field(name = "`.elvis`", value = "Elvis says hi.", inline = False)
        embed.add_field(name = "`.owner`", value = "Elvis responds with name of the owner of the guild.", inline = False)
        embed.add_field(name = "`.clear [number]`", value = "Owner can delete input number of messages.", inline = False)
        await ctx.send(embed=embed)
    
    @commands.command(name = "help-weather", aliases = ["helpweather", "hw", "helpw"])
    async def _help_weather(self, ctx: commands.Context):
        embed = discord.Embed(
            title = "Weather Command",
            color = discord.Color.from_rgb(244,66,146)
        )
        embed.add_field(name = "`.weather [city]`", value = "Elivs returns weather of the input city.", inline = False)
        await ctx.send(embed=embed)
    
    @commands.command(name = "help-music", aliases = ["helpmusic", "hm", "helpm", "music"])
    async def _help_music(self, ctx: commands.Context):
        embed = discord.Embed(
            title = "Music Commands",
            color = discord.Color.from_rgb(244,66,146)
        )
        embed.add_field(name = "`.join`", value = "Elvis joins your voice channel.", inline = False)
        embed.add_field(name = "`.go`", value = "Elvis leaves voice channel.", inline = False)
        embed.add_field(name = "`.play [song title]`", value = "Elvis plays requested song.", inline = False)
        embed.add_field(name = "`.stop`", value = "Elvis terminates entire queue of songs", inline = False)
        embed.add_field(name = "`.pause`", value = "Elvis temporarily stops the record", inline = False)
        embed.add_field(name = "`.resume`", value = "Elvis resumes the record where you left off.", inline = False)
        embed.add_field(name = "`.skip`", value = "Elvis skips the current playing song.", inline = False)
        embed.add_field(name = "`.queue`", value = "Elvis displays all songs up next.", inline = False)
        embed.add_field(name = "`.remove [song number]`", value = "Elvis removes song from queue.", inline = False)
        embed.add_field(name = "`.current`", value = "Elvis displays whats currently being played.", inline = False)
        embed.add_field(name = "`.shuffle `", value = "Elvis shuffles your queue of songs.", inline = False)
        await ctx.send(embed=embed)
    
    
    @commands.command(name = "help-easter", aliases = ["eastereggs", "eggs", "hh", "hindi",])
    async def _help_easter(self, ctx: commands.Context):
        embed = discord.Embed(
            title = "Easter Eggs!",
            color = discord.Color.from_rgb(244,66,146)
        )
        embed.add_field(name = "`.sun`", value = "Elvis says hi.", inline = False)
        embed.add_field(name = "`.saaf [number]`", value = "Elvis deletes input number of messages.", inline = False)
        embed.add_field(name = "`.maalik`", value = "Elvis responds with name of the owner of the guild.", inline = False)
        embed.add_field(name = "`.mausam [city]`", value = "Elivs returns weather of the input city.", inline = False)
        embed.add_field(name = "`.aaja`", value = "Elvis joins your voice channel.", inline = False)
        embed.add_field(name = "`.nikal`", value = "Elvis leaves voice channel.", inline = False)
        embed.add_field(name = "`.baja[song title]`", value = "Elvis plays requested song.", inline = False)
        embed.add_field(name = "`.band`", value = "Elvis terminates entire queue of songs", inline = False)
        embed.add_field(name = "`.ruk`", value = "Elvis temporarily stops the record", inline = False)
        embed.add_field(name = "`.wapas`", value = "Elvis resumes the record where you left off.", inline = False)
        embed.add_field(name = "`.agla`", value = "Elvis skips the current playing song.", inline = False)
        embed.add_field(name = "`.iskebaad`", value = "Elvis displays all songs up next.", inline = False)
        embed.add_field(name = "`.hata [song number]`", value = "Elvis removes song from queue.", inline = False)
        embed.add_field(name = "`.abhi`", value = "Elvis displays whats currently being played.", inline = False)
        embed.add_field(name = "`.khichdi `", value = "Elvis shuffles your queue of songs.", inline = False)
        await ctx.send(embed=embed)
    

def setup(elvis):
    elvis.add_cog(Help(elvis))