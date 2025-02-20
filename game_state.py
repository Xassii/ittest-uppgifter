import random
import adventuretexts as at

class game_state:
    def __init__(self, hp, turns, p, tiles):
        self.monster = {'hp': hp, 'p_at': [], 'Location': None}
        self.__turns = turns
        self.__turn = 0
        self.players = p
        self.__dead = []
        self.current = self.players[0]
        self.__tiles = tiles
        self.__map = self.__create_map()
        self.__monster_str = self.__determen_strength()
        
    def __determen_strength(self):
        if len(self.players) > 2:
            return 2
        elif len(self.players) > 1:
            return 1
        else:
            return 0
    
    def next_turn(self):
        self.__turn = (self.__turn + 1) % (self.__turns + 1)
        
        if self.__turn == self.__turns:
            self.current = self.monster
        else:
            self.current = self.players[self.__turn]
    
    def __deal_damage(self, n, damage):
        pc = self.monster['p_at'][n]
        text = f' dealing {damage} points of damage.'
        print(random.choice(at.m_attack) + pc.name + text)
        pc.injured(damage)
    
    def __check_dead(self, pc):
        if not pc.alive:
            self.__dead.append(pc)
            self.players.remove(pc)
            self.monster['p_at'].remove(pc)
            self.__turn = -1
    
    def m_attack(self):
        damage2 = 0
        at_m = self.monster['p_at']
        if self.__monster_str > 2:
            damage1 = random.randint(1, 10)
            damage2 = random.randint(1, 10)
        elif self.__monster_str > 1:
            damage1 = random.randint(1, 10)
        else:
            damage1 = random.randint(1, 6)
        
        print('\n/\\/\\/\\/\\/\\/ Monster \\/\\/\\/\\/\\/\\\n')
        if damage2 and len(at_m) > 1 and random.randint(0, 1):
            self.__deal_damage(0, damage1)
            self.__deal_damage(1, damage2)
            self.__check_dead(at_m[1])
        else:
            self.__deal_damage(0, damage1 + damage2)
        self.__check_dead(at_m[0])
    
    def reduce_ressistance(self):
        for pc in self.players:
            if pc.resistance > 0:
                pc.resistance -= 1
                if not pc.resistance:
                    print(f'-- {pc.name}s resistance ended. --')
    
    def together_with_current(self):
        together = []
        for pc in self.players:
            if not self and self.current.possition == pc.possition:
                together.append(pc)
        
        return together
    
    def __create_map(self):
        x_pos = []
        y_pos = []
        type = []
        map = []
        
        for room in self.__tiles:
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
        return map
    
    def print_map(self):
        for i in self.__map:
            print(' '.join(i))