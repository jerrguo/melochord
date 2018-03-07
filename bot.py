import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print ("BOT STARTED UP")
    print ("BOT USERNAME: " + bot.user.name)
    print ("BOT ID: " + bot.user.id)



bot.run('NDIwNzcyMjYwNzMxOTQ0OTcy.DYDn4A.vMAcnvE_N1a7iYehOfXJUk6knAY')
