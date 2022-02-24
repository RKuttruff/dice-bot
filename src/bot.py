#Copyright (C) 2022  Riley Kuttruff
#
#	This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#	Public License for more details.
#
#	You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os, sys, random, json, zipfile

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

aliases = {}

def info(msg):
	logger.info(msg)
	
def err(msg):
	logger.error(msg)
  
# Function to read in aliases from statefile.
# Currently a placeholder
def init():
	info('reading aliases from aliases.json')
	f = open("aliases.json", "r")
	aliases = json.loads(f.read())

# Function to write out aliases to statefile.
# Currently a placeholder
def stateWrite():
	info('serializing alias dict to json')
	aliasStr = json.dumps(aliases)
	info('writing to aliases.json')
	try:
		f = open("aliases.json", "w")
		f.write(aliasStr)
		f.close()
	except:
		err('State output failed!')
		err('Emergency alias dump: ')
		err(aliasStr)

@logger.catch
def usrInput():
	while True:
		cmd = input(":")
		if cmd.lower() == 'quit':
			info("Quit command recieved: exiting")
			stateWrite()
			os._exit(0) 	# Is this the best way? sys.exit doesn't work cause not main thread...

thread = Thread(target=usrInput)

def guildHasAliases(guild):
	return guild.id in aliases.keys()
	
@logger.catch
@bot.event
async def on_ready():
	logstr = f'{bot.user} is connected to the following guild(s):\n'
	for guild in bot.guilds:
		logstr += f'\t-{guild.name}(id: {guild.id})'
	
	info(logstr)
	
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
		await ctx.reply('You rolled: ' + ', '.join(s.split()) + '; total = ' + str(total))
 
@logger.catch
@bot.command(name='alias', help='Assign, remove and manage aliases')
async def alias(ctx, *args):
	info('alias command called')
	
	try:
		args = list(args)
		
		if len(args) > 0:
			subcmd = args.pop(0).lower()
			gid = ctx.guild.id
			
			if subcmd == 'add':
				pass
			elif subcmd == 'remove':
				pass
			elif subcmd == 'list':
				pass
			elif subcmd == 'purge':
				if guildHasAliases(gid):
					info(f'Purging aliases for guild {gid}')
					del aliases[gid]
					stateWrite()
					await ctx.reply("Aliases purged successfully")
				else:
					await ctx.reply("No aliases to purge")
			else:
				await ctx.reply("Invalid subcommand. Valid subcommands are: `add`, `remove`, `list` and `purge`")
		else:
			await ctx.reply("You must provide an argument! See !help for more")
	except Exception as e:
		logger.exception(e)

@logger.catch
@bot.command(name='roll', help='Roll a set of dice defined by a given alias')
async def roll(ctx, alias):
	info('roll command called')
	
@logger.catch
@bot.event
async def on_guild_join(g):
	info(f'Bot has joined guild: {g.name}(id: {g.id})')
	
@logger.catch
@bot.event
async def on_guild_remove(g):
	info(f'Bot has left guild: {g.name}(id: {g.id})')
	if guildHasAliases(g):
		del aliases[g.id]
		stateWrite()
		info('aliases removed')
	else:
		info('No aliases from the leaving guild to remove')

init()

info("Running bot! Beep Boop!")
		
try:
	bot.run(TOKEN)
except Exception as e:
	logger.exception(e)

