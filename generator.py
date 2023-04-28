import random

import rooms

ROOMS_IN_LABYRINTH = 6 # количество комант из которых будет состоять лабиринг
ITEMS_IN_LABYRINTH = 2
MAX_EXTRA_LINKS_AMOUNT = 3 # все команты связанны со всеми, в данном параметре задается количество дополнительных связей

def fatal(msg):
    print("Ошибка! " + msg)
    exit(1)


def check_data():
    items_max_amount = len(rooms.ITEMS)

    if ITEMS_IN_LABYRINTH > ROOMS_IN_LABYRINTH:
        fatal("Количество вещей к поиску не может превышать количество комнат")

    if ITEMS_IN_LABYRINTH > items_max_amount:
        fatal("Заданное количество вещей не может превышать доступное количество вещей")

    for room in rooms.ROOMS:
        if len(room.descriptions_with_items) != items_max_amount:
            fatal("Для комнаты " + room.title + " задано не верное количество описаний с пердметами")


# случайно выбираем вещи для участия в игре
def pick_items():
    items = rooms.ITEMS.copy()
    picked_items = []
    for i in range(ITEMS_IN_LABYRINTH):
        item = pop_random_from(items)
        picked_items.append(item)

    return picked_items


def pick_rooms_for_items(items):
    rooms_cp = rooms.ROOMS.copy();
    items_cp = items.copy()
    picked_rooms = [];
    for item in items:
        room = None
        item_i = item_ind(item)
        while room is None:
            room_tmp = pick_random_from(rooms_cp);
            if room_tmp.descriptions_with_items[item_i] != "":
                rooms_cp.remove(room_tmp)
                room_tmp.put_item(item)
                room = room_tmp;
        picked_rooms.append(room)

    for i in range(ROOMS_IN_LABYRINTH - len(picked_rooms)):
        picked_rooms.append(pop_random_from(rooms_cp))

    return picked_rooms



def item_ind(item_id):
    return rooms.ITEMS.index(item_id)


# вынимает и возвращает случайный элемент из списка
def pop_random_from(l):
    return l.pop(random.randint(0, len(l) - 1))


# возращает случайный элемент списка
def pick_random_from(l):
    return l[random.randint(0, len(l) - 1)]


# возращает случайный элемент списка, кроме уже заданного
def pick_random_but_not_from(l, i):
    ind_to_avoid = l.index(i)
    return l[random_but_not(len(l), ind_to_avoid)]


# связываем команты между собой случайным образом
def link_labyrinth(rooms_to_link):
    for r1 in rooms_to_link:
        r2 = rooms_to_link[random_but_not(len(rooms_to_link), rooms_to_link.index(r1))]
        if r2 not in r1.links:
            link_two_rooms(r1, r2)

    for i in range(0, MAX_EXTRA_LINKS_AMOUNT):
        r1 = pick_random_from(rooms_to_link)
        r2 = pick_random_but_not_from(rooms_to_link, r1)
        if r2 not in r1.links:
            link_two_rooms(r1, r2)


# связывает две команты (связи в обе стороны. не направленные)
def link_two_rooms(r1, r2):
    r1.add_link(r2)
    r2.add_link(r1)


# возвращает случайное число из диапазона [0..n), за исключением not_n
def random_but_not(n, not_n):
    if not_n == 0:
        return random.randint(1, n-1);

    if not_n == n-1:
        return random.randint(0, n-2);

    if bool(random.getrandbits(1)):
        return random.randint(0, not_n-1)
    else:
        return random.randint(not_n+1, n-1)


