import time, sys, os, minmodul
"""
for x in range(5, -1, -1):
    print(x)
    time.sleep(1)

print('And now we start')

with open('short-text.txt', 'w') as file:
    file.write("Första raden\nAndra raden\nTredje raden\n")
"""
print(f'Python-version: {sys.version.split()[0]}')
for i in os.listdir():
    print(i)

minmodul.insult()