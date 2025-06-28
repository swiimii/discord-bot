# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
import json
import os
import random
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
if( os.name == 'nt' ):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


description = '''Sam's bot for choosing between and helping play games.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

def check_data_file():
    """Check if the data file exists, if not create it."""
    if not os.path.exists("_data.json"):
        with open("_data.json", 'w+') as file:
            file.write("{\"available_games\": []}")
            file.close()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


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

class Game_Tools(commands.Cog, name='Game Tools'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def chwazi(self, ctx):
        """Randomly chooses a voice participant."""
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
    
    @commands.command()
    async def roll(ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)


    @commands.command()
    async def choose(ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

class Help_Choosing_Games(commands.Cog, name='Help Choosing Games'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def addgame(self, ctx, *games_names):
        """Records a game played by the user."""
        check_data_file()
        games_names = ' '.join(games_names)
        if not games_names:
            await ctx.send('Please provide one or more game name to record, separated by commas.')
            return
        with open("_data.json", 'r+') as file:
            data = json.load(file)
            for game in [ name.strip() for name in games_names.split(',')]:
                if( game not in data["available_games"]):
                    data["available_games"].append(game)
                    file.seek(0)
                    file.write(json.dumps(data))
                    file.truncate()
                    await ctx.send(f'Game "{game}" has been recorded!')
                else:
                    await ctx.send(f'Game "{game}" is already recorded!')

    @commands.command()
    async def listgames(self, ctx):
        """Lists all recorded games."""
        check_data_file()
        with open("_data.json", 'r+') as file:
            data = json.load(file)
            if data["available_games"]:
                games_list = '\n- '.join(data["available_games"])
                await ctx.send(f'Recorded games: \n- {games_list}')
            else:
                await ctx.send('No games have been recorded yet.')

    @commands.command()
    async def forgetgame(self, ctx, *game_names):
        """Forgets a recorded game."""
        game_names = ' '.join(game_names)
        if not game_names:
            await ctx.send('Please provide one or more game names to forget, separated by commas.')
            return
        check_data_file()
        with open("_data.json", 'r+') as file:
            data = json.load(file)
            for game in [ name.strip() for name in game_names.split(',')]:
                if game in data["available_games"]:
                    data["available_games"].remove(game)
                    file.seek(0)
                    file.write(json.dumps(data))
                    file.truncate()
                    await ctx.send(f'Game "{game}" has been forgotten!')
                else:
                    await ctx.send(f'Game "{game}" is not recorded!')

    @commands.command()
    async def choosegame(self, ctx):
        """Chooses a game from the recorded games."""
        check_data_file()
        with open("_data.json", 'r+') as file:
            data = json.load(file)
            if data["available_games"]:
                chosen_game = random.choice(data["available_games"])
                await ctx.send(f'Randomly selected game: {chosen_game}')
            else:
                await ctx.send('No games have been recorded yet.')

asyncio.run(bot.add_cog(Game_Tools(bot)))
asyncio.run(bot.add_cog(Help_Choosing_Games(bot)))
bot.run(os.getenv("DISCORD_TOKEN"))