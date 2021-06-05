from os import environ
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
			n = Game(message.channel, players[message.author], message.author)
			players[message.author].game = n
			await n.release(players[message.author].world, players[message.author].level) #player level
			return

		if inp[0] == ".place" or inp[0] == ".p":
			for i in range(1, len(inp)):
				if len(inp[i]) > 2 and inp[i][1] == "-":
					await players[message.author].game.place(int(inp[i][0]), inp[i][2:])
			return

		if inp[0] == ".remove" or inp[0] == ".r":
			await players[message.author].game.remove(int(inp[1]))
			return

		if inp[0] == ".check" or inp[0] == ".c":
			if players[message.author].game != -1:
				await players[message.author].game.check(1)
				return 
			await message.channel.send("No current game found.")

		if inp[0] == ".l":
			players[message.author].level = int(inp[1])
			await message.channel.send("Level set to " + str(inp[1]))
			return 




client = MyClient()
client.run(environ["BOT_TOKEN"])
	

