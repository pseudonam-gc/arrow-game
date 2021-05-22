import discord
from PIL import Image, ImageDraw, ImageFont
from grid import Space
from grid import Grid
from game import Game
from player import Player
import random
import copy
import math

players = {}

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

		inp = message.content.split()

		if inp[0] == ".start":
			p = Player(message.author)
			players[message.author]=p
			await message.channel.send("Initialized account " + str(message.author) + ". Type \".adv\" to begin!")
			return
		elif not (message.author in players):
			await message.channel.send("Please initialize your account with .start.")
			return 

		if inp[0] == ".adv" or inp[0] == ".a":
			n = Game(message.channel, message.author)
			await n.release(players[message.author].world, players[message.author].level) #player level
			return

		if inp[0] == ".submit" or inp[0] == ".s":
			pass

		if inp[0] == ".l":
			players[message.author].level = int(inp[1])




client = MyClient()
client.run('ODEyNDQ4OTk2NzE4MDE4NTYw.YDA6Fw.LAws-I70C_7i9cP8EzQVNW_dmKg')
	

