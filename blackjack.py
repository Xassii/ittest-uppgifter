import random

def choose_ace(cards):
    card = 0
    print(f'Got ace!\nCurrent score is {cards}. Should the ace be worth 1 or 11?')
    while True:
        try:
            card = int(input('Choose 1 or 11: '))
            if card == 1 or card == 11:
                return card
            else:
                print('\n\nChoose only 1 or 11!')
        except ValueError:
            print('\n\nOnly write a number!')


def choose_end(cards):
    print(f'Youre score is {cards}. Do you want an other card?')
    while True:
        end = input('1 = more cards, 2 = done: ')
        if end == '1':
            return False
        elif end == '2':
            return True
        else:
            print('\n\nOnly choose 1 or 2!')


comp_cards = 0
my_cards = 0
end = False

while comp_cards < 17:
    card = random.randint(1, 10)
    if comp_cards > 10 or card > 1:
        comp_cards += card
    else:
        comp_cards += 11

while not end:
    card = random.randint(1, 10)
    if card == 1:
        card = choose_ace(my_cards)
    my_cards += card
    if my_cards >= 21:
        break
    end = choose_end(my_cards)

print(f'Computer got {comp_cards}, you got {my_cards}.')