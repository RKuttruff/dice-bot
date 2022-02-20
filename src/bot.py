import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

aliases = {}

# Function to read in aliases from statefile.
# Currently a placeholder
def init():
	print('init')

# Function to write out aliases to statefile.
# Currently a placeholder
def stateWrite():
	print('stateWrite')


@bot.event
async def on_ready():
	print(f'{bot.user} is connected to the following guild:\n')
	for guild in bot.guilds:
		print(f'{guild.name}(id: {guild.id})')

@bot.command(name='roll_dice', help='Rolls dice with the numbers of faces given several die can be rolled in one command')
async def roll_die(ctx, *args):
	total = 0
	valid = False
	s = ''
	for arg in args:
		if int(arg) > 0:
			valid = True
			r = random.randint(1, int(arg))
			s = s + str(r) + ' '
			total += r

	if valid:
#		print(s.split())
		await ctx.send('You rolled: ' + ', '.join(s.split()) + '; total = ' + str(total))


@bot.command(name='alias', help='Assign, remove and manage aliases')
async def alias(ctx, *args):
	print('alias command called')

@bot.command(name='roll', help='Roll a set of dice defined by a given alias')
async def roll(ctx, alias):
	print('roll command called')


init()

bot.run(TOKEN)
