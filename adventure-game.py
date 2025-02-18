import random, math
import adventuretexts as at

class player:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.alive = True
        self.max_health = self.__decide_health()
        self.health = self.max_health
        self.possition = None
        self.cooldown = 0
        self.resistance = 0
    
    def __decide_health(self):
        if self.role == 'Paladin':
            return 40 + random.randint(0, 10)
        elif self.role == 'Warior':
            return 25 + random.randint(0, 10)
        elif self.role == 'Warlock':
            return 10 + random.randint(0, 10)
    
    def injured(self, damage):
        if self.resistance:
            self.health -= math.floor(damage / 2)
            print(f'{self.name} resisted some of the damage.')
        else:
            self.health -= damage
        
        if self.health <= 0:
            print(f'{self.name} died.')
            self.alive = False
    
    def attack(self):
        if self.role == 'Paladin':
            return random.randint(1, 6)
        elif self.role == 'Warior':
            return random.randint(1, 6) + random.randint(1, 4)
        elif self.role == 'Warlock':
            return random.randint(1, 10) + random.randint(1, 10)
    
    def use_abillity(self, target):
        if self.role == 'Paladin':
            self.cooldown = 4
            healed = random.randint(1, 4) + random.randint(1, 4)
            target.health += healed
            if target.health > target.max_health:
                target.health = target.max_health
                print(f'{target.name} is fully healed.')
            else:
                print(f'{target.name} got healed {healed} points.')
        elif self.role == 'Warior':
            self.cooldown = 3
            print('You totes used your abillity') #TODO
        elif self.role == 'Warlock':
            self.cooldown = 6
            target.resistance = 3
            print(f'{target.name} feel invinceble.')


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
    roles = ['Paladin', 'Warior', 'Warlock']
    for i in range(num):
        name = input(f'\nName player {i + 1}: ')
        text = f'What role shuld {name} be?\n1 - Paladin'
        text += ', 2 - Warior or 3 - Warlock: '
        role_num = def_int_input(1, 3, text) - 1
        players.append(player(name, roles[role_num]))
        
        text = f'{players[i].name} is a {players[i].role} with'
        text += f' {players[i].max_health} points of health.'
        print(text)
    
    return players


def add_tiles(num, exist, neigbor):
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
    print(at.instructions)
    player_num = def_int_input(1, 4, 'How many players? (1-4): ')
    players = create_players(player_num)
    
    monster_health = 0
    if len(players) > 1:
        for pc in players:
            monster_health += pc.health * 2
    else:
        monster_health += math.floor(players[0].health * 1.5)
    #if player_num > 1:
    #    monster_health = int((monster_health / player_num) * (player_num - 1))
    #else:
    #    monster_health = int(monster_health / 2)
    
    tiles = create_tiles()
    
    for pc in players:
        pc.possition = tiles[0]
    
    return players, tiles, monster_health


def get_directions(dir_list, monster, pc):
    directions = ''
    if monster < 1 and pc.possition.type == 'L':
        directions = ', '.join(dir_list)
        directions += ' and you can leave'
        dir_list.append('Leave')
    elif monster > 0 and pc.possition.type == 'M':
        directions = ', '.join(dir_list)
        directions += ' and you can fight the monster.'
        directions += f' You have {pc.health} points of health'
        dir_list.append('Fight')
    elif len(dir_list) == 1:
        directions = dir_list[0]
    else:
        directions = ', '.join(dir_list[:-1])
        directions += ' and ' + dir_list[-1]
    
    if not pc.cooldown:
        directions += '. You may also use your abillity'
        dir_list.append('Abillity')
    else:
        pc.cooldown -= 1
    
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


def pcs_at_pc_pos(players, pc):
    together = []
    for other_pc in players:
        same_place = pc.possition == other_pc.possition
        if other_pc != pc and same_place:
            together.append(other_pc)
    
    return together


def move_pc(pc, players, at_m, encounter, towards, monster):
    if at_m and pc.possition.type == 'M':
        at_m.remove(pc)
    pc.possition = pc.possition.doors[towards]
    
    together = pcs_at_pc_pos(players, pc)
    
    if not encounter and pc.possition.type == 'M':
        print(random.choice(at.first))
        encounter = True
    else:
        text = pc.possition.description
        if len(together) > 2:
            text += f' {together[0].name}, {together[1].name} and '
            text += f'{together[2].name}' + random.choice(at.togeter)
        if len(together) > 1:
            text += f' {together[0].name} and {together[1].name}'
            text += random.choice(at.togeter)
        elif together:
            text += f' {together[0].name}' + random.choice(at.meet)
        
        print(text)
    
    if monster > 0 and pc.possition.type == 'M':
        at_m.append(pc)
    
    return at_m, encounter


def use_abillity(players, pc):
    together = pcs_at_pc_pos(players, pc)
    if together:
        text = 'Choose who to use your abillity on:\n'
        for i, oter_pc in enumerate(together):
            max = i + 2
            text += f'{i+1} - {oter_pc.name}, '
        text = text[:-2] + f' or {max} - yourself: '
        
        choise = def_int_input(1, max, text) - 1
        if choise == max - 1:
            pc.use_abillity(pc)
        else:
            pc.use_abillity(together[choise])
    else:
        pc.use_abillity(pc)


def attack(pc, monster, at_m):
    #print('You shake in your boots!')
    damage = pc.attack()
    monster -= damage
    
    if monster <= 0:
        num = random.randint(0, len(at.finall) - 1)
        print(at.finall[num][0] + pc.name + at.finall[num][1])
        pc.possition.description = random.choice(at.after)
        at_m = []
    else:
        text = random.choice(at.attack)
        print(f"{text}{damage} points of damage.")
    
    return monster, at_m


def play(players, tiles, monster): # To long
    encounter = False
    at_m = []
    dead = []
    print(f'\n\n----------- oOo -----------')
    print(at.start)
    print_map(tiles)
    input()
    
    while True:
        for pc in players:
            dir_list = list(pc.possition.doors.keys())
            dir_list, directions = get_directions(dir_list, monster, pc)
            
            print(f'\n----------- {pc.name} -----------')
            print(f'\n{pc.name}s turn. You can go {directions}.')
            choise = player_choise(dir_list, 'Choose what to do: ')
            
            if choise == 'Leave':
                return True, dead
            
            if choise in ['North', 'South', 'East', 'West']:
                a = move_pc(pc, players, at_m, encounter, choise, monster)
                at_m, encounter = a
                if pc.possition.type == 'T':
                    print_map(tiles)
            elif choise == 'Abillity':
                use_abillity(players, pc)
            else:
                monster, at_m = attack(pc, monster, at_m)
            input()
        
        if at_m and len(players + dead) > 2:
            damage1 = random.randint(1, 10)
            damage2 = random.randint(1, 10)
            text2 = ''
            
            if len(at_m) > 1 and random.randint(0, 1):
                text = f' dealing {damage1} points of damage.' #TODO
                text2 = f' dealing {damage2} points of damage.' #TODO
            else:
                text = f' dealing {damage1 + damage2} points of damage.' #TODO
            
            print('\n/\\/\\/\\/\\/\\/ Monster \\/\\/\\/\\/\\/\\\n')
            print(random.choice(at.m_attack) + at_m[0].name + text)
            if text2:
                print(random.choice(at.m_attack) + at_m[1].name + text2)
                at_m[0].injured(damage1)
                at_m[1].injured(damage2)
            else:
                at_m[0].injured(damage1 + damage2)
            
            if not at_m[0].alive:
                dead.append(at_m[0])
                players.remove(at_m[0])
                at_m.remove(at_m[0])
            
            if text2 and not at_m[1].alive:
                dead.append(at_m[0])
                players.remove(at_m[0])
                at_m.remove(at_m[0])
            
            if not players:
                print(monster)
                return False, dead
            
            input()
        elif at_m:
            damage = random.randint(1, 10)
            text = f' dealing {damage} points of damage.' #TODO
            print('\n/\\/\\/\\/\\/\\/ Monster \\/\\/\\/\\/\\/\\\n')
            print(random.choice(at.m_attack) + at_m[0].name + text)
            at_m[0].injured(damage)
            
            if not at_m[0].alive:
                dead.append(at_m[0])
                players.remove(at_m[0])
                at_m.remove(at_m[0])
            
            if not players:
                print(monster)
                return False, dead
            
            input()
        
        for pc in players:
            if pc.resistance:
                pc.resistance -= 1
                if not pc.resistance:
                    print(f'-- {pc.name}s resistance ended. --')


def end(won, dead):
    print(f'\n----------- oOo -----------')
    if not dead:
        print(random.choice(at.triumf))
    elif won:
        if len(dead) > 2:
            names = f's {dead[0].name}, {dead[1].name} and {dead[2].name}'
        elif len(dead) > 1:
            names = f's {dead[0].name} and {dead[1].name}'
        else:
            names = f' {dead[0].name}'
        num = random.randint(0, len(at.viktory) - 1)
        print(at.viktory[num][0] + names + at.viktory[num][1])
    else:
        print(random.choice(at.defeat))


if __name__ == '__main__':
    players, tiles, monster = setupp()
    win, dead = play(players, tiles, monster)
    end(win, dead)