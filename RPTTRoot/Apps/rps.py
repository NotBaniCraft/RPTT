import random
def rpsgame():
    first = True
    while True:
        if first: print("R = Rock; P = Paper; S = Scissors; E to exit"); first = False
        choice = input("Enter what you would like to choose: ")
        randintchoice = random.randint(1, 3)
        if randintchoice == 1: 
            randchoice = "R"
            print("The computer chose rock.")
        elif randintchoice == 2:
            randchoice = "P"
            print("The computer chose paper.")
        elif randintchoice == 3:
            randchoice = "S"
            print("The computer chose scissors.")
        if randchoice == choice:
            print("The game was a tie.")
        elif randchoice == "R" and choice == "P":
            print("You won!")
        elif randchoice == "R" and choice == "S":
            print("The computer won.")
        elif randchoice == "P" and choice == "R":
            print("The computer won.")
        elif randchoice == "P" and choice == "S":
            print("You won!")
        elif randchoice == "S" and choice == "R":
            print("You won!")
        elif randchoice == "S" and choice == "P":
            print("The computer won.")

rpsgame()