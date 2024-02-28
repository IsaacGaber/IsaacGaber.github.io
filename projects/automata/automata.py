# Isaac John Gaber
import random, os
#--------------------------------------------------------
# pygame.init()
# font_size = 12
# font = pygame.font.Font("Courier_Prime\CourierPrime-Regular.ttf", font_size)
# sets file path for patterns
# print("This is In Fact")
random.seed()

# helper function
# sigmoid clamp used for smooth life
def sigmoidclamp(x,mi, mx):
    return mi + (mx-mi)*(lambda t: (1+200**(-t+0.5))**(-1) )( (x-mi)/(mx-mi) )
# used to load from pattern file on initialization
def pattern_from_file(path):
    file = open(path)
    pattern = []
    lines = file.readlines()
    for line in lines:
        pattern.append(str(line.strip()))
    file.close()
    return pattern

# class definitions
#--------------------------------------------------------
class Automata():
    """Class that holds the values of automata throughout the world"""
    def __init__(self, name, x, y, display_x, display_y, density):
        self.name = name
        self.x = x
        self.y = y
        self.start_density = density
        self.display_size = (display_x, display_y)
        # predefine common font character to save on rendering time
        # commonly used default characters
        self.chars = {
            "x": "<span>" + "x" + "</span>",
            "o": "<span>" + "o" + "</span>",
            ".": "<span>" + "." + "</span>",
            " ": "<span>" + " " + "</span>",
            "#": "<span>" + "#" + "</span>",
            "=": "<span>" + "=" + "</span>",
            "@": "<span>" + "@" + "</span>",
            "|": "<span>" + "|" + "</span>"
            }
        # checks for any patterns stored in file
        # patterns_2d = "patterns_2d.txt"
        # if os.path.exists(patterns_2d):
        #     self.state = [[0 for x in range(self.x)] for y in range(self.y)]
        #     # loads pattern into list
        #     new_pattern = pattern_from_file(patterns_2d)
        #     # sets pattern position in center of screen
        #     pattern_position = (self.x//2, self.y//2)
        #     # appends pattern to state
        #     self.add_pattern(new_pattern, pattern_position)
        # # else:
        #     self.state = [[random.random() < density for x in range(self.x)] for y in range(self.y)]

        self.state = [[random.random() < density for x in range(self.x)] for y in range(self.y)]

    def add_pattern(self, pattern, position):
        x_pos, y_pos = position
        y = 0
        for line in pattern:
            x = 0
            for char in line:
                # allows blank spaces or underscores for pattern
                if char == 'x':
                    self.state[y_pos + y][x_pos + x] = 1
                x += 1
            y += 1

    def step(self):
        raise NotImplementedError
    # translates value into pygame surface
    def format(self, cell):
        if cell == False:
            return self.chars['.']
        else:
            return self.chars['o']

    def check_neighbors(self, x, y):
        """returns number of neighbors turned on - in Moore neighborhood - wraps around"""
        neighbors = (
        (self.state[y][x-1] == 1) + (self.state[y][(x+1)%self.x] == 1)+
        (self.state[y-1][x] == 1) + (self.state[(y+1)%self.y][x] == 1)+
        (self.state[y-1][x-1] == 1) + (self.state[y-1][(x+1)%self.x] == 1)+
        (self.state[(y+1)%self.y][x-1] == 1) + (self.state[(y+1)%self.y][(x+1)%self.x] == 1)
        )
        return neighbors

    def check_neighbors_VN(self, x, y):
        """returns number of neighbors turned on - in Von Neumann neighborhood - wraps around"""
        neighbors = (
        (self.state[y][x-1] == 1) + (self.state[y][(x+1)%self.x] == 1)+
        (self.state[y-1][x] == 1) + (self.state[(y+1)%self.y][x] == 1)
        )
        return neighbors
    # translates the state of the world into array of pygame surfaces
    def render(self):
        to_render = []
        for y in range(self.y):
            for x in range(self.x):
                buffer = self.format(self.state[y][x])
                if buffer != None:
                    to_render.append(buffer)
        return to_render


#--------------------------------------------------------
class Life(Automata):
    """class for 'life' Cellular Automata"""
    def step(self):
        new_state = [cell for cell in self.state]
        for y in range(self.y):
            for x in range(self.x):
                neighbors = self.check_neighbors(x, y)
                state = self.state[y][x]
                if neighbors < 2 and state == True:
                    new_state[y][x] = False
                elif neighbors > 3 and state == True:
                    new_state[y][x] = False
                elif neighbors == 2:
                    new_state[y][x] = self.state[y][x]
                elif neighbors == 3 and state == False:
                    new_state[y][x] = True
        self.state = new_state

#--------------------------------------------------------
class SmoothAutomata(Automata):
    """Inspired by the implementation of a partially continuous game of life within the Netlogo demos - currently partially functional"""
    def check_neighbors(self, x, y):
        """returns mean of neighbor state turned on - in Moore neighborhood - wraps around"""
        neighbors = (
        self.state[y][x-1] + self.state[y][(x+1)%self.x]+
        self.state[y-1][x] + self.state[(y+1)%self.y][x]+
        self.state[y-1][x-1] + self.state[y-1][(x+1)%self.x]+
        self.state[(y+1)%self.y][x-1] + self.state[(y+1)%self.y][(x+1)%self.x]
        ) / 8
        return neighbors

    def format(self, cell):
        if cell <= .01:
            return None
        elif cell <= .25:
            return self.chars['.']
        elif cell <= .3:
            return self.chars['=']
        elif cell <= .35:
            return self.chars['#']
        elif cell <= .45:
            return self.chars['@']
        else:
            return None

    def step(self):
        # preset values for smoothlife
        min_birth = .278
        max_birth = .365
        min_survive = .267
        max_survive = .445
        new_state = [cell for cell in self.state]
        for y in range(self.y):
            for x in range(self.x):
                neighbors = self.check_neighbors(x, y)
                state = self.state[y][x]
                if neighbors >= min_birth and neighbors <= max_birth and state < min_birth:
                    new_state[y][x] = sigmoidclamp(state, min_birth, max_birth)
                elif max_survive >= neighbors >= min_survive and min_survive <= state <= max_survive:
                    new_state[y][x] = sigmoidclamp(state, min_survive, max_survive)
                elif neighbors < min_survive:
                    new_state[y][x] = (state +neighbors)/2
                else:
                    new_state[y][x] = (state+neighbors)/4
        self.state = new_state

#--------------------------------------------------------

class Seed(Automata):
    """Class for 'seed' cellular automata"""
    def step(self):
        new_state = [cell for cell in self.state]
        for y in range(self.y):
            for x in range(self.x):
                neighbors = self.check_neighbors(x, y)
                state = self.state[y][x]
                if neighbors == 2 and state == False:
                    new_state[y][x] = True
                else:
                    new_state[y][x] = False
        self.state = new_state
#--------------------------------------------------------
class BriansBrain(Automata):
    """Class for 'Brians Brain' cellular automata"""
    def step(self):
        new_state = [cell for cell in self.state]
        for y in range(self.y):
            for x in range(self.x):
                neighbors = self.check_neighbors(x, y)
                state = self.state[y][x]
                if neighbors == 2 and state == 0:
                    new_state[y][x] = 1
                elif state == 1:
                    new_state[y][x] = 2
                else:
                    new_state[y][x] = 0
        self.state = new_state

    # translates value into pygame surface
    def format(self, cell):
        if cell == False:
            return self.chars['.']
        elif cell == 1:
            return self.chars['o']
        else:
            return self.chars['x']

#--------------------------------------------------------
class Wireworld(Automata):
    """Class for 'Wireworld' cellular automata - Unimplemented"""
    def step(self):
        new_state = [cell for cell in self.state]
        for y in range(self.y):
            for x in range(self.x):
                neighbors = self.check_neighbors(x, y)
                state = self.state[y][x]
                if state == 0:
                    new_state[y][x] = 0
                elif state == 1:
                    new_state[y][x] = 2
                elif state == 2:
                    new_state[y][x] = 3
                elif state == 3 and 2 >= neighbors >= 1:
                    new_state[y][x] = 1
        self.state = new_state
#--------------------------------------------------------

class Fluid(Automata):

    def __init__(self, name, x, y, display_x, display_y, density):
        super().__init__(name, x, y, display_x, display_y, density)
        self.state = [[random.random() for x in range(self.x)] for y in range(self.y)]
        # predefine common font character to save on rendering time
        # water-specific characters
        self.chars = {
            "x": font.render("x", True, "Blue", "Black"),
            "o": font.render("o", True, "White", "Black"),
            ".": font.render(".", True, "White", "Black"),
            " ": font.render(" ", True, "White", "Black"),
            "#": font.render("#", True, "White", "Black"),
            "=": font.render("=", True, "White", "Black"),
            "@": font.render("@", True, "White", "Black"),
            "|": font.render("|", True, "White", "Black")
            }
        # fluid specific vars
        # level at which to skip cells
        self.dry = .001
        # level to overfill cells to enable water finding own level
        self.overfill = .01
        # max water level per cell
        self.max = 1.0


    def check_neighbors(self, x, y):
        """returns list of of neighbors turned on in Moore neighborhood - wraps around and also returns index of points"""
        neighbors = [
        (self.state[y][x-1], y, x-1), (self.state[y][(x+1)%self.x], y, (x+1)%self.x),
        (self.state[y-1][x], y-1, x), (self.state[(y+1)%self.y][x], (y+1)%self.y, x)
        ]
        return neighbors

    def step(self):
        new_state = [cell for cell in self.state]
        for y in range(self.y):
            for x in range(self.x):
                volume = self.state[y][x]
                # skips flow step if water level low enough
                if volume < self.dry:
                    pass
                # flows to blocks adjacent
                else:
                    for neighbor in self.check_neighbors(x, y):
                        if neighbor[0] < volume:
                            n_y, n_x = neighbor[1], neighbor[2]
                            flow = (volume - neighbor[0])/4
                            new_state[n_y][n_x] += flow
                            volume -= (volume-neighbor[0])/4
                    new_state[y][x] = volume
        self.state = new_state

    # translates values of characters
    def format(self, char):
        if char <= self.dry:
            return self.chars[' ']
        elif char <= .2:
            return self.chars['.']
        elif char <= .3:
            return self.chars['=']
        elif char <= .5:
            return self.chars['#']
        else:
            return self.chars['@']

#--------------------------------------------------------
class Automata3D():
    def __init__(self, name, x, y, z, display_x, display_y, density):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.start_density = density
        self.state = [[[random.random() < density for x in range(self.x)] for y in range(self.y)] for z in range(self.z)]
        self.display_size = (display_x, display_y)
        self.chars = {
            "x": font.render("x", True, "Blue", "Black"),
            "o": font.render("o", True, "White", "Black"),
            ".": font.render(".", True, "White", "Black"),
            " ": font.render(" ", True, "White", "Black"),
            "|": font.render("|", True, "White", "Black")
            }

    def check_neighbors(self, x, y, z):
        """returns number of neighbors turned on - in Moore neighborhood in 3D - wraps around"""
        neighbors = (
        (self.state[z][y][x-1] == 1) + (self.state[z][y][(x+1)%self.x] == 1)+
        (self.state[z][y-1][x] == 1) + (self.state[z][(y+1)%self.y][x] == 1)+
        (self.state[z][(y+1)%self.y][x-1] == 1) + (self.state[z][(y+1)%self.y][(x+1)%self.x] == 1)+
        (self.state[z-1][y][x] == 1) + (self.state[(z+1)%self.z][y][x] == 1) +
        (self.state[z-1][y][x-1] == 1) + (self.state[z-1][y][(x+1)%self.x] == 1)+
        (self.state[z-1][y-1][x] == 1) + (self.state[z-1][(y+1)%self.y][x] == 1)+
        (self.state[z-1][(y+1)%self.y][x-1] == 1) + (self.state[z-1][(y+1)%self.y][(x+1)%self.x] == 1) +
        (self.state[(z+1)%self.z][y][x-1] == 1) + (self.state[(z+1)%self.z][y][(x+1)%self.x] == 1)+
        (self.state[(z+1)%self.z][y-1][x] == 1) + (self.state[(z+1)%self.z][(y+1)%self.y][x] == 1)+
        (self.state[(z+1)%self.z][(y+1)%self.y][x-1] == 1) + (self.state[(z+1)%self.z][(y+1)%self.y][(x+1)%self.x] == 1)
        )
        return neighbors

    def step(self):
        random.seed()
        return [[[random.random() < .5 for x in range(self.x)] for y in range(self.y)] for z in range(self.z)]

    def format(self, char):
        if char == True:
            return self.chars['o']
        else:
            return None

    def render(self):
        """returns a rotated, formatted version of each character in each layer as pygame surfaces in an array"""
        to_render = []
        for z in range(self.z):
            for y in range(self.y):
                for x in range(self.x):
                    # retrieves the rendered ascci representation of the cell
                    buffer = self.format(self.state[z][y][x])
                    if buffer != None:
                        # adds the ascii to the blit buffer, formats in center of screen
                        to_render.append((buffer, ((x-y)*font_size+(self.display_size[0]/2), (x+y+z)*font_size-(self.z+self.x+self.y-3)/2*font_size+(self.display_size[1]/2))))
        return reversed(to_render)


#--------------------------------------------------------
class Life3D(Automata3D):
    def step(self):
        new_state = [[cell for cell in slice] for slice in self.state]
        for z in range(self.z):
            for y in range(self.y):
                for x in range(self.x):
                    neighbors = self.check_neighbors(x, y, z)
                    state = self.state[z][y][x]
                    if neighbors < 2 and state == True:
                        new_state[z][y][x] = False
                    elif neighbors > 3 and state == True:
                        new_state[z][y][x] = False
                    elif neighbors == 2:
                        pass
                    elif neighbors == 3 and state == False:
                        new_state[z][y][x] = True
        self.state = new_state

#--------------------------------------------------------
class Fluid3D(Automata3D):
    def __init__(self, name, x, y, z, display_x, display_y, density):
        super().__init__(name, x, y, z, display_x, display_y, density)
        # predefine common font character to save on rendering time
        self.chars = {
            "x": font.render("x", True, "Blue", "Black"),
            "o": font.render("o", True, "White", "Black"),
            ".": font.render(".", True, "Blue", "Black"),
            " ": font.render(" ", True, "White", "Black"),
            "#": font.render("#", True, "Blue", "Black"),
            "=": font.render("=", True, "Blue", "Black"),
            "@": font.render("@", True, "Blue", "Black"),
            "$": font.render("$", True, "Blue", "Black"),
            "^": font.render(" ", True, "Blue", "Blue"),
            "|": font.render("|", True, "White", "Black")
            }
        self.dry = .01
        self.overfill = .01
        self.max = 1.0
        self.viscosity = .6

    def format(self, char):
        """returns rendered character surfaces from values"""
        if char <= self.dry:
            return None
        elif char < .1:
            return self.chars['.']
        elif char <= .4:
            return self.chars['=']
        elif char <= .5:
            return self.chars['#']
        elif char <= .9:
            return self.chars['$']
        elif char <= 1.0:
            return self.chars['@']
        elif char > 1.0:
            return self.chars['^']

    def check_neighbors(self, x, y, z):
        """returns list of of neighbors turned on in Von Neumann neighborhood - doesn't wrap around and also returns position of points"""
        neighbors = []
        if x > 0:
            neighbors.append((self.state[z][y][x-1], (z, y, x-1)))
        if x < (self.x-1):
            neighbors.append((self.state[z][y][(x+1)], (z, y, x+1)))
        if y > 0:
            neighbors.append((self.state[z][y-1][x], (z, y-1, x)))
        if y < (self.y-1):
            neighbors.append((self.state[z][(y+1)][x], (z, (y+1), x)))
        if z > 0:
            neighbors.append((self.state[z-1][y][x], (z-1, y, x)))
        if z < (self.z-1):
            neighbors.append((self.state[(z+1)][y][x], ((z+1), y, x)))
        return neighbors

    def step(self):
        new_state = [[cell for cell in slice] for slice in self.state]
        for z in range(self.z):
            for y in range(self.y):
                for x in range(self.x):
                    volume = self.state[z][y][x]
                    # skips flow step if water level low enough
                    if volume < self.dry:
                        pass
                    else:
                        neighbors = self.check_neighbors(x,y,z)
                        for neighbor in neighbors:
                            n_z, n_y, n_x, = neighbor[1]
                            neighbor_volume = neighbor[0]
                            flow = 0
                            # flows to blocks above:
                            if n_z < z:
                                if volume > self.max:
                                    flow = volume - self.max
                            # flows to blocks below:
                            if n_z > z:
                                # handles normal flow
                                if neighbor_volume < self.max:
                                    if neighbor_volume + volume < self.max:
                                        flow = (volume*self.viscosity)/len(neighbors)
                                    else:
                                        flow = (self.max - neighbor_volume)*self.viscosity/len(neighbors)
                                # allows for slight compression
                                elif neighbor_volume >= self.max:
                                    if neighbor_volume < (volume + self.overfill):
                                        flow = self.overfill
                            # flow to side
                            if n_z == z:
                                if neighbor_volume < volume:
                                    flow = ((volume - neighbor_volume)*self.viscosity)/len(neighbors)
                                # writes volume and flow
                            new_state[n_z][n_y][n_x] += flow
                            new_state[z][y][x] -= flow
        self.state = new_state


#--------------------------------------------------------

##world = BriansBrain(40, 40, .5)
##world.run()
def create_models(display_size):
    lifemodel = Life("game of life", 74, 45, *display_size, .3)
    # brianmodel = BriansBrain("brian's brain", 74, 45, *display_size, .3)
    # seedmodel = Seed("'Seed' model", 74, 45, *display_size, .1)
    # smoothmodel = SmoothAutomata("life-ish smooth automata", 74, 45, *display_size, .4)
    # life3dmodel = Life3D("game of life 3D", 15, 15, 10, *display_size, .1)
    # fluidmodel = Fluid("Simple Fluid Model 2D", 74, 45, *display_size, .8)
    # fluidmodel3D = Fluid3D("Simple Fluid Model 3D", 20, 20, 10, *display_size, .4)
    # models = [lifemodel, brianmodel, seedmodel, smoothmodel, life3dmodel, fluidmodel, fluidmodel3D]
    models = [lifemodel]
    return models
