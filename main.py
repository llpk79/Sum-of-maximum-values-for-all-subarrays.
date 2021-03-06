"""This is a terribly slow, early attempt at solving this problem. Do not use this code!"""


def get_left(lefts, x, y):
    if isinstance(lefts.get(x), int):
        lefts[x] = (lefts[x], y)
    elif isinstance(lefts.get(x), tuple):
        lefts[x] = (*lefts[x], y)
    else:
        lefts[x] = y
    return lefts


def get_right(rights, x, y):
    rights[x] = y
    return rights


def get_total(lefts, rights, x):
    total = x * lefts[x] * rights[x]
    del(rights[x])
    del(lefts[x])
    return total


def is_multiple(multiples, x, i, j):
    if multiples.get(x):
        multiples[x] = *multiples[x], (i, len(multiples[x]))
    elif not multiples.get(x):
        multiples[x] = (j, 0), (i, 1)
    return multiples


def get_multi_right(rights, multiples, x, i, keep=None):
    rights[x] = [0] * len(multiples[x])
    for place in multiples[x]:
        rights[x][place[1]] = i - place[0]
    rights[x] = tuple(rights[x])
    if not keep:
        del(multiples[x])
    return rights


def get_multi_total(lefts, rights, x):
    frequency = 0
    for left, right in zip(lefts[x], tuple(rights[x])):
        frequency += left * right
    for i in range(1, len(lefts[x])):
        frequency -= lefts[x][i - 1] * rights[x][i]
    total = x * frequency
    del(rights[x])
    del(lefts[x])
    return total


def do_the_thing(a):
    total = 0
    value, position = [], []
    rights, lefts, multiples = {}, {}, {}
    for i, x in enumerate(a):
        if not value:
            value.append(x)
            position.append(i)
            get_left(lefts, x, i + 1)
        elif x < value[-1]:
            get_left(lefts, x, i - position[-1])
            value.append(x)
            position.append(i)
        elif x == value[-1]:
            temp_pos = position.pop()
            is_multiple(multiples, x, i, temp_pos)
            if position:
                get_left(lefts, x, i - position[-1])
            else:
                get_left(lefts, x, i + 1)
            position.append(i)
        elif x > value[-1]:
            while value and x >= value[-1]:
                temp_value = value.pop()
                temp_pos = position.pop()
                if x == temp_value:
                    is_multiple(multiples, x, i, temp_pos)
                    if not value:
                        get_multi_right(rights, multiples, temp_value, i + 1, keep=True)
                else:
                    if multiples.get(temp_value):
                        get_multi_right(rights, multiples, temp_value, i)
                        total += get_multi_total(lefts, rights, temp_value)
                    else:
                        get_right(rights, temp_value, i - temp_pos)
                        total += get_total(lefts, rights, temp_value)
            if value:
                get_left(lefts, x, i - position[-1])
            else:
                get_left(lefts, x, i + 1)
            value.append(x)
            position.append(i)
    while value:
        temp_value = value.pop()
        temp_pos = position.pop()
        if not multiples.get(temp_value):
            get_right(rights, temp_value, len(a) - temp_pos)
        if multiples.get(temp_value):
            get_multi_right(rights, multiples, temp_value, len(a))
            total += get_multi_total(lefts, rights, temp_value)
        else:
            total += get_total(lefts, rights, temp_value)
    return total


a = [1,2,4,3]

print(do_the_thing(a))
