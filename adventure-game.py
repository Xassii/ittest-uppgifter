import random, math
from game_state import game_state
from player import player
from room import room
import adventuretexts as at

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
    tiles.append(room(0, 0, 'You return to the start.'))
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
    
    tiles = create_tiles()
    
    for pc in players:
        pc.possition = tiles[0]
    
    game = game_state(monster_health, player_num, players, tiles)
    
    return game


def get_directions(dir_list, game): #TODO Add rest option
    directions = ''
    m_hp = game.monster['hp']
    pc = game.current
    
    if m_hp < 1 and pc.possition.type == 'L':
        directions = ', '.join(dir_list)
        directions += ' and you can leave'
        dir_list.append('Leave')
    elif m_hp > 0 and pc.possition.type == 'M':
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
        print(f'You need to chose {poss}.') #TODO print nicer


def move_pc(game, encounter, towards):
    pc = game.current
    at_m = game.monster['p_at']
    
    if at_m and pc.possition.type == 'M':
        at_m.remove(pc)
    pc.possition = pc.possition.doors[towards]
    
    together = game.together_with_current()
    
    if not encounter and pc.possition.type == 'M':
        print(random.choice(at.first))
        encounter = True
    else:
        text = pc.possition.description
        if len(together) > 2:
            text += f' {together[0].name}, {together[1].name} and '
            text += f'{together[2].name}' + random.choice(at.togeter)
        elif len(together) > 1:
            text += f' {together[0].name} and {together[1].name}'
            text += random.choice(at.togeter)
        elif together:
            text += f' {together[0].name}' + random.choice(at.meet)
        
        print(text)
    
    if game.monster['hp'] > 0 and pc.possition.type == 'M':
        at_m.append(pc)
    
    return encounter


def use_abillity(game):
    pc = game.current
    together = game.together_with_current()
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


def attack(game):
    #print('You shake in your boots!')
    pc = game.current
    damage = pc.attack()
    game.monster['hp'] -= damage
    
    if game.monster['hp'] <= 0: #TODO diffrent text depending on class
        num = random.randint(0, len(at.finall) - 1)
        print(at.finall[num][0] + pc.name + at.finall[num][1])
        pc.possition.description = random.choice(at.after)
        game.monster['p_at'] = []
    else: #TODO diffrent text depending on class
        text = random.choice(at.attack)
        print(f"{text}{damage} points of damage.")


def end(won, game):
    dead = game.dead
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


def play(): # To long
    game = setupp()
    encounter = False
    print(f'\n\n----------- oOo -----------')
    print(at.start)
    #print(game)
    #game.print_map()
    input()
    
    while True:
        if isinstance(game.current, dict):
            if not game.current['p_at']: #if no players at monster
                game.reduce_ressistance()
                game.next_turn()
                continue
            
            game.m_attack()
            input()
            
            if not game.players:
                end(False, game)
                return None
            game.reduce_ressistance()
        else:
            pc = game.current
            dir_list = list(pc.possition.doors.keys())
            dir_list, directions = get_directions(dir_list, game)
            
            print(f'\n----------- {pc.name} -----------')
            print(f'\n{pc.name}s turn. You can go {directions}.')
            choise = player_choise(dir_list, 'Choose what to do: ')
            
            if choise == 'Leave':
                end(True, game)
                return None
            
            if choise in ['North', 'South', 'East', 'West']:
                encounter = move_pc(game, encounter, choise)
                if pc.possition.type == 'T':
                    game.print_map()
            elif choise == 'Abillity':
                use_abillity(game)
            else:
                attack(game)
            input()
        
        game.next_turn()


if __name__ == '__main__':
    play()