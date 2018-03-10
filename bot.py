import discord
from discord.ext import commands
import asyncio

from music_cog import Music

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

bot = commands.Bot(command_prefix='!')
bot.add_cog(Music(bot))

@bot.event
async def on_ready():
    print ("BOT STARTED UP")
    print ("BOT USERNAME: " + bot.user.name)
    print ("BOT ID: " + bot.user.id)

bot.run('NDIxNTEzNTk5NDg4NDkxNTIw.DYOUpQ.HDnbKD6hDd0wXv0OOWonPSQbZKg')
