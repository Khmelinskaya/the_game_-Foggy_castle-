#!/usr/bin/python3

import generator
import msg

LIVES = 2 # количество попыток для выбора предмета

def print_bye_bye():
    print(msg.BYE)

def view_room(room):
    if room.item_id is not None:
        description_ind = generator.item_ind(room.item_id)
        print(room.descriptions_with_items[description_ind])
    else:
        print(room.empty_room_description)

def list_items(items):
    for i in range(0, len(items)):
        print("  * {} {}".format(i+1, items[i]))


def main_loop(items, rooms):
    global LIVES
    current_room = rooms[0]
    print(msg.ITEMS_TO_SEARCH)
    for item in items:
        print("  * ", item)
    print()

    while 1:
        if LIVES == 0:
            print(msg.GAME_OVER)
            exit(0)

        if len(items) == 0:
            print(msg.WIN)
            exit(0)

        print(msg.LIVES_LEFT.format(LIVES))
        view_room(current_room)
        print(msg.TO_MOVE)
        for i in range(1, len(current_room.links)+1):
            print("  * {} {}".format(i, current_room.links[i-1].title))

        print(msg.PROMPT, "\n")
        cmd = input("> ")
        if cmd == "q":
            print_bye_bye()
            exit(0)

        num = int(cmd)
        if num == 0:
            list_items(items)
            item_num = int(input(msg.INPUT_ITEM_NUMBER))
            if item_num < 0 or item_num > len(items):
                print(msg.ITEM_NOT_EXISTS)
                LIVES = LIVES - 1
                continue
            elif items.index(current_room.item_id) == item_num - 1:
                print(msg.ITEM_FOUND.format(current_room.item_id))
                current_room.remove_item()
                del items[item_num - 1]
                continue
            else:
                print(msg.ITEM_NOT_FOUND)
                LIVES = LIVES - 1
                continue
        else:
            if num in range(1, len(current_room.links)+1):
                current_room = current_room.links[num-1]


if __name__ == "__main__":
    generator.check_data() # проверяем что данные консистентны
    items = generator.pick_items()
    labyrinth_rooms = generator.pick_rooms_for_items(items)
    generator.link_labyrinth(labyrinth_rooms)
    print(msg.INTRO_MESSAGE)

    main_loop(items, labyrinth_rooms)

