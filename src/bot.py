import os
import sys
import random

from threading import Thread

from discord.ext import commands
from dotenv import load_dotenv

from loguru import logger

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

def fine(msg):
	logger.fine(msg)
	
def err(msg)
	logger.error(msg)
def usrInput():
	while True:
		cmd = input(":")
		if cmd.lower() == 'quit':
			os._exit(0) 	# Is this the best way? sys.exit doesn't work cause not main thread...

thread = Thread(target=usrInput)

@bot.event
async def on_ready():
	print(f'{bot.user} is connected to the following guild:\n')
	for guild in bot.guilds:
		print(f'{guild.name}(id: {guild.id})')
	thread.start()

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
		

bot.run(TOKEN)
	
