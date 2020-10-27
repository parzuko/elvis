"""
Created By Jivansh Sharma 
September 2020
@parzuko

"""

import discord
from discord.ext import commands
import requests
from get_token import weather_token

icons = {
    "01d" : "🌞",
    "01n" : "🌜",
    "02d" : "⛅",
    "02n" : "⛅",
    "03d" : "⛅",
    "03n" : "⛅",
    "04d" : "🌂",   
    "04n" : "🌂",
    "09d" : "🌂",
    "09n" : "🌂",
    "10n" : "☔",
    "10d" : "☔",
    "11n" : "☔",
    "11d" : "☔",
    "13n" : "⛄",
    "13d" : "⛄",
    "50n" : "💨",
    "50d" : "💨"
}



class Weather:
    def __init__(self, location):
        self.location = location
    
    def get_info(self):
        weather_key = weather_token
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'APPID': weather_key, "q": self.location, "units": 'metric'}
        response = requests.get(url, params = params)
        weather = response.json()

        return self.organize_data(weather)

    def organize_data(self, information):
        try: 
            name = information['name']
            desc = information['weather'][0]['description']
            temp = information['main']["temp"]
            icon = information['weather'][0]["icon"]

            final_list = [name,desc,temp,icon]
        except:
            final_list = []
        
        return final_list

class GiveWeather(commands.Cog):
    def __init__(self, elvis: commands.Bot):
        self.elvis = elvis

    @commands.command(name = "weather", aliases = ["w", "temp", "mausam"])
    async def _weather(self, ctx: commands.Context, *, location: str = ""):
        """Gives weather of input city."""

        if location == "":
            await ctx.send("Please enter a city you'd like weather from after the `.weather` command.\n\nFor example: `.weather Noida`")
        else:
            result = Weather(location)
            info_list = result.get_info() 
            if len(info_list) != 0:
                embed = (discord.Embed(title='City',
                                    description=f'```{info_list[0]}```',
                                    color=discord.Color.from_rgb(244,66,146))                       
                        )
                embed.add_field(name='Conditions', value=f"{info_list[1].capitalize()}")
                embed.add_field(name='Temperature',value=f"{info_list[2]}°C") 
                embed.add_field(name='Climate', value = f"{icons[info_list[3]]}")

                await ctx.send(embed=embed)
            else:
                await ctx.send("I'm Having a bit of trouble 😅. I'm better at music tho!")

        await ctx.message.add_reaction("🌞")

def setup(elvis):
    elvis.add_cog(GiveWeather(elvis))