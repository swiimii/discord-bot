# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
import json
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

def check_data_file():
    """Check if the data file exists, if not create it."""
    if not os.path.exists("_data.json"):
        with open("_data.json", "w") as file:
            json.dump({"available_games": []}, file)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def chwazi(ctx):
    """Randomly chooses a member from the current voice channel."""
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        members = [member for member in channel.members if not member.bot]
        if members:
            chosen = random.choice(members)
            await ctx.send(f'Randomly selected: {chosen.display_name}')
        else:
            await ctx.send('No human members found in the voice channel.')
    else:
        await ctx.send('You are not connected to a voice channel.')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@bot.command()
async def recordgame(ctx, game_name: str):
    """Records a game played by the user."""
    check_data_file()
    with open("_data.json", "a") as file:
        data = json.load(file.read())
        if( game_name not in data["available_games"]):
            data["available_games"] += game_name
            file.write(json.dumps(data))
            await ctx.send(f'Game "{game_name}" has been recorded!')
        else:
            await ctx.send(f'Game "{game_name}" is already recorded!')

@bot.command()
async def listgames(ctx):
    """Lists all recorded games."""
    check_data_file()
    with open("_data.json", "r") as file:
        data = json.load(file.read())
        if data["available_games"]:
            games_list = ', '.join(data["available_games"])
            await ctx.send(f'Recorded games: {games_list}')
        else:
            await ctx.send('No games have been recorded yet.')

@bot.command()
async def forgetgame(ctx, game_name: str):
    """Forgets a recorded game."""
    check_data_file()
    with open("_data.json", "r") as file:
        data = json.load(file.read())
        if game_name in data["available_games"]:
            data["available_games"].remove(game_name)
            with open("_data.json", "w") as write_file:
                json.dump(data, write_file)
            await ctx.send(f'Game "{game_name}" has been forgotten!')
        else:
            await ctx.send(f'Game "{game_name}" is not recorded!')

bot.command()
async def choosegame(ctx):
    """Chooses a game from the recorded games."""
    check_data_file()
    with open("_data.json", "r") as file:
        data = json.load(file.read())
        if data["available_games"]:
            chosen_game = random.choice(data["available_games"])
            await ctx.send(f'Randomly selected game: {chosen_game}')
        else:
            await ctx.send('No games have been recorded yet.')

bot.run(os.getenv("DISCORD_TOKEN"))