print(open('game_instructions.txt', 'r').read())
map_text = open('map.txt', 'r').read()
list_commands = open('commands.txt', 'r').read()

ghost_convo = ''


player = {
    'inventory': [],
    'inventory_room': 5,
    'location': 'foyer',
    'is_fighting': False,
    'health': 50,
    'attack': 10,
}

rooms = {
    'foyer': {
        'description': 'Starting area for the adventure.',
        'exits': ['parlor', 'library']
    },
    'parlor': {
        'description': 'A room with several exciting items. Also has a piano for entertaining guests.\nThere might be some interesting items around here.',
        'items': [
            {
                'name': 'Damaged Amulet',
                'description': 'An amulet that is damaged.',
            },
            {
                'name': 'Piano',
                'description': 'How are you able to carry a piano with you?',
            }
        ],
        'exits': ['foyer', 'kitchen']
    },
    'library': {
        'description': 'A room with many books to read for both entertainment and learning. You see a ghost that wants to talk.',
        'conversation': 'library-ghost-convo.txt',
        'items': [
            {
                'name': 'book',
                'description': 'This doesn\'t seem to have much use. You can maybe read it sometime when you study.',
            },
            {
                'name': 'novel',
                'description': 'This doesn\'t seem to have much use. You can maybe read it sometime.',
            }
        ],
        'exits': ['foyer', 'kitchen']
    },
    'kitchen': {
        'description': 'An area for making, baking, and preparing meals.',
        'items': [
            {
                'name': 'knife',
                'description': 'A knife that can help you protect yourself',
                'attack': 20,
            },
            {
                'name': 'sandwich',
                'description': 'A sandwich that can make a great meal',
                'heal': 5,
            }
        ],
        'exits': ['parlor', 'library', 'pantry']
    },
    'pantry': {
        'description': 'A room for keeping ingredients for the kitchen. You see a large rat in this room.',
        'monsters': [
            {
                'name': 'rat',
                'health': 10,
                'attack': 1,
                'status': 'awake',
            }
        ],
        'exits': ['kitchen']
    },
}


def add_item_to_inventory(item, items_list, player):
    if len(player['inventory']) < player['inventory_room']:
        player['inventory'].append(item)
    else:
        print('Cannot take any more items. Inventory is full!')
        return True
    return False


while True:
    print('\nYou are currently in the ' + player['location'] + '.')
    print(rooms[player['location']]['description'] + '\n')
    user_command = input(list_commands)
    print('\n')

    if user_command.lower() == 'map':
        print(map_text)

    elif user_command.lower() == 'inventory':
        if len(player['inventory']) > 0:
            item_names = []
            for item in player['inventory']:
                item_names.append(item['name'])
            print(item_names)
        else:
            print('No items in inventory')

    elif user_command.lower() == 'conversation':
        if ghost_convo != '':
            print('This was the conversation you had with the ghost:')
            print(ghost_convo)

        elif 'conversation' in rooms[player['location']]:
            with open(rooms[player['location']]['conversation'], 'r+') as my_file:
                convo_array = my_file.readlines()

            user_convo = ''
            print(convo_array[0])
            ghost_convo += convo_array[0]
            while user_convo != 'stop':
                user_convo = input('Adventurer: ')
                ghost_convo += user_convo + '\n'
                print(convo_array[1])
                ghost_convo += convo_array[1] + '\n'

        else: 
            print('Nothing to talk to in here.')

    elif user_command.lower() == 'take all items':
        if 'items' in rooms[player['location']] and len(rooms[player['location']]['items']) > 0:
            taken_items = []
            inventory_full = False
            while len(rooms[player['location']]['items']) > 0 and inventory_full == False:
                item = rooms[player['location']]['items'][0]
                inventory_full = add_item_to_inventory(item, rooms[player['location']]['items'], player)
                if inventory_full == False:
                    taken_items.append(item['name'])
                    rooms[player['location']]['items'].remove(item)
                
            print('Took: ' + str(taken_items))
        else: 
            print('No items to take.')
        
    elif user_command.lower() == 'items':
        if 'items' in rooms[player['location']] and len(rooms[player['location']]['items']) > 0:
            all_items = []
            for items in rooms[player['location']]['items']:
                all_items.append(items['name'])
            print(all_items)
        else: 
            print('No items to take.')

    elif user_command.lower() == 'fight':
        if 'monsters' in rooms[player['location']]:
            for monster in rooms[player['location']]['monsters']:
                while (monster['health'] > 0 or monster['status'] !='sleep') and player['health'] > 0:
                    print('You must use hypnosis and get the monsters health to 0 to win.\n')
                    print('\nName: ' + str(monster['name']))
                    print('Health: ' + str(monster['health']))
                    print('Status: ' + monster['status'])
                    print('\nYour Health: ' + str(player['health']))
                    attack_command = input("\nEnter a command like 'karate-chop', 'hypnosis', 'inventory', or 'use [item]': ")

                    if attack_command.lower() == 'karate-chop':
                        monster['health'] -= player['attack']
                    
                    elif attack_command.lower() == 'inventory':
                        if len(player['inventory']) > 0:
                            item_names = []
                            for item in player['inventory']:
                                item_names.append(item['name'])
                            print(item_names)
                        else:
                            print('No items in inventory')

                    else:
                        attack_command_split = attack_command.lower().split()

                        if attack_command_split[0] == 'use' and len(attack_command_split) < 3:
                            for item in player['inventory']:
                                if attack_command_split[1] in item['name']:
                                    if 'attack' in item:
                                        monster['health'] -= item['attack']
                                    if 'heal' in item:
                                        player['health'] += item['heal']
                                    if 'attack' in item or 'heal' in item:
                                        player['inventory'].remove(item)
                                    else:
                                        print('Cannot use that item')
                        
                        elif attack_command_split[0] == 'hypnosis':
                            monster['status'] = 'sleep'
                        
                        else:
                            print('Command not recognized!')

                    if monster['health'] > 0 and monster['status'] != 'sleep':
                        player['health'] -= monster['attack']
                
                if player['health'] < 1:
                    print('You died. Game Over!')
                    break
                else:
                    print('You beat all of the monsters!')
        else:
            print('No monsters to attack in here')

    elif user_command.lower() == 'quit':
        print('Thanks for playing this short text adventure!')
        break

    else:
        command = user_command.lower().split()

        if command[0] == 'enter' and len(command) < 3:
            if command[1] in rooms[player['location']]['exits']:
                player['location'] = command[1]
                print('You have moved to ' + command[1])
            else:
                print('Cannot enter that room from this room!')

        elif command[0] == 'take' and len(command) < 3:
            if 'items' in rooms[player['location']]:
                for item in rooms[player['location']]['items']:
                    # TODO: this doesn't work correctly
                    if item['name'] == command[1]:
                        item_name = item['name']
                        add_item_to_inventory(item, rooms[player['location']]['items'], player)
                        rooms[player['location']]['items'].remove(item)
                        print('Took: ' + item_name)
            else: 
                print('No items to take.')

        else:
            print('Command not recognized. Try again!')