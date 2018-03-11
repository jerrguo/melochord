import discord
from discord.ext import commands
import asyncio

from song import Song

class Music:

    def __init__(self, bot):
        self.bot = bot
        self.playlist = asyncio.Queue()
        self.voice_state = "IDLE"

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

    # Play music in voice channel
    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, message_string : str):
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        server = ctx.message.author.server
        state = self.bot.voice_client_in(server)

        if state is None:
            await self.bot.say("Join a voice channel first...")
            return False

        try:
            player = await state.create_ytdl_player(message_string, ytdl_options=opts)
        except Exception as e:
            print ("ERROR 96\n")
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            print ("REACH 100\n")
            song = Song(ctx.message, player)
            await self.bot.say('Enqueued ' + str(song))
            await self.playlist.put(song)
            player.start()
            return song
















# Holder
