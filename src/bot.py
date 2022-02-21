import os
import sys
import random

from threading import Thread

from discord.ext import commands
from dotenv import load_dotenv

from loguru import logger

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def errfilter(r):
	return r["level"].name == "ERROR" or r["level"].name == "CRITICAL"
	
def errfiltercomp(r):
	return r["level"].name != "ERROR" and r["level"].name != "CRITICAL"

logger.add("dicebot_out_{time}.log", rotation="10 MB", filter=errfiltercomp, compression="gz")
logger.add("dicebot_err_{time}.log", rotation="10 MB", filter=errfilter, compression="gz")

logger.remove(0)

bot = commands.Bot(command_prefix='!')

def info(msg):
	logger.info(msg)
	
def err(msg):
	logger.error(msg)

@logger.catch
def usrInput():
	while True:
		cmd = input(":")
		if cmd.lower() == 'quit':
			os._exit(0) 	# Is this the best way? sys.exit doesn't work cause not main thread...

thread = Thread(target=usrInput)

@logger.catch
@bot.event
async def on_ready():
	print(f'{bot.user} is connected to the following guild:\n')
	for guild in bot.guilds:
		print(f'{guild.name}(id: {guild.id})')
	thread.start()

@logger.catch
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
		
try:
	bot.run(TOKEN)
except Exception as e:
	logger.exception(e)
