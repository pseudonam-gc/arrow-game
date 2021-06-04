from operator import xor
import random
import copy

class Space():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.level = -1
        self.value = value
        self.star_value = 0
    def add_star_value(self, x):
        self.star_value += x

class Grid():
    # 7x7 grid
    # Items are strings in the list identified with a character and a direction (UDLR). 
    # Capital = preplaced. Lowercase = player-placed
    # 0 = Uninitialized 
    # P = Player
    # A = Arrow
    # B = Bold Arrow
    # XX = Wall
    # * = Star (appears twice)

    def __init__(self):
        self.tempgrid = -1
        self.perp = 1 # 1 or 0
        self.inventory = []
    def printGrid(self): 
        for i in self.grid:
            print (" ".join([y.value for y in [x for x in i]]))
        print ("")

    def generateGrid(self, level, l, w, arrow_count, star_count, unnec_arrows, walls, tilts): # g is the grid being filled
        self.level = level
        self.l = l 
        self.w = w
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
        prev_dir = ""
        prev_movement = -1 # -1 = n/a, 0 = hor, 1 = ver


        # TILTS
        tilt_list = []
        for i in range(arrow_count):
            tilt_list.append(0)
        for i in range(tilts):  
            s = random.randint(0, len(tilt_list)-1)
            while tilt_list[s] != 0:
                s = random.randint(0, len(tilt_list)-1)
            tilt_list[s] = 1

        """
        arrow_spaces = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j].value == "A":
                    arrow_spaces.append((i, j))
        for i in range(tilts):
            s = random.randint(0, len(arrow_spaces)-1)
            sx = arrow_spaces[s].x
            sy = arrow_spaces[s].y
            self.grid[sy][sx].value = "T"
            """

        while t < arrow_count:

            # Fills candidate_spaces
            candidate_spaces = []
            if self.perp != 1:
                for i in space_list:
                    if xor(i.x == prev_x, i.y == prev_y):
                        candidate_spaces.append(i)
            else:
                if prev_movement == -1:
                    for i in space_list:
                        if xor(i.x == prev_x, i.y == prev_y):
                            candidate_spaces.append(i)
                elif prev_movement == 0:
                    for i in space_list:
                        if i.y == prev_y:
                            candidate_spaces.append(i)
                elif prev_movement == 1:
                    for i in space_list:
                        if i.x == prev_x:
                            candidate_spaces.append(i)
            if len(candidate_spaces) == 0:
                break

            seed = random.randint(0, len(candidate_spaces)-1)
            space = candidate_spaces[seed]

            if self.perp == 1:
                if space.x == prev_x:
                    prev_movement = 0
                else:
                    prev_movement = 1


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
                if tilt_list[t] == 0:
                    if prev_x < space.x:
                        self.grid[prev_y][prev_x].value = "AR"
                        prev_dir = "R"
                    elif prev_x > space.x:
                        self.grid[prev_y][prev_x].value = "AL"
                        prev_dir = "L"
                    elif prev_y < space.y:
                        self.grid[prev_y][prev_x].value = "AD"
                        prev_dir = "D"
                    else:
                        self.grid[prev_y][prev_x].value = "AU"
                        prev_dir = "U"
                else:
                    if prev_x < space.x:
                        if prev_dir == "U":
                            self.grid[prev_y][prev_x].value = 'TC'
                        elif prev_dir == "D":
                            self.grid[prev_y][prev_x].value = 'TA'
                        else:
                            self.grid[prev_y][prev_x].value = "AR"

                    elif prev_x > space.x:
                        if prev_dir == "U":
                            self.grid[prev_y][prev_x].value = 'TA'
                        elif prev_dir == "D":
                            self.grid[prev_y][prev_x].value = 'TC'
                        else:
                            self.grid[prev_y][prev_x].value = "AL"
                    elif prev_y < space.y:
                        if prev_dir == "L":
                            self.grid[prev_y][prev_x].value = 'TA'
                        elif prev_dir == "R":
                            self.grid[prev_y][prev_x].value = 'TC'
                        else:
                            self.grid[prev_y][prev_x].value = "AD"
                    else:
                        if prev_dir == "L":
                            self.grid[prev_y][prev_x].value = 'TC'
                        elif prev_dir == "R":
                            self.grid[prev_y][prev_x].value = 'TA'
                        else:
                            self.grid[prev_y][prev_x].value = "AU"
                    # TODO: Copy this over to the final arrow placement
            else:
                if prev_x < space.x:
                    self.grid[prev_y][prev_x].value = "PR"
                    prev_dir = "R"
                elif prev_x > space.x:
                    self.grid[prev_y][prev_x].value = "PL"
                    prev_dir = "L"
                elif prev_y < space.y:
                    self.grid[prev_y][prev_x].value = "PD"
                    prev_dir = "D"
                else:
                    self.grid[prev_y][prev_x].value = "PU"
                    prev_dir = "U"

            # Sets previous space to current space

            prev_x = space.x 
            prev_y = space.y
            t += 1 

        # Fix final space
        candidate_spaces = []
        if self.perp != 1:
            for i in space_list:
                if xor(i.x == prev_x, i.y == prev_y):
                    candidate_spaces.append(i)
        else:
            if prev_movement == -1:
                for i in space_list:
                    if xor(i.x == prev_x, i.y == prev_y):
                        candidate_spaces.append(i)
            elif prev_movement == 0:
                for i in space_list:
                    if i.y == prev_y:
                        candidate_spaces.append(i)
            elif prev_movement == 1:
                for i in space_list:
                    if i.x == prev_x:
                        candidate_spaces.append(i)
        if len(candidate_spaces) == 0:
            self.generateGrid(l, w, arrow_count, star_count, unnec_arrows, walls, tilts)
            return
        seed = random.randint(0, len(candidate_spaces)-1)
        space = candidate_spaces[seed]

        if prev_x < space.x:
            self.grid[prev_y][prev_x].value = "AR"
            # append everything to the right of this
            for i in space_list:
                if i.x > space.x and i.y == space.y:
                    star_spaces.append(i)
        elif prev_x > space.x:
            self.grid[prev_y][prev_x].value = "AL"
            for i in space_list:
                if i.x < space.x and i.y == space.y:
                    star_spaces.append(i)
        elif prev_y < space.y:
            self.grid[prev_y][prev_x].value = "AD"
            for i in space_list:
                if i.y > space.y and i.x == space.x:
                    star_spaces.append(i)
        else:
            self.grid[prev_y][prev_x].value = "AU"
            for i in space_list:
                if i.y < space.y and i.x == space.x:
                    star_spaces.append(i)
        self.open_squares = space_list

        # Clear duplicates
        star_spaces = list(set(star_spaces))

        if len(star_spaces) >= 5:
            for i in range(5):
                min_star_count = star_spaces[0].star_value
                for j in range(len(star_spaces)):
                    if star_spaces[j].star_value < min_star_count:
                        min_star_count = star_spaces[j].star_value
                min_star_spaces = []
                for j in range(len(star_spaces)):
                    if star_spaces[j].star_value == min_star_count:
                        min_star_spaces.append(star_spaces[j])
                s = random.randint(0, len(min_star_spaces)-1)
                min_star_spaces[s].value = "**"
                
                for j in range(len(star_spaces)):
                    # Every star space with same row/col gets +1
                    if star_spaces[j].x == min_star_spaces[s].x:
                        star_spaces[j].add_star_value(1)
                        if abs(star_spaces[j].y-min_star_spaces[s].y)<=1:
                            star_spaces[j].add_star_value(1)
                    if star_spaces[j].y == min_star_spaces[s].y:
                        star_spaces[j].add_star_value(1)
                        if abs(star_spaces[j].x-min_star_spaces[s].x)<=1:
                            star_spaces[j].add_star_value(1)
                    if star_spaces[j] == min_star_spaces[s]:
                        star_spaces[j].add_star_value(100000)
                    # Every adjacent star space gets +1
            decoy_star_spaces = []
            for i in range(len(space_list)):
                    # Find empty space not in 
                if space_list[i] not in star_spaces and space_list[i].value == "00":
                    decoy_star_spaces.append(space_list[i])
            if len(decoy_star_spaces) >= star_count-5:           
                for i in range(star_count-5):
                    ind = random.randint(0, len(decoy_star_spaces)-1)
                    decoy_star_spaces[ind].value = "**"
                    decoy_star_spaces.pop(ind)


            else:
                self.generateGrid(level, l, w, arrow_count, star_count, unnec_arrows, walls, tilts) 
                return
        else:
            self.generateGrid(level, l, w, arrow_count, star_count, unnec_arrows, walls, tilts)
            return

        # DECOY ARROWS
        for i in range(unnec_arrows):
            if len(self.open_squares) == 0:
                break
            s = random.randint(0, len(self.open_squares)-1)
            d = ["R", "U", "D", "L"]
            sx = self.open_squares[s].x
            sy = self.open_squares[s].y
            self.grid[sy][sx].value = "A"+d[random.randint(0, 3)]
            self.open_squares.pop(s)

        # WALLS
        for i in range(walls):
            if len(self.open_squares) == 0:
                break
            s = random.randint(0, len(self.open_squares)-1)
            sx = self.open_squares[s].x
            sy = self.open_squares[s].y
            self.grid[sy][sx].value = "XX"
            self.open_squares.pop(s)
        

    def generateTempGrid(self, removed_arrows):
        arrow_spaces = []
        self.tempgrid = []

        for i in range(len(self.grid)):
            self.tempgrid.append([])
            for j in range(len(self.grid[i])):
                self.tempgrid[i].append(self.grid[i][j].value)
                if self.tempgrid[i][j][0] == "A":
                    arrow_spaces.append((i, j))
        # TODO: ENSURE LEN() >= REMOVED_ARROWS OR RESTART THE WHOLE PROCESS        

        if self.level == 9:
            for i in range(len(arrow_spaces)):
                sy = arrow_spaces[i][0]
                sx = arrow_spaces[i][1]
                if self.tempgrid[sy][sx] in ["AU", "AD"]:
                    self.inventory.append(self.tempgrid[sy][sx][0].lower()+self.tempgrid[sy][sx][1])
                    self.tempgrid[sy][sx] = "00"
            return

        for i in range(removed_arrows):
            s = random.randint(0, len(arrow_spaces)-1)
            sy = arrow_spaces[s][0]
            sx = arrow_spaces[s][1]
            print (i, sx, sy)
            self.inventory.append(self.tempgrid[sy][sx][0].lower()+self.tempgrid[sy][sx][1])
            self.tempgrid[sy][sx] = "00"
            arrow_spaces.pop(s)


            
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