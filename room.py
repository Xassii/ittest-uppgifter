class room:
    def __init__(self, x, y, description):
        self.possition = [x, y]
        self.description = description
        self.doors = {}
        self.type = ''
    
    def connect(self, neigbour, direction, dir_back):
        self.doors[direction] = neigbour
        neigbour.doors[dir_back] = self