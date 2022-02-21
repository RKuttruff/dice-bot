#Copyright (C) 2022  Riley Kuttruff
#
#	This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#	Public License for more details.
#
#	You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

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
	else:
		await ctx.send('Invalid use of !roll_dice command! Please follow the command with a list of numbers (integers) greater than 0.')

bot.run(TOKEN)
