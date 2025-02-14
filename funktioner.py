def greetings(name):
    print(f'GREETINGS {name}!')


def summurize(x, y):
    return x + y


def sum_all(numbers):
    sum = 0
    for number in numbers:
        sum += number
    return sum


def commpare(x, y):
    if x > y:
        return x
    return y


def mostly_true(a, b, c):
    if a and b:
        return True
    if a and c:
        return True
    if b and c:
        return True
    return False


def print_all(x):
    for i in range(1, x + 1):
        print(i)


def print_all_reverse(x):
    for i in range(x, -1, -1):
        print(i)


name = input('Vad heter du? ')
greetings(name)

sum = summurize(5, 7)
print(sum)

print_all(12)
print_all_reverse(12)