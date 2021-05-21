import discord
from PIL import Image, ImageDraw, ImageFont
from grid import Space
from grid import Grid
from game import Game
from player import Player
import random
import copy
import math

players = []

class MyClient(discord.Client):

	async def on_ready(self):
		# Load in players	
		
		print ('Logged on as', self.user)
		botLog = self.get_channel(821125824202670081)
		await botLog.send("SubmissionsBot is now online.")

	async def on_message(self, message):
		
		if message.author == self.user:
			return

		# Bot only reads messages with a "."

		if message.content[0] != ".":
			return
		if message.content == ".start":
			p = Player(message.author)
			players.append(p)
			await message.channel.send("Initialized account " + str(message.author) + ". Type \".adv\" to begin!")
			return
		elif message.author not in [x.dID for x in players]:
			await message.channel.send("Please initialize your account with .start.")
			return 

		if message.content == ".adv":
			n = Game(message.channel, message.author)
			await n.release(1) #player level
			return



client = MyClient()
client.run('ODEyNDQ4OTk2NzE4MDE4NTYw.YDA6Fw.LAws-I70C_7i9cP8EzQVNW_dmKg')
	

