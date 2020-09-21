"""
Created By Jivansh Sharma 
September 2020
@parzuko

"""
from config import token_path


with open(f"{token_path}","r+") as token_file:
    token = token_file.read()
