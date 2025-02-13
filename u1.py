# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:20:16 2025

@author: amanda
"""

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

#--------------- change

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