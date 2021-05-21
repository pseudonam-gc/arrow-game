import discord
from PIL import Image, ImageDraw, ImageFont
from grid import Space
from grid import Grid
from player import Player
import random
import copy
import math

# TODO: Parse out image inputs

def drawPlayer(draw, x, y, dir):
	draw.ellipse((x-40, y-40, x+40, y+40), fill=(0, 255, 0))
	drawArrow(draw, x, y, dir, size=0.7)
		
def drawArrow(draw, x, y, dir, size=1): # x and y are centered spaces
	if dir == "U":
		draw.line((x, y+30*size, x, y-30*size), fill=(0, 0, 0), width=5)
		draw.line((x-15*size, y-10*size, x, y-30*size), fill=(0, 0, 0), width=4)
		draw.line((x+15*size, y-10*size, x, y-30*size), fill=(0, 0, 0), width=4)
	elif dir == "D":
		draw.line((x, y-30*size, x, y+30*size), fill=(0, 0, 0), width=5)
		draw.line((x-15*size, y+10*size, x, y+30*size), fill=(0, 0, 0), width=4)
		draw.line((x+15*size, y+10*size, x, y+30*size), fill=(0, 0, 0), width=4)
	elif dir == "R":
		draw.line((x-30*size, y, x+30*size, y), fill=(0, 0, 0), width=5)
		draw.line((x+10*size, y-15*size, x+30*size, y), fill=(0, 0, 0), width=4)
		draw.line((x+10*size, y+15*size, x+30*size, y), fill=(0, 0, 0), width=4)
	elif dir == "L":
		draw.line((x+30*size, y, x-30*size, y), fill=(0, 0, 0), width=5)
		draw.line((x-10*size, y-15*size, x-30*size, y), fill=(0, 0, 0), width=4)
		draw.line((x-10*size, y+15*size, x-30*size, y), fill=(0, 0, 0), width=4)

class Game():
    def __init__(self, channel, dID):
        # create grid
        self.grid = Grid()
        self.channel = channel
        #self.timer = -1
        self.dID = dID
    async def begin(self):
        #self.timer = 90
        pass

    async def release(self, world, level):
        l = 8
        w = 8
        arrow_count = 0
        star_count = 7
        unnec_arrows = 0
        removed_arrows = 0  
        if world == 1:
            if level == 1:
                l = 5
                w = 5
                arrow_count = 2
                star_count = 5
                removed_arrows = 2
            if level == 2:
                l = 6
                w = 6
                arrow_count = 4
                star_count = 5
                removed_arrows = 2
            if level == 3:
                l = 7
                w = 7
                arrow_count = 6
                star_count = 5
                unnec_arrows = 1
                removed_arrows = 1

        im = Image.new("RGB", (300+100*l, 300+100*w), (128, 128, 128))
        draw = ImageDraw.Draw(im)

        # Background

        draw.rectangle((0, 0, im.width, im.height), fill=(255, 255, 255))
        font = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 72)
        # Horizontal Lines
        for i in range(w+1):
            draw.line((150, 150+i*100, 150+l*100, 150+i*100), fill=(0, 0, 0), width=8)
        for i in range(l+1):
            draw.line((150+i*100, 150, 150+i*100, 150+w*100), fill=(0, 0, 0), width=8)

        a = Grid()
        a.generateGrid(l, w, arrow_count, star_count)

        a.generateTempGrid(removed_arrows, unnec_arrows)
        for i in range(l):
            for j in range(w):
                v = a.tempgrid[j][i]
                if v == "00":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(255, 255, 255))
                elif v[0] == "P":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(200, 200, 200))
                    drawPlayer(draw, 200+i*100, 200+j*100, v[1])
                elif v[0] == "A":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(200, 200, 200))
                    drawArrow(draw, 200+i*100, 200+j*100, v[1])
                    paint_color = (200, 200, 200)
                elif v[0] == "*":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(255, 255, 0))
                    paint_color = (255, 255, 255)

        #draw.rectangle((100, 100, 200, 200), fill=(0, 255, 0))
        #draw.ellipse((250, 300, 450, 400), fill=(0, 0, 255))
        im.save('test.png', quality=95)
        await self.channel.send(file=discord.File("test.png"))



        for i in range(l):
            for j in range(w):
                v = a.grid[j][i].value
                if v == "00":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(255, 255, 255))
                elif v[0] == "P":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(200, 200, 200))
                    drawPlayer(draw, 200+i*100, 200+j*100, v[1])
                elif v[0] == "A":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(200, 200, 200))
                    drawArrow(draw, 200+i*100, 200+j*100, v[1])
                    paint_color = (200, 200, 200)
                elif v[0] == "*":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(255, 255, 0))
                    paint_color = (255, 255, 255)

        #draw.rectangle((100, 100, 200, 200), fill=(0, 255, 0))
        #draw.ellipse((250, 300, 450, 400), fill=(0, 0, 255))
        im.save('SPOILER_test.png', quality=95)
        await self.channel.send(file=discord.File("SPOILER_test.png"))