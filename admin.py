import os
import random
import sys

sys.path.append(os.path.split(sys.path[0])[0])

client = TCPClient()
client.connect("localhost", 6317)


def main():
    # client.send_data(["update", None])
    print("1) Clear Data")
    print("2) Reset Users")
    print("3) Add User")
    print("8) Start Game")
    print("9) Exit")

    insert = 0
    while insert != 4:
        insert = input("Your choice")

        if insert == 1:
            client.send_data(["update", "clear all"])
        elif insert == 2:
            client.send_data(["update", "reset ids"])
        elif insert == 3:
            client.send_data(["update", "user joined", random.randint(0, 10000000)])
        elif insert == 8:
            client.send_data(["update", "start game"])
        elif insert == 9:
            sys.exit()


if __name__ == '__main__':
    main()
