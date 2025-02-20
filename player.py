import random, math

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
    
    def __str__(self):
        if self.alive:
            text = f"{self.name} the {self.role} has {self.health} out of "
            text += f"{self.max_health} points of health."
            if self.resistance:
                text += f" They have resistance."
        else:
            text = f"{self.name}s the {self.role} is dead."
            
        return text
    
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