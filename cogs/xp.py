"""
Created By Jivansh Sharma 
September 2020
@parzuko

"""

import discord
from discord.ext import commands
import mysql.connector
import random

# This is not an ideal example and would ideally be a database hosted on a server

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "12345",
    database = "userlevels",
    auth_plugin = "mysql_native_password"
)

class XPLeveling(commands.Cog):
    def __init__(self, elvis):
        self.elvis = elvis
    
    def get_xp(self):
        return random.randint(1,5)

    def get_level(self, new_xp):
        current_level = ""

        if new_xp < 20:
            current_level = "Aquintances"
        elif new_xp >= 20 and new_xp < 60:
            current_level = "Friends"
        elif new_xp >= 60 and new_xp < 120:
            current_level = "Best Friends"
        elif new_xp >= 120 and new_xp < 240:
            current_level = "Homies"
        elif new_xp >= 240:
            current_level = "Brothers"
        return current_level    
    

    @commands.command(name="friendship", aliases=["dosti", "xp"])
    async def _xp(self, ctx):
        user_id = ctx.message.author.id
        name = ctx.message.author.name
        cursor = mydb.cursor()
        try:
            cursor.execute(f"SELECT friendship_level FROM xp WHERE client_id = {user_id}")
            result = cursor.fetchall()
            level = result[0][0]
            embed = discord.Embed(
                    title = f"**{name} and Elvis are `{level}`.**",
                    color=discord.Color.teal(),
            )
            await ctx.send(embed=embed)
        except Exception:
            embed = discord.Embed(
                    title = f"**{name} and Elvis are meeting for the first time!**",
                    color=discord.Color.from_rgb(244,66,146),
            )
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content[0] == ".":
            xp = self.get_xp()
            user_id = message.author.id
            name = message.author.name
            cursor = mydb.cursor()
            cursor.execute(f"SELECT user_xp, friendship_level FROM xp WHERE client_id = {user_id}")
            result = cursor.fetchall()
            if len(result) == 0:
                cursor.execute(f"INSERT INTO xp VALUES({user_id},{xp},'Aquintances')") 
                mydb.commit()
                embed = discord.Embed(
                    title = f"**{name} and Elvis are now `Aquintances`**",
                    color=discord.Color.teal()
                )
                await message.channel.send(embed=embed)

            else:
                new_xp = result[0][0] + xp
                current_level = result[0][1]
                flag = False
                new_level = self.get_level(new_xp)
                if current_level != new_level:
                    flag = True
                    current_level = new_level
                cursor.execute(f"UPDATE xp SET user_xp = {new_xp}, friendship_level = '{current_level}' WHERE client_id = {message.author.id}")
                mydb.commit()
                if flag:
                    embed = discord.Embed(
                        title = f"**{name} and Elvis are now `{current_level}`**",
                        color=discord.Color.teal(),
                    )
                    await message.channel.send(embed=embed)



def setup(elvis):
    elvis.add_cog(XPLeveling(elvis))