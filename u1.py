# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:20:16 2025

@author: amanda
"""

import random

num = 30
num2 = 30

if num == num2:
    print('num == num2')
elif num < num2:
    print('num2 är större')
else:
    print('num är större')

#---------------

num3 = None

if num3 == None:
    print('None')

#---------------

is_sunny = True
is_warm = False

if is_sunny and is_warm:
    print('Det är varmt. Det är soligt.')
elif is_sunny:
    print('Det är soligt.')
elif is_warm:
    print('Det är varmt.')
else:
    print('Det är varken varmt eller soligt.')

#---------------

random_number = random.randint(1, 3)

guess = int(input('Guess a number: '))

if guess == random_number:
    print('Correct!')
else:
    print(f'Wrong. Nummber was {random_number}.')