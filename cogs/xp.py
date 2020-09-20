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

class XP_Leveling(commands.Cog):
    def __init__(self, elvis):
        self.elvis = elvis
    
    def get_xp(self):
        return random.randint(1,10)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content[0] == ".":
            xp = self.get_xp()
            print(f"{message.author.name} gets {xp}xp")
            cursor = mydb.cursor()
            cursor.execute(f"SELECT user_xp, user_level FROM users WHERE client_id = {message.author.id}")
            result = cursor.fetchall()
            if len(result) == 0:
                print("addig to db")
                cursor.execute(f"INSERT INTO users VALUES({message.author.id},{xp}, 1)")
                mydb.commit()
                print("done")
            else:
                new_xp = result[0][0] + xp
                current_level = result[0][1]


                if new_xp < 20:
                    current_level = 1
                elif new_xp > 20 and new_xp < 40:
                    current_level = 2
                elif new_xp > 40 and new_xp < 60:
                    current_level = 3



                print(f"new = {new_xp}") 
                print(f"new level = {current_level}")
                cursor.execute(f"UPDATE users SET user_xp = {new_xp}, user_level = {current_level} WHERE client_id = {message.author.id}")
                mydb.commit()

def setup(elvis):
    elvis.add_cog(XP_Leveling(elvis))