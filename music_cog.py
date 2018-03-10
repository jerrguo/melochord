import discord
from discord.ext import commands
import asyncio

from song import Song

class Music:

    def __init__(self, bot):
        self.bot = bot
        self.playlist = []
        # self.voice_states = {}

    # async def create_voice_client(self, channel):
    #     voice = await self.bot.join_voice_channel(channel)
    #     state = self.get_voice_state(channel.server)
    #     state.voice = voice

    # Summon bot to current voice channel
    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        channel = ctx.message.author.voice_channel

        # If user is not in a channel
        if channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.bot.voice_client_in(channel.server)

        # If bot is not in a channel
        if state is None:
            state = await self.bot.join_voice_channel(channel)
        # If bot is already in a channel
        else:
            await state.move_to(channel)

        return True

    # Make bot join a specified voice channel
    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        # Identify and attempt to join specified voice channel
        try:
            await self.bot.join_voice_channel(channel)
        # If already in a voice channel
        except discord.ClientException:
            await self.bot.say('Already in a voice channel...')
        # If not such voice channel exists
        except discord.InvalidArgument:
            await self.bot.say('This is not a voice channel...')
        # Successful join
        else:
            await self.bot.say('Ready to play audio in ' + channel.name)















# Holder
