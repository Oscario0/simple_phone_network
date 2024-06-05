import json

network = {
    "switchboards": {},
    "phones": {}
}

def switch_add(area_code):
    if area_code not in network["switchboards"]:
        network["switchboards"][area_code] = {"connected_switchboards": set(), "phones": set()}

def switch_connect(area_code1, area_code2):
    if area_code1 in network["switchboards"] and area_code2 in network["switchboards"]:
        network["switchboards"][area_code1]["connected_switchboards"].add(area_code2)
        network["switchboards"][area_code2]["connected_switchboards"].add(area_code1)

def phone_add(phone_number):
    if phone_format(phone_number):
        area_code, num_part_1, num_part_2 = map(int, phone_number.split('-'))
        if area_code in network["switchboards"]:
            full_number = f"{num_part_1:03d}-{num_part_2:03d}"
            network["phones"][full_number] = {"connected_to": None}
            network["switchboards"][area_code]["phones"].add(full_number)
            return full_number
    print("Invalid phone number format.")
    return None

def phone_format(phone_number):
    parts = phone_number.split('-')
    return len(parts) == 3 and all(part.isdigit() for part in parts)

def start_call(phone_number1, phone_number2):
    if phone_number1 in network["phones"] and phone_number2 in network["phones"]:
        if network["phones"][phone_number1]["connected_to"] is None and network["phones"][phone_number2]["connected_to"] is None:
            if can_connect(phone_number1, phone_number2):
                network["phones"][phone_number1]["connected_to"] = phone_number2
                network["phones"][phone_number2]["connected_to"] = phone_number1
                print(f"{phone_number1} and {phone_number2} are now connected.")
            else:
                print(f"{phone_number1} and {phone_number2} were not connected.")
        else:
            print(f"One of the phones ({phone_number1} or {phone_number2}) is already in a call.")
    else:
        print(f"Invalid phone numbers: {phone_number1}, {phone_number2}.")

def can_connect(phone_number1, phone_number2):
    return True

def display():
    for area_code, switchboard in network["switchboards"].items():
        print(f"Switchboard with area code: {area_code}")
        print("    Trunk lines are:")
        for connected_code in switchboard["connected_switchboards"]:
            print(f"    \tTrunk line connection to: {connected_code}")
        print("    Local phone numbers are:")
        for phone_number in switchboard["phones"]:
            status = "connected to " + network["phones"][phone_number]["connected_to"] if network["phones"][phone_number]["connected_to"] else "not in use"
            print(f"    \tPhone with number: {area_code}-{phone_number} is {status}.")
        print()
    
    
    print("          \nNOTE: When starting a call, enter phone numbers without area code in the format 000-0000.")


def network_save(filename):
    with open(filename, 'w') as file:
        serializable_switchboards = {
            area: {
                'connected_switchboards': list(data['connected_switchboards']),
                'phones': list(data['phones'])
            } for area, data in network["switchboards"].items()
        }
        json.dump(serializable_switchboards, file)

def network_load(filename):
 
    network["switchboards"] = {}
    network["phones"] = {}

    with open(filename, 'r') as file:
        serializable_switchboards = json.load(file)
        for area, data in serializable_switchboards.items():
            switch_add(area)
            for connected_code in data['connected_switchboards']:
                switch_connect(area, connected_code)
            for phone_number in data['phones']:
                phone_add(f"{area}-{phone_number}")


while True:
    user_input = input("Enter command ('quit' to exit): ").strip()

    if user_input.lower() == 'quit':
        break

    parts = user_input.split()
    command = parts[0].lower()

    if command == 'switch-add':
        if len(parts) == 2:
            switch_add(int(parts[1]))
            print(f"Switchboard with area code {parts[1]} added.")
        else:
            print("Invalid syntax. Example: switch-add <area_code>")
    
    elif command == 'switch-connect':
        if len(parts) == 3:
            switch_connect(int(parts[1]), int(parts[2]))
            print(f"Switchboards {parts[1]} and {parts[2]} connected.")
        else:
            print("Invalid syntax. Example: switch-connect <area_code1> <area_code2>")
    
    elif command == 'phone-add':
        if len(parts) == 2:
            phone_number = phone_add(parts[1])
            if phone_number:
                print(f"Phone with number {parts[1]} added.")
        else:
            print("Invalid syntax. Example: phone-add <area_code>-<num_part_1>-<num_part_2>")
    
    elif command == 'start-call':
        if len(parts) == 3:
            start_call(parts[1], parts[2])
        else:
            print("Invalid syntax. Try again")
    
    elif command == 'display':
        display()
    
    elif command == 'network-save':
        if len(parts) == 2:
            network_save(parts[1])
            print(f"Network saved to {parts[1]}.")
        else:
            print("Invalid syntax. Example: network-save <filename>")
    
    elif command == 'network-load':
        if len(parts) == 2:
            network_load(parts[1])
            print(f"Network loaded from {parts[1]}.")
        else:
            print("Invalid syntax. Example: network-load <filename>")
    
    else:
        print("Invalid command. Please try again.")

network_save("network_data.txt")

network_load("network_data.txt")

display()
