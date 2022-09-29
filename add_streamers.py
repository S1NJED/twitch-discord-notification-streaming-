import json, os

def create_file():
    path = os.path.exists("streamers")
    if not path:
        with open('streamers', 'w') as file:
            file.write(json.dumps([]))

def add_streamer(streamer):
    create_file()
    with open('streamers', 'r') as file:
        data = json.loads(file.read())
    if streamer in data:
        print(f"{streamer} is already in the lists.")
        return
        
    with open('streamers', 'w') as file:
        data.append(streamer)
        file.write(json.dumps(data))
    print(f"{streamer} was added to the list.\nCurrent streamers: {', '.join(data)}")

def delete_streamer(streamer):
    create_file()
    with open('streamers', 'r') as file:
        data = json.loads(file.read())
    if not streamer in data:
        print(f"{streamer} is not in the list.")
        return
        
    with open('streamers', 'w') as file:
        data.remove(streamer)
        file.write(json.dumps(data))

def list_streamer():
    create_file()
    with open('streamers', 'r') as file:
        data = ", ".join(json.loads(file.read()))
        if len(data) == 0:
            print('There is no streamers in the list.')
        else:
            print(f"Streamers list: {data}")

def main():
    print("[1] Add a streamer.\n[2] Delete a streamer\n[3] Show the current streamers in the list\n")
    while True:
        try:
            option = int(input('\n-->'))
        except:
            os.system('cls')
            continue
        
        if not option in [1, 2, 3]:
            print(f"You must type 1, 2 or 3, not {option}")
        else:
            if option == 1:
                streamer = str(input("[ADD] Enter a streamer name: "))
                add_streamer(streamer)
            elif option == 2:
                streamer = str(input("[DEL] Enter a streamer name "))
                delete_streamer(streamer)
            elif option == 3:
                list_streamer()
        
if __name__ == '__main__':
    main()