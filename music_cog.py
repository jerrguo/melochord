import discord
from discord.ext import commands
import asyncio

from song import Song

class Music:

    def __init__(self, bot):
        self.bot = bot
        self.audio_player = bot.loop.create_task(self.audio_player_task())                          # Task to control playing of songs
        self.play_next_song = asyncio.Event()                                                       # End of song detection
        self.player = None                                                                          # Current player
        self.songlist = []                                                                          # Queue of songs
        self.paused = False                                                                         # State of player

    # Play the next song in playlist
    def toggle_next(self):
        print ("TOGGLED NEXT")
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    # Audio player task
    async def audio_player_task(self):
        while True:
            print ("AUDIO TASK BEGINNING")
            if (self.player and self.player.is_playing()) or self.paused:
                print ("STOPPED")
                self.player.stop()

            self.songlist = self.songlist[1:]

            if self.songlist:
                self.player = self.songlist[0].player
                print ("PLAYED " + str(self.songlist[0]))
                self.player.start()

            print ("START/NO SONGS CHECKPOINT")
            self.play_next_song.clear()
            print ("END DETECTED\n")
            await self.play_next_song.wait()

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

        self.audio_player = self.bot.loop.create_task(self.audio_player_task())                     # Task to control playing of songs
        self.play_next_song = asyncio.Event()                                                       # End of song detection
        self.player = None                                                                          # Current player
        self.songlist = []                                                                          # Queue of songs
        self.paused = False                                                                         # State of player

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
                await asyncio.sleep(1.2)                                # 1.2 second delay so the deleting process can be even
        except discord.errors.Forbidden:
            await self.bot.say("I don't have permission to do this...")
        else:
            print ("CHAT CLEAR CONCLUDED")

    # Play music in voice channel
    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, message_string : str):
        if (self.player and self.player.is_playing()) or self.paused:
            await self.bot.say("Use !add to add to playlist.")
            return False

        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        server = ctx.message.author.server
        state = self.bot.voice_client_in(server)

        if state is None:
            await self.bot.say("I'm not in a voice channel...")
            return False

        try:
            player = await state.create_ytdl_player(message_string, ytdl_options=opts, after=self.toggle_next)
            player.volume = 0.6
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            song = Song(ctx.message, player)
            await self.bot.say('Enqueued ' + str(song))
            self.songlist.insert(0, song)                       # Add to playlist

            # Check beginning of playlist to determine if this song should be played
            print ("CHECKPOINT PLAY COMMAND")
            self.player = player
            self.player.start()

            return song

    # Adds a song to playlist
    @commands.command(pass_context=True, no_pm=True)
    async def add(self, ctx, *, message_string : str):
        if not self.songlist:
            await self.bot.say('Use !play to start the playlist.')

        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        server = ctx.message.author.server
        state = self.bot.voice_client_in(server)

        if state is None:
            await self.bot.say("I'm not in a voice channel...")
            return False

        try:
            tmpplayer = await state.create_ytdl_player(message_string, ytdl_options=opts, after=self.toggle_next)
            tmpplayer.volume = 0.6
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            print ("CHECKPOINT ADD COMMAND")
            song = Song(ctx.message, tmpplayer)
            await self.bot.say('Enqueued ' + str(song))
            self.songlist.append(song)                          # Add to playlist

            return song

    # Removes a song from playlist
    @commands.command(pass_context=True, no_pm=True)
    async def remove(self, ctx, *, number : int):
        try:
            if number is 1:
                await self.bot.say('Use !skip to skip the song.')
            else:
                await self.bot.say('Removed ' + str(self.songlist[number - 1]))
                self.songlist.pop(number - 1)

        except:
            await self.bot.say('Use !remove [song number] with a valid song number.')

    # Pauses the player
    @commands.command(pass_context=True, no_pm=True)
    async def pause(self):
        if self.player and self.player.is_playing():
            self.paused = True
            self.player.pause()

    # Resumes the player
    @commands.command(pass_context=True, no_pm=True)
    async def resume(self):
        if self.player and not self.player.is_playing():
            self.paused = False
            self.player.resume()

    # Skip currently playing song
    @commands.command(pass_context=True, no_pm=True)
    async def skip(self):
        if (self.player and self.player.is_playing()) or self.paused:
            self.player.stop()
        else:
            await self.bot.say('Nothing to skip...')

    # Adjust volume of player
    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, *, number : float):
        try:
            if int(number) > 100 or int(number) < 0:
                await self.bot.say('Volume must be between 0-100...')
        except:
            await self.bot.say('Volume must be between 0-100...')
        else:
            if self.player and self.player.is_playing():
                self.player.volume = int(number)/100
                await self.bot.say('Set the volume to {:.0%}'.format(self.player.volume))

    # Shows the list of songs in playlist
    @commands.command(pass_context=True, no_pm=True)
    async def playlist(self, ctx):
        return_string = ""

        if not self.songlist:
            await self.bot.say("No songs in playlist.")
            return False

        counter = 1
        for sng in self.songlist:
            return_string = return_string + str(counter) + ': ' + str(sng) + '\n\n'
            counter = counter + 1
        await self.bot.say(return_string)














###
