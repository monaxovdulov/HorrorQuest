import random


class Room:
    def __init__(self, description, items, directions, puzzle):
        self.description = description
        self.items = items
        self.directions = directions
        self.puzzle = puzzle


house = {
    "гостиная": Room("Вы находитесь в гостиной. Здесь зловещая тишина.", ["диван", "телевизор"],
                     {"север": "кухня", "восток": "коридор"}, None),
    "кухня": Room("Вы находитесь на кухне. Все вокруг в беспорядке.", ["нож", "запертый ящик"], {"юг": "гостиная"},
                  "Ящик заперт числовым кодом."),
    "коридор": Room("Вы в длинном коридоре с множеством дверей. На стене висит картина.", ["картина"],
                    {"запад": "гостиная", "север": "спальня", "восток": "главная дверь"},
                    "Картина кажется подозрительной."),
    "спальня": Room("Вы находитесь в спальне. Здесь холодно.", [], {"юг": "коридор"}, None),
    "главная дверь": Room("Вы у главной двери. Она заперта.", [], {}, None)
}


def game():
    current_room = "гостиная"
    ghost_room = random.choice([room for room in house.keys() if room != "гостиная"])
    inventory = []
    code_found = False

    print(
        "Команды: 'идти [направление]', 'взять [предмет]', 'инвентарь', 'помощь', 'осмотреть [предмет]', 'использовать [предмет]'")

    while True:
        # Describe the room
        room = house[current_room]
        print(room.description)

        # List the items in the room
        if room.items:
            print("В комнате вы видите: " + ", ".join(room.items))

        # List the available directions
        print("Вы можете идти в следующих направлениях: " + ", ".join(room.directions.keys()))

        # Get the player's action
        action = input("Что вы хотите сделать? ").split()

        # Check for help command
        if action[0] == "помощь":
            print(
                "Команды: 'идти [направление]', 'взять [предмет]', 'инвентарь', 'помощь', 'осмотреть [предмет]', 'использовать [предмет]'")

        # Check inventory
        elif action[0] == "инвентарь":
            print("У вас есть: " + ", ".join(inventory))

        # Player wants to move
        elif action[0] == "идти":
            if action[1] in room.directions:
                if room.directions[action[1]] == ghost_room:
                    print("Призрачный ИИ находится в этой комнате! Вы не можете туда идти.")
                else:
                    current_room = room.directions[action[1]]
                    ghost_room = random.choice([room for room in house.keys() if room != current_room])
            else:
                print("Вы не можете идти в этом направлении. Попробуйте другое направление.")

        # Player wants to take an item
        elif action[0] == "взять":
            if action[1] in room.items:
                if action[1] == "запертый ящик" and not code_found:
                    print("Ящик заперт. Вам нужно найти код, чтобы его открыть.")
                else:
                    inventory.append(action[1])
                    room.items.remove(action[1])
                    print(f"Вы взяли {action[1]}")
            else:
                print("Здесь нет такого предмета. Попробуйте другой предмет.")

        # Player wants to examine an item
        elif action[0] == "осмотреть":
            if action[1] in room.items:
                if action[1] == "картина":
                    print("При ближайшем рассмотрении вы находите код, скрытый на картине: 1234")
                    code_found = True
                else:
                    print(f"Ничего необычного в {action[1]}.")
            else:
                print("Здесь нет такого предмета. Попробуйте другой предмет.")

        # Player wants to use an item
        elif action[0] == "использовать":
            if action[1] == "код" and code_found:
                if "запертый ящик" in inventory:
                    inventory.remove("запертый ящик")
                    inventory.append("ключ")
                    print("Вы использовали код, чтобы открыть ящик, и нашли внутри ключ!")
                else:
                    print("Сейчас вам не нужен код.")
            else:
                print("Вы не можете использовать это. Попробуйте другой предмет.")

        # Check if player has found the key to exit the house
        elif current_room == "главная дверь" and "ключ" in inventory:
            print("Вы нашли ключ и открыли главную дверь! Вы сбежали из дома и выиграли игру!")
            break
        else:
            print("Я не понимаю это действие. Попробуйте снова или используйте 'помощь' для доступных команд.")


if __name__ == "__main__":
    game()



"""
Игрок должен взаимодействовать с предметами в комнатах, 
решить головоломку, чтобы получить ключ, и, наконец, сбежать из дома, чтобы выиграть игру. 
При этом необходимо избегать призрачного ИИ, который перемещается между комнатами в случайном порядке.

"""
