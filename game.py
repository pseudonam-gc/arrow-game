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
        self.submission = {} # key-value pairs are ID-Space. 
        # Set everything in submission to -1.
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
                arrow_count = 5
                star_count = 5
                unnec_arrows = 1
                removed_arrows = 1
            if level == 4:
                l = 7
                w = 7
                arrow_count = 6
                star_count = 5
                removed_arrows = 3
            if level == 5:
                l = 7
                w = 7
                arrow_count = 5
                star_count = 5
                removed_arrows = 5

        self.grid = Grid()
        self.grid.generateGrid(l, w, arrow_count, star_count, unnec_arrows)

        self.grid.generateTempGrid(removed_arrows)
        for i in range(len(self.grid.inventory)):
            self.submission[i] = -1
        await self.check()

    async def check(self, laser=0): # laser is boolean

        l = self.grid.l 
        w = self.grid.w

        im = Image.new("RGB", (300+(200)+100*l, 300+100*w), (128, 128, 128))
        draw = ImageDraw.Draw(im)

        # Background

        draw.rectangle((0, 0, im.width, im.height), fill=(255, 255, 255))
        font = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 72)
        # Horizontal Lines
        for i in range(w+1):
            draw.line((150, 150+i*100, 150+l*100, 150+i*100), fill=(0, 0, 0), width=8)
        for i in range(l+1):
            draw.line((150+i*100, 150, 150+i*100, 150+w*100), fill=(0, 0, 0), width=8)

        # Horizontal Letters
        for i in range(w):
            draw.text((200+i*100, 100), chr(65+i), font=font, fill=(0,0,0), anchor="mm")
        for i in range(w):
            draw.text((200+i*100, 200+w*100), chr(65+i), font=font, fill=(0,0,0), anchor="mm")

        # Vertical Numbers
        for i in range(w):
            draw.text((100, 200+i*100), str(i+1), font=font, fill=(0,0,0), anchor="mm")
        for i in range(w):
            draw.text((200+w*100, 200+i*100), str(i+1), font=font, fill=(0,0,0), anchor="mm")
        # Draw tempGrid

        for i in range(l):
            for j in range(w):
                v = self.grid.tempgrid[j][i]
                if v == "00":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(255, 255, 255))
                elif v[0] == "P":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(200, 200, 200))
                    drawPlayer(draw, 200+i*100, 200+j*100, v[1])
                    player_loc = [i, j]
                    player_dir = v[1]
                elif v[0] == "A":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(200, 200, 200))
                    drawArrow(draw, 200+i*100, 200+j*100, v[1])
                elif v[0] == "a":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(0, 255, 0))
                    drawArrow(draw, 200+i*100, 200+j*100, v[1])
                elif v[0] == "*":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(255, 255, 0))

        # Draw inventory lines
        for i in range(len(self.grid.inventory)+1):
            draw.line((250+l*100, 150+i*100, 350+l*100, 150+i*100), fill=(0, 0, 0), width=8)
        draw.line((350+l*100, 150, 350+l*100, 150+len(self.grid.inventory)*100), fill=(0, 0, 0), width=8)
        draw.line((250+l*100, 150, 250+l*100, 150+len(self.grid.inventory)*100), fill=(0, 0, 0), width=8)

        # Draw inventory

        for i in range(len(self.grid.inventory)):
            if self.submission[i] == -1:
                draw.rectangle((254+l*100, 154+i*100, 346+l*100, 246+i*100), fill=(255, 255, 255))
            else:
                draw.rectangle((254+l*100, 154+i*100, 346+l*100, 246+i*100), fill=(0, 255, 0))
            if self.grid.inventory[i][0] == "a":
                drawArrow(draw, 300+l*100, 200+i*100, self.grid.inventory[i][1])


        #draw.rectangle((100, 100, 200, 200), fill=(0, 255, 0))
        #draw.ellipse((250, 300, 450, 400), fill=(0, 0, 255))

        # Draw laser

        if laser == 1:
            # find the initial starting location / direction
            visited_array = []
            while 0 <= player_loc[0] <= l-1 and 0 <= player_loc[1] <= w-1:
                if [player_loc[0], player_loc[1]] not in visited_array:
                    if self.grid.tempgrid[player_loc[1]][player_loc[0]][0].upper() in ["A", "B"]:
                        player_dir = self.grid.tempgrid[player_loc[1]][player_loc[0]][1]
                visited_array.append(player_loc.copy())
                # move to next location
                if player_dir == "U":
                    player_loc[1] -= 1
                elif player_dir == "D":
                    player_loc[1] += 1
                elif player_dir == "R":
                    player_loc[0] += 1
                elif player_dir == "L":
                    player_loc[0] -= 1
            for i in range(len(visited_array)-1):
                p1 = visited_array[i]
                p2 = visited_array[i+1]
                draw.line((200+100*p1[0], 200+100*p1[1], 200+100*p2[0], 200+100*p2[1]), fill=(255,0,0), width=10)
            p = visited_array[len(visited_array)-1]
            draw.line((175+100*p[0], 175+100*p[1], 225+100*p[0], 225+100*p[1]), fill=(255,0,0), width=10)
            draw.line((225+100*p[0], 175+100*p[1], 175+100*p[0], 225+100*p[1]), fill=(255,0,0), width=10)



        im.save('test.png', quality=95)
        await self.channel.send(file=discord.File("test.png"))
        """
        await self.channel.send(file=discord.File("test.png"))

        for i in range(l):
            for j in range(w):
                v = self.grid.grid[j][i].value
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
        await self.channel.send(file=discord.File("SPOILER_test.png"))"""

    async def place(self, piece_id, space):
        # TODO: Ensure id is an integer

        if piece_id > len(self.grid.inventory) or piece_id < 0:
            return
        if len(space) == 2 and not space[0].isnumeric() and space[1].isnumeric():
            xind = ord(space[0].upper())-64-1
            yind = int(space[1])-1
            # self.submission is 0-indexed
            if self.submission[piece_id-1] != -1:
                n = self.submission[piece_id-1]
                self.grid.tempgrid[n[1]][n[0]] = "00"
            if self.grid.tempgrid[yind][xind] == "00":
                space_value = self.grid.inventory[piece_id-1]
                self.grid.tempgrid[yind][xind] = space_value
                self.submission[piece_id-1] = (xind, yind)
            elif self.grid.tempgrid[yind][xind].islower():
                # TODO: Case for this
                pass

            # TODO: Inform players of fail
    
    async def remove(self, piece_id):
        if self.submission[piece_id-1] != -1:
            n = self.submission[piece_id-1]
            self.grid.tempgrid[n[1]][n[0]] = "00"
            self.submission[piece_id-1] = -1
        # TODO: inform players of fail

