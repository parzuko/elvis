"""
Created By Jivansh Sharma 
September 2020
@parzuko

"""

import discord
from discord.ext import commands
import requests

class Weather:
    def __init__(self, location):
        self.location = location
    
    def get_oauth(self):
        with open("C:\\Users\\jivan\\Desktop\\auth.txt","r+") as auth_file:
            auth = auth_file.read()
        return auth


    def get_info(self):
        weather_key = self.get_oauth()
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

            final_list = [name,desc,temp]
        except:
            final_list = []
        
        return final_list

class GiveWeather(commands.Cog):
    def __init__(self, elvis):
        self.elvis = elvis

    @commands.command(name = "weather", aliases = ["w","temp","mausam"])
    async def _weather(self,ctx,*,location):
        """Gives weather of input city."""

        result = Weather(location)
        info_list = result.get_info() 
        if len(info_list) != 0 :
            weather = (discord.Embed(title='City',
                                description=f'```{info_list[0]}```',
                                color=discord.Color.red())
                    .add_field(name='Conditions', value=f"{info_list[1].capitalize()}")
                    .add_field(name='Temperature',value=f"{info_list[2]}°C") 
                    )

            await ctx.send(embed=weather)
        else:
            await ctx.send("I'm Having a bit of trouble😅, I'm better at music tho!")


def setup(elvis):
    elvis.add_cog(GiveWeather(elvis))