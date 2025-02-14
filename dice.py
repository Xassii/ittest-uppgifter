import random, time

def wait_for_trow():
    time.sleep(2)
    print('...')
    time.sleep(2)
    print('...')
    time.sleep(2)


def throw_dice(name):
    print(f'\n{name}s turn!')
    wait_for_trow()
    one = random.randint(1,6)
    print(f'First throw was {one}')
    wait_for_trow()
    two = random.randint(1,6)
    print(f'Second throw was {two}\n')

    return one + two

if __name__ == '__main__':
    p1 = input('Player one name: ')
    p2 = input('Player two name: ')
    score1 = throw_dice(p1)
    time.sleep(1)
    score2 = throw_dice(p2)
    if score1 > score2:
        print(f'{p1} won!')
    elif score1 < score2:
        print(f'{p2} won!')
    else:
        print('Tie')