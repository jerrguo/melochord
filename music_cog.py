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
            state = self.bot.voice_client_in(channel.server)
            await self.bot.say('Ready to play audio in ' + channel.name)
            await state.move_to(channel)

        # Successful join
        else:
            await self.bot.say('Ready to play audio in ' + channel.name)

    # Disconnect bot from all voice channels
    @commands.command(pass_context=True, no_pm=True)
    async def disconnect(self, ctx):
        server = ctx.message.author.server
        state = self.bot.voice_client_in(server)
        if state is not None:
            await state.disconnect()
        else:
            await self.bot.say("I'm not in a voice channel...")

    # Clear all messages in text channel
    @commands.command(pass_context=True, no_pm=True)
    async def clearchat(self, ctx):
        message = ctx.message
        try:
            async for msg in self.bot.logs_from(message.channel):
                await self.bot.delete_message(msg)
                await asyncio.sleep(1.2)                                            # 1.2 second delay so the deleting process can be even
        except discord.errors.Forbidden:
            await self.bot.say("I don't have permission to do this...")
        else:
            print ("CHAT CLEAR CONCLUDED")












# Holder
