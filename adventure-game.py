import random
import adventuretexts as at

class player:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.possition = None
    
    def injured(self, damage):
        self.health -= damage


class room:
    def __init__(self, x, y, description):
        self.possition = [x, y]
        self.description = description
        self.doors = {}
        self.type = ''
    
    def connect(self, neigbour, direction, dir_back):
        self.doors[direction] = neigbour
        neigbour.doors[dir_back] = self


def def_int_input(min, max, text=''):
    if not text:
        text = f'\nWrite number between {min} and {max}: '
    while True:
        try:
            num = int(input(text))
            if num <= max and num >= min:
                return num
            print(f'\nNumber need to be between {min} and {max}!')
        except ValueError:
            print('\nNeed to be a number!')


def create_players(num):
    players = []
    for i in range(num):
        name = input(f'\nName player {i + 1}: ')
        text = f'How much health should {name} have? (10-50): '
        health = def_int_input(10, 50, text)
        players.append(player(name, health))
    
    return players


def add_tiles(num, exist, neigbor): #This aint great
    tiles = []
    for i in range(num):
        next_room = random.choice(neigbor)
        neigbor.remove(next_room)
        exist.append(next_room)
        text = random.choice(at.r_desc)
        tiles.append(room(next_room[0], next_room[1], text))
        
        if not [next_room[0]+1, next_room[1]] in neigbor + exist:
            neigbor.append([next_room[0]+1, next_room[1]])
        if not [next_room[0]-1, next_room[1]] in neigbor + exist:
            neigbor.append([next_room[0]-1, next_room[1]])
        if not [next_room[0], next_room[1]+1] in neigbor + exist:
            neigbor.append([next_room[0], next_room[1]+1])
        if not [next_room[0], next_room[1]-1] in neigbor + exist:
            neigbor.append([next_room[0], next_room[1]-1])
        
        while len(neigbor) > 8:
            neigbor.remove(random.choice(neigbor))
    
    return tiles


def connect_tiles(tiles):
    for room in tiles:
        for other_room in tiles:
            x1, y1 = room.possition
            x2, y2 = other_room.possition
            
            if x2 + 1 == x1 and y2 == y1 and not 'South' in room.doors.keys():
                room.connect(other_room, 'South', 'North')
                if random.randint(0, 9):
                    break
            elif x2 - 1 == x1 and y2 == y1 and not 'North' in room.doors.keys():
                room.connect(other_room, 'North', 'South')
                if random.randint(0, 9):
                    break
            elif x2 == x1 and y2 + 1 == y1 and not 'West' in room.doors.keys():
                room.connect(other_room, 'West', 'East')
                if random.randint(0, 9):
                    break
            elif x2 == x1 and y2 - 1 == y1 and not 'East' in room.doors.keys():
                room.connect(other_room, 'East', 'West')
                if random.randint(0, 9):
                    break


def create_tiles(): #This aint great
    tiles = []
    tiles.append(room(0, 0, 'You return to the start'))
    for x, y in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
        text = random.choice(at.r_desc)
        tiles.append(room(x, y, text))
    
    tile_num = def_int_input(5, 25, '\nHow many rooms shoud there be? (5-25): ')
    tile_num -= 5
    if tile_num:
        existing_rooms = [[0, 0], [-1, 0], [0, -1], [1, 0], [0, 1]]
        neigbors = [[2, 0], [1, 1], [1, -1], [-2, 0], [-1, 1],
                    [-1, -1], [0, -2], [0, 2]]
        new = add_tiles(tile_num, existing_rooms, neigbors)
        tiles = tiles + new
    
    connect_tiles(tiles)
    
    types = ['M', 'L']
    if tile_num >= 10:
        types.append('T')
    tiles[0].type = 'S'
    for i in types:
        while True:
            tile = random.choice(tiles)
            if tile.type == '':
                tile.type = i
                if i == 'M':
                    tile.description = random.choice(at.m_desc)
                elif i == 'T':
                    tile.description += at.t_desc[0]
                else:
                    tile.description += random.choice(at.l_desc)
                break
    
    return tiles


def setupp():
    player_num = def_int_input(1, 4, 'How many players? (1-4): ')
    players = create_players(player_num)
    
    monster_health = 0
    for i in players:
        monster_health += i.health
    if player_num > 1:
        monster_health = int((monster_health / player_num) * (player_num - 1))
    else:
        monster_health = int(monster_health / 2)
    
    tiles = create_tiles()
    
    for player in players:
        player.possition = tiles[0]
    
    return players, tiles, monster_health


def get_directions(dir_list, monster, player):
    directions = ''
    if monster < 1 and player.possition.type == 'L':
        directions = ', '.join(dir_list)
        directions += ' and you can leave'
        dir_list.append('Leave')
    elif monster > 0 and player.possition.type == 'M':
        directions = ', '.join(dir_list)
        directions += ' and you can fight the monster.'
        directions += f' You have {player.health} points of health'
        dir_list.append('Fight')
    elif len(dir_list) == 1:
        directions = dir_list[0]
    else:
        directions = ', '.join(dir_list[:-1])
        directions += ' and ' + dir_list[-1]
    
    return dir_list, directions


def player_choise(possebileties, text):
    poss = {}
    for a in possebileties:
        poss[a[0]] = a
    while True:
        choise = input(text)
        if choise and choise[0].upper() in poss:
            return poss[choise[0].upper()]
        print(f'You need to chose {poss}.')


def print_map(rooms):
    x_pos = []
    y_pos = []
    type = []
    map = []
    
    for room in rooms:
        x_pos.append(room.possition[0])
        y_pos.append(room.possition[1])
        type.append(room.type)
    
    x_pos = [x - min(x_pos) for x in x_pos]
    y_pos = [y - min(y_pos) for y in y_pos]
    
    size_x = max(x_pos) + 1
    size_y = max(y_pos) + 1
    
    for i in range(size_x):
        map.append([])
        for j in range(size_y):
            map[i].append('■')
    
    for x, y, t in zip(x_pos, y_pos, type):
        if t:
            map[x][y] = t
        else:
            map[x][y] = '□'
    
    map.reverse()
    for i in map:
        print(' '.join(i))


def play(players, tiles, monster): # To long
    encounterd_monster = False
    at_monster = []
    dead = []
    print(f'\n\n----------- oOo -----------')
    print(at.start)
    #print_map(tiles)
    
    while True:
        for player in players:
            dir_list = list(player.possition.doors.keys())
            dir_list, directions = get_directions(dir_list, monster, player)
            
            print(f'\n----------- {player.name} -----------')
            print(f'\n{player.name}s turn. You can go {directions}.')
            choise = player_choise(dir_list, 'Choose what to do: ')
            
            if choise in ['North', 'South', 'East', 'West']:
                if player.possition.type == 'M':
                    at_monster.remove(player)
                player.possition = player.possition.doors[choise]
                
                if not encounterd_monster and player.possition.type == 'M':
                    print(random.choice(at.first))
                    encounterd_monster = True
                else:
                    print(player.possition.description)
                
                if player.possition.type == 'T':
                    print_map(tiles)
                elif player.possition.type == 'M':
                    at_monster.append(player)
            elif choise == 'Leave':
                return True, players, dead
            else:
                #print('You shake in your boots!')
                damage = random.randint(1, 6)
                monster -= damage
                if monster <= 0:
                    num = random.randint(0, len(at.finall) - 1)
                    print(at.finall[num][0] + player.name + at.finall[num][1])
                    player.possition.description = random.choice(at.after)
                    player.possition.type = ''
                    at_monster = []
                else:
                    text = random.choice(at.attack)
                    print(f"{text}{damage} points of damage.")
            input()
        
        if at_monster:
            damage = random.randint(1, 6)
            at_monster[0].injured(damage)
            
            text = f' dealing {damage} points of damage.'
            print('\n/\\/\\/\\/\\/\\/ Monster \\/\\/\\/\\/\\/\\\n')
            print(random.choice(at.m_attack) + at_monster[0].name + text)
            
            if at_monster[0].health <= 0:
                print(f'{at_monster[0].name} died.')
                dead.append(at_monster[0].name)
                players.remove(at_monster[0])
                at_monster.remove(at_monster[0])
                if not players:
                    return False, players, dead
            input()


if __name__ == '__main__':
    players, tiles, monster = setupp()
    won, players, dead = play(players, tiles, monster)
    print(f'\n----------- oOo -----------')
    if not dead:
        print(random.choice(at.triumf))
    elif won:
        if len(dead) > 2:
            names = f's {dead[0]}, {dead[1]} and {dead[2]}'
        elif len(dead) > 1:
            names = f's {dead[0]} and {dead[1]}'
        else:
            names = f' {dead[0]}'
        num = random.randint(0, len(at.viktory) - 1)
        print(at.viktory[num][0] + names + at.viktory[num][1])
    else:
        print(random.choice(at.defeat))