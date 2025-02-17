import random

class player:
    def __init__(self, name):
        self.health = 20
        self.name = name


def visit_m(monster, discoverd, p):
    print(f'{p.name} steps into the cortyard. The house is on the werge of being compleatly owergrown with vines but you can probobly still get throu the door to the north. The western wing looks almost compleatly collapsed but it might be worth it to check throu the rubble. To the east the plants have gown wilde in what you presume used to be a guarden. You can see the path you came frome thrue the gate to the south.')
    if monster == 3 and discoverd:
        print('- The monster attacks. -')
    elif monster == 3:
        print('In the northeastern corner of the cortyard there is an old well.')


def visit_n(monster, discoverd, p):
    print(f'{p.name} enter the house.')
    if monster == 1 and discoverd:
        print('- The monster attacks. -')
    elif monster == 1:
        print('One of the old doors shake.')


def visit_e(monster, discoverd, p):
    print(f'{p.name} fight to move throu the tall grass.')
    if monster == 4 and discoverd:
        print('- The monster attacks. -')
    elif monster == 4:
        print('Everything is quiet.')


def visit_s(p):
    print(f'{p.name} walk onto the rode.')


def visit_w(monster, discoverd, p):
    print(f'{p.name} carfully step onto the rubble.')
    if monster == 2 and discoverd:
        print('- The monster attacks. -')
    elif monster == 2:
        print('I dont know what to wright.')


player_at = 5
monster_hp = 15
monster_at = random.randint(1, 4)
first_contackt = False
the_player = player(input('What do you want to be called? '))

while True:
    if player_at == 5 and monster_hp <= 0:
        print(f'{the_player.name} won.')
        break
    if the_player.health <= 0:
        print(f'{the_player.name} died.')
        break
    
    choise = input(f'-What will you do {the_player.name}? ')
    
    choose_n = choise == 'n' or 'north' in choise.lower()
    choose_e = choise == 'e' or 'east' in choise.lower()
    choose_s = choise == 's' or 'south' in choise.lower()
    choose_w = choise == 'w' or 'west' in choise.lower()
    choose_f = choise == 'f' or 'fight' in choise.lower()
    
    choose_m = (choose_n and player_at == 5) or (choose_e and player_at == 2)
    choose_m = choose_m or (choose_s and player_at == 1)
    choose_m = choose_m or (choose_w and player_at == 4)
    
    if choose_f and player_at == monster_at:
        monster_hp -= random.randint(1, 6)
        if monster_hp <= 0:
            print('The monster died.')
            monster_at = 0
    
    if choose_m:
        player_at = 3
        visit_m(monster_at, first_contackt, the_player)
    elif choose_n or (choose_f and player_at == 1):
        player_at = 1
        visit_n(monster_at, first_contackt, the_player)
    elif choose_e or (choose_f and player_at == 4):
        player_at = 4
        visit_e(monster_at, first_contackt, the_player)
    elif choose_s or (choose_f and player_at == 5):
        player_at = 5
        visit_s(the_player)
    elif choose_w or (choose_f and player_at == 2):
        player_at = 2
        visit_w(monster_at, first_contackt, the_player)
    
    if first_contackt and monster_hp > 0 and player_at == monster_at:
        the_player.health -= random.randint(1, 6)
    elif player_at == monster_at:
        first_contackt = True