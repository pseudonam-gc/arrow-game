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

def drawTilt(draw, x, y, dir):
    if dir == "C":
        dir = "A"
    else:
        dir = "C"
    # LOL
    if dir == "C":
        draw.arc((x-35, y-35, x+35, y+35), -110, 0, fill=(0, 0, 255), width=8)
        draw.arc((x-35, y-35, x+35, y+35), -290, -180, fill=(0, 0, 255), width=8)
    elif dir == "A":
        draw.arc((x-35, y-35, x+35, y+35), 180, 290, fill=(255, 165, 0), width=8)
        draw.arc((x-35, y-35, x+35, y+35), 0, 110, fill=(255, 165, 0), width=8)
    draw.ellipse((x-28, y-28, x+28, y+28), fill=(200,200,200))
    if dir == "C":
        draw.line((x+15, y+30, x-15, y+45), fill=(0, 0, 255), width=4)
        draw.line((x+15, y+30, x-15, y+5), fill=(0, 0, 255), width=4)

        draw.line((x-15, y-30, x+15, y-45), fill=(0, 0, 255), width=4)
        draw.line((x-15, y-30, x+15, y-5), fill=(0, 0, 255), width=4)
    elif dir == "A":
        draw.line((x-15, y+30, x+15, y+45), fill=(255, 165, 0), width=4)
        draw.line((x-15, y+30, x+15, y+5), fill=(255, 165, 0), width=4)

        draw.line((x+15, y-30, x-15, y-45), fill=(255, 165, 0), width=4)
        draw.line((x+15, y-30, x-15, y-5), fill=(255, 165, 0), width=4)

class Game():
    def __init__(self, channel, player, dID):
        # create grid
        self.grid = Grid()
        self.channel = channel
        self.player = player
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
        walls = 0
        second_walls = 0
        tilts = 0
        if world == 1:
            # Opening level - introduce the players to the arrow placing mechanic
            if level == 1:
                l = 5
                w = 5
                arrow_count = 2
                star_count = 5
                removed_arrows = 2
            # Introduce players to pre-placed grid, also nontrivial
            if level == 2:
                l = 6
                w = 6
                arrow_count = 4
                star_count = 5
                removed_arrows = 2
            # Show that every arrow doesn't have to be touched. Also back arrows
            if level == 3:
                l = 7
                w = 7
                arrow_count = 5
                star_count = 5
                unnec_arrows = 2
                removed_arrows = 1
            # Enough introductions, raise the difficulty a bit
            if level == 4:
                l = 7
                w = 7
                arrow_count = 7
                unnec_arrows = 2
                star_count = 5
                removed_arrows = 3
            # Players can place wherever they want. Gimmick level
            if level == 5:
                l = 7
                w = 7
                arrow_count = 6
                star_count = 6
                removed_arrows = 6
            # Introduces walls. Still nontrivial
            if level == 6:
                l = 7
                w = 7
                arrow_count = 5
                star_count = 6
                unnec_arrows = 3
                walls = 3
                removed_arrows = 2
            # Reinforces back arrows, also quite hard 
            if level == 7:
                l = 7
                w = 7
                arrow_count = 7
                star_count = 6
                unnec_arrows = 3
                walls = 7
                removed_arrows = 2
            # Wall spam, just for the heck of it. Lots of arrows but quite ez
            if level == 8:
                l = 7
                w = 7
                arrow_count = 10
                star_count = 6
                walls = 21
                unnec_arrows = 2
                removed_arrows = 3
            # Gimmick level! All the horizontal arrows are placed, verticals aren't.
            if level == 9:
                l = 7
                w = 7
                arrow_count = 12
                star_count = 6
                removed_arrows = -1
            # Introduces tilts 
            if level == 10:
                l = 7
                w = 7
                arrow_count = 5
                tilts = 2
                star_count = 5
                removed_arrows = 2
            # Somewhat difficult tilt level
            if level == 11:
                l = 7
                w = 7
                arrow_count = 8
                tilts = 4
                walls = 3
                unnec_arrows = 3
                star_count = 6
                removed_arrows = 2
            # Very difficult tilt level, back arrows too
            if level == 12:
                l = 7
                w = 7
                arrow_count = 10
                tilts = 7
                walls = 5
                star_count = 5
                removed_arrows = 2
            # Introduce second walls. Back arrows, for obvious reasons. 
            if level == 13:
                l = 7
                w = 7
                arrow_count = 6
                star_count = 5
                removed_arrows = 4
                second_walls = 10
        # NOTE: ARROWS must be greater than or equal to tilts, removed_arrows
        self.grid = Grid()
        self.grid.generateGrid(level, l, w, arrow_count, star_count, unnec_arrows, walls, second_walls, tilts)

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
                elif v[0] == "X":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(100, 100, 100))
                    draw.line((165+i*100, 165+j*100, 235+i*100, 235+j*100), fill=(255, 255, 255), width=6)
                    draw.line((235+i*100, 165+j*100, 165+i*100, 235+j*100), fill=(255, 255, 255), width=6)
                elif v[0] == "Y":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(200, 200, 200))
                    draw.line((165+i*100, 165+j*100, 235+i*100, 235+j*100), fill=(255, 255, 255), width=6)
                    draw.line((235+i*100, 165+j*100, 165+i*100, 235+j*100), fill=(255, 255, 255), width=6)
                elif v[0] == "T":
                    draw.rectangle((154+i*100, 154+j*100, 246+i*100, 246+j*100), fill=(200, 200, 200))
                    drawTilt(draw, 200+i*100, 200+j*100, v[1])

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
            leave = 0
            visited_array = []
            second_wall_array = []
            while 0 <= player_loc[0] <= l-1 and 0 <= player_loc[1] <= w-1:
                if self.grid.grid[player_loc[1]][player_loc[0]].value[0] == "X":
                    leave = 1
                if self.grid.grid[player_loc[1]][player_loc[0]].value[0] == "Y":
                    if [player_loc[0], player_loc[1]] in second_wall_array:
                        leave = 1
                    else:
                        second_wall_array.append([player_loc[0], player_loc[1]])
                if [player_loc[0], player_loc[1]] not in visited_array:
                    if self.grid.tempgrid[player_loc[1]][player_loc[0]][0].upper() in ["A", "B"]:
                        player_dir = self.grid.tempgrid[player_loc[1]][player_loc[0]][1]
                    if self.grid.tempgrid[player_loc[1]][player_loc[0]].upper() == "TC":
                        # CLOCKWISE TURN
                        if player_dir == "U":
                            player_dir = "R"
                        elif player_dir == "R":
                            player_dir = "D"
                        elif player_dir == "D":
                            player_dir = "L"
                        elif player_dir == "L":
                            player_dir = "U"
                    if self.grid.tempgrid[player_loc[1]][player_loc[0]].upper() == "TA":
                        # CLOCKWISE TURN
                        if player_dir == "U":
                            player_dir = "L"
                        elif player_dir == "L":
                            player_dir = "D"
                        elif player_dir == "D":
                            player_dir = "R"
                        elif player_dir == "R":
                            player_dir = "U"
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
                if leave == 1:
                    break
            for i in range(len(visited_array)-1):
                p1 = visited_array[i]
                p2 = visited_array[i+1]
                draw.line((200+100*p1[0], 200+100*p1[1], 200+100*p2[0], 200+100*p2[1]), fill=(255,0,0), width=10)
            p = visited_array[len(visited_array)-1]
            draw.line((175+100*p[0], 175+100*p[1], 225+100*p[0], 225+100*p[1]), fill=(255,0,0), width=10)
            draw.line((225+100*p[0], 175+100*p[1], 175+100*p[0], 225+100*p[1]), fill=(255,0,0), width=10)            

        im.save('test.png', quality=95)

        if laser == 1: 
            c = 0
            star_space_array = [] # ensures the same star doesn't count twice
            for i in range(len(visited_array)):
                if [[visited_array[i][0]], [visited_array[i][1]]] not in star_space_array:
                    if self.grid.tempgrid[visited_array[i][1]][visited_array[i][0]] == "**":
                        c += 1
                        star_space_array.append([[visited_array[i][0]], [visited_array[i][1]]])
            if c >= 5:
                # Success
                self.player.level += 1
                await self.channel.send("Success! You have advanced to World " + str(self.player.world) + "." + str(self.player.level), file=discord.File("test.png"))
            else:
                await self.channel.send(file=discord.File("test.png"))


        else: 
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
            if self.grid.tempgrid[yind][xind] == "00":
                if self.submission[piece_id-1] != -1:
                    n = self.submission[piece_id-1]
                    self.grid.tempgrid[n[1]][n[0]] = "00"
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

