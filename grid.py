from operator import xor
import random
import copy

class Space():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

class Grid():
    # 7x7 grid
    # Items are strings in the list identified with a character and a direction (UDLR). 
    # Capital = preplaced. Lowercase = player-placed
    # 0 = Uninitialized 
    # P = Player
    # A = Arrow
    # B = Bold Arrow
    # * = Star (appears twice)

    def __init__(self):
        self.tempgrid = -1
    def printGrid(self): 
        for i in self.grid:
            print (" ".join([y.value for y in [x for x in i]]))
        print ("")

    def generateGrid(self, l, w, arrow_count, star_count): # g is the grid being filled
        self.grid = []
        for i in range(w):
            self.grid.append([])
            for j in range(l):
                self.grid[i].append(Space(j, i, "00"))
        space_list = [] # List of Space objects in the grid
        for i in self.grid:
            for j in i:
                space_list.append(j)
        # Assign the player's position
        py = random.randint(0,w-1)
        px = random.randint(0,l-1)
        self.grid[py][px].value = "PP"

        prev_x = px
        prev_y = py
        prev_space = self.grid[py][px]
        candidate_spaces = []
        star_spaces = []
        t = 0 

        while t < arrow_count:

            # Fills candidate_spaces
            candidate_spaces = []
            for i in space_list:
                if xor(i.x == prev_x, i.y == prev_y):
                    candidate_spaces.append(i)
            if len(candidate_spaces) == 0:
                break

            seed = random.randint(0, len(candidate_spaces)-1)
            space = candidate_spaces[seed]

            if space.x == prev_x:
                hor = 0
            else:
                hor = 1

            candidate_spaces[seed].value = str(t)

            # Updates direction of previous space

            # Clear all spaces in between and start/ending space for obv reasons
            
            k = 0
            if hor == 1:
                while k < len(space_list):
                    if (space_list[k].y == space.y) and (space_list[k].x in range(min(space.x, prev_x), max(space.x, prev_x)+1)):
                        if not ((space_list[k].x == prev_x and space_list[k].y == prev_y) or (space_list[k].x == space.x and space_list[k].y == space.y)):
                            star_spaces.append(space_list[k])
                        space_list.pop(k) 
                    else:
                        k += 1
            else:
                while k < len(space_list):
                    if (space_list[k].x == space.x) and (space_list[k].y in range(min(space.y, prev_y), max(space.y, prev_y)+1)):
                        if not ((space_list[k].x == prev_x and space_list[k].y == prev_y) or (space_list[k].x == space.x and space_list[k].y == space.y)):
                            star_spaces.append(space_list[k])
                        space_list.pop(k) 
                    else:
                        k += 1

            # Arrows, folks!
            if t != 0:
                if prev_x < space.x:
                    self.grid[prev_y][prev_x].value = "AR"
                elif prev_x > space.x:
                    self.grid[prev_y][prev_x].value = "AL"
                elif prev_y < space.y:
                    self.grid[prev_y][prev_x].value = "AD"
                else:
                    self.grid[prev_y][prev_x].value = "AU"
            else:
                if prev_x < space.x:
                    self.grid[prev_y][prev_x].value = "PR"
                elif prev_x > space.x:
                    self.grid[prev_y][prev_x].value = "PL"
                elif prev_y < space.y:
                    self.grid[prev_y][prev_x].value = "PD"
                else:
                    self.grid[prev_y][prev_x].value = "PU"


            # Sets previous space to current space

            prev_x = space.x 
            prev_y = space.y
            t += 1 
        # TODO: Hide part of the grid.

        # Fix final space

        if prev_x < space.x:
            self.grid[prev_y][prev_x].value = "AR"
        elif prev_x > space.x:
            self.grid[prev_y][prev_x].value = "AL"
        elif prev_y < space.y:
            self.grid[prev_y][prev_x].value = "AD"
        else:
            self.grid[prev_y][prev_x].value = "AU"
            

        # TODO: ENSURE LEN(STAR_SPACES) >= 5 OR RESTART THE WHOLE PROCESS
        # TODO: SPAWN GOLD ON DIFFERENT ROWS/COLUMNS IF POSSIBLE
        if len(star_spaces) >= 5:
            for i in range(star_count):
                s = random.randint(0, len(star_spaces)-1)
                star_spaces[s].value = "**"
                star_spaces.pop(s)
        else:
            self.generateGrid(l, w, arrow_count, star_count)
        
    def generateTempGrid(self):
        arrow_spaces = []
        self.tempgrid = []
        for i in range(len(self.grid)):
            self.tempgrid.append([])
            for j in range(len(self.grid[i])):
                self.tempgrid[i].append(self.grid[i][j].value)
                if self.tempgrid[i][j][0] == "A":
                    arrow_spaces.append((i, j))
        # TODO: ENSURE LEN(STAR_SPACES) >= 3 OR RESTART THE WHOLE PROCESS        

        for i in range(3):
            s = random.randint(0, len(arrow_spaces)-1)
            sy = arrow_spaces[s][0]
            sx = arrow_spaces[s][1]
            self.tempgrid[sy][sx] = "00"
            arrow_spaces.pop(s)

        # TODO: DECOY ARROWS?


            
def validDirections(y, x):
    dir_list = ["U", "D", "L", "R"]
    if x == 0:
        dir_list.remove("L")
    if x == 6:
        dir_list.remove("R")
    if y == 0:
        dir_list.remove("U")
    if y == 6:
        dir_list.remove("D")
    return dir_list


#n = Grid()
#generateGrid(n)
#printGrid(n)