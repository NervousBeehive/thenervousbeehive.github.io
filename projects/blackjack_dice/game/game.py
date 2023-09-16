
import random
import colorama
import os

# Initialize colorama so colors show up correctly in terminal
colorama.init(convert=True)

# Glorified input function that checks input against a list only allowing whitelisted inputs to be accepted
def validated_input(question, whitelist):
    answer = input(question)
    while True:
        if answer in whitelist:
            return answer
        else:
            print("Incorrect input please try again...")
            answer = input(question).lower()

def intro():
    # Intro to the game explaining rules and asking if the player would like to play singleplayer or multiplayer
    print("")
    print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
    print("    Welcome to Blackjack Dice!")
    print('''
                   (( _______      
         _______     /\O    O\     
        /O     /\   /  \      \    
       /   O  /O \ / O  \O____O\ ))
    ((/_____O/    \\    /O     /   
      \O    O\    / \  /   O  /    
       \O    O\ O/   \/_____O/     
        \O____O\/ ))          ))   
      ((                           
      ''')
    print("------------------------------------")
    print("Rules:")
    print("1. Both players start with a deck of 10 cards with random values ranging from 1 - 10.")
    print("2. Both players take turns drawing cards trying to get as close to 21.")
    print("3. Although if you go over 21 you automatically lose and the other player wins.")
    print("4. However if both players pass and neither go over 21 whoever has the highest number wins.")
    print("------------------------------------")

    gamemode = validated_input("What gamemode would you like to play ((s)ingleplayer/(m)ultiplayer/(sim)ulation): ", ["s", "m", "sim"])
    if gamemode == "m":
        multiplayer()
    elif gamemode == "s":
        singleplayer()
    else:
        simulation()

def singleplayer():
    # Initialize both player and cpu decks, scores and pass state
    player_deck = []
    for i in range(10):
        player_deck.append(random.randint(1, 10))
    player_score = 0
    player_passed = False

    cpu_deck = []
    for i in range(10):
        cpu_deck.append(random.randint(1, 10))
    cpu_score = 0
    cpu_passed = False

    # Asking player for their username
    player_username = input("Please enter your username: ")
    print("------------------------------------")

    # Main game loop
    while True:
        # Checking if Player 1 hasn't passed before asking if they would like to roll or pass
        if not player_passed:
            print(colorama.Fore.LIGHTGREEN_EX + player_username + "'s turn!")
            print(player_username + " currently has " + str(player_score) + " score.")
            print(player_username + "'s current deck = " + str(player_deck))
            choice = validated_input("What would you like to do (roll/pass): ", ["roll", "pass"])
            if choice == "roll":
                print("")
                # Picking random number to use as index based on the lenght of deck. Index starts a t 0 in lists therefore you must take one of the lenght
                random_index = random.randint(0, len(player_deck) - 1)
                random_number = player_deck[random_index]
                # pop() function removes number from deck after it has been rolled once
                player_deck.pop(random_index)
                print(player_username + " rolled a " + str(random_number) + ".")
                player_score += random_number
                # Making sure players score is not over 21 as that would cause them to lose
                if player_score > 21:
                    print(player_username + "'s score is greater than 21. Score set to 0 and automatically passed.")
                    print("------------------------------------")
                    player_score = 0
                    player_passed = True
                else:
                    print(player_username + "'s new total is " + str(player_score) + ".")
                    print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
            else:
                # If player chooses to pass player_passed will be set to True, so they aren't asked if they would like to roll or pass again
                print(player_username + " has passed.")
                print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
                player_passed = True

        # Checking if Player 1 hasn't passed before asking if they would like to roll or pass
        if not cpu_passed:
            print(colorama.Fore.LIGHTBLUE_EX + "CPU's turn!")
            print("CPU currently has " + str(cpu_score) + " score.")
            print("CPU's current deck = " + str(cpu_deck))
            # CPU AI
            # Firstly CPU checks all numbers in deck and sees if drawing them would put their score over 21
            # If the number will but them over 21, 1 is added to risk if it won't put them over 21 1 is added to safe
            risk = 0
            safe = 0
            for i in cpu_deck:
                if cpu_score + i > 21:
                    risk += 1
                else:
                    safe += 1
            # Deciding whether to pass or roll
            # If player has passed and cpu's score is higher than players cpu will also pass
            if (player_passed == True) and cpu_score > player_score:
                choice = "pass"
            # If the percentage of safe numbers tact could be drawn is over 50% cpu will choose to roll
            elif (safe + risk / 100) * safe > 50:
                choice = "roll"
            # And even if the percentage of risky numbers is more than safe numbers if the player has passed and has a higher score than the cpu,
            # the cpu will choose to roll anyway as its better than just accepting defeat
            elif (player_passed == True) and cpu_score < player_score:
                choice = "roll"
            else:
                choice = "pass"
            print("CPU has chose to " + choice)
            print("")
            if choice == "roll":
                print("")
                random_index = random.randint(0, len(cpu_deck) - 1)
                random_number = cpu_deck[random_index]
                # pop() function removes number from deck after it has been rolled once
                cpu_deck.pop(random_index)
                print("CPU rolled a " + str(random_number) + ".")
                cpu_score += random_number
                # Making sure cpus score is not over 21 as that would cause them to lose
                if cpu_score > 21:
                    print("CPU's score is greater than 21. Score set to 0 and automatically passed.")
                    print("------------------------------------")
                    cpu_score = 0
                    cpu_passed = True
                else:
                    print("CPU's new total is " + str(cpu_score) + ".")
                    print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
            else:
                print("CPU has passed.")
                print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
                cpu_passed = True

        # Once both player and cpu have passed display both players scores before calculating who wins
        else:
            print(colorama.Fore.LIGHTWHITE_EX + player_username + "'s final score equals " + str(player_score) + ".")
            print("CPU's final score equals " + str(cpu_score) + ".")
            print("")

            if player_score > cpu_score:
                print(player_username + " wins by " + str(player_score - cpu_score) + " points!")
            elif player_score < cpu_score:
                print("CPU wins by " + str(cpu_score - player_score) + " points!")
            else:
                print("Both player and cpu scored the same amount of points Draw!")

            print("------------------------------------")
            print("")
            # Asking player if they would like to play again
            choice = validated_input("Would you like to play again (yes/no): ", ["yes", "no"])
            if choice == "yes":
                os.system("cls")
                intro()
            else:
                print("Thanks for playing. Goodbye!")
                exit()

def multiplayer():
    # Initialize both players decks, scores and pass state
    player1_deck = []
    for i in range(10):
        player1_deck.append(random.randint(1, 10))
    player1_score = 0
    player1_passed = False

    player2_deck = []
    for i in range(10):
        player2_deck.append(random.randint(1, 10))
    player2_score = 0
    player2_passed = False

    # Asking players for their usernames
    player1_username = input("Please enter Player 1's username: ")
    player2_username = input("Please enter Player 2's username: ")
    print("------------------------------------")
    print("")

    # Main game loop
    while True:
        # Checking if Player 1 hasn't passed before asking if they would like to roll or pass
        if not player1_passed:
            print(colorama.Fore.LIGHTGREEN_EX + player1_username + "'s turn!")
            print(player1_username + " currently has " + str(player1_score) + " score.")
            print(player1_username + "'s current deck = " + str(player1_deck))
            choice = validated_input("What would you like to do (roll/pass): ", ["roll", "pass"])
            if choice == "roll":
                print("")
                # Picking random number to use as index based on the lenght of deck. Index starts a t 0 in lists therefore you must take one of the lenght
                random_index = random.randint(0, len(player1_deck) - 1)
                random_number = player1_deck[random_index]
                # pop() function removes number from deck after it has been rolled once
                player1_deck.pop(random_index)
                print(player1_username + " rolled a " + str(random_number) + ".")
                player1_score += random_number
                # Making sure players score is not over 21 as that would cause them to lose
                if player1_score > 21:
                    print(player1_username + "'s score is greater than 21. Score set to 0 and automatically passed.")
                    print("------------------------------------")
                    player1_score = 0
                    player1_passed = True
                else:
                    print(player1_username + "'s new total is " + str(player1_score) + ".")
                    print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
            else:
                # If player chooses to pass player1_passed will be set to True, so they aren't asked if they would like to roll or pass again
                print(player1_username + " has passed.")
                print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
                player1_passed = True

        # Basically the same thing as for Player one again for Player 2
        if not player2_passed:
            print(colorama.Fore.LIGHTBLUE_EX + player2_username + "'s turn!")
            print(player2_username + " currently has " + str(player2_score) + " score.")
            print(player2_username + "'s current deck = " + str(player2_deck))
            choice = validated_input("What would you like to do (roll/pass): ", ["roll", "pass"])
            if choice == "roll":
                print("")
                random_index = random.randint(0, len(player2_deck) - 1)
                random_number = player2_deck[random_index]
                player2_deck.pop(random_index)
                print(player2_username + " rolled a " + str(random_number) + ".")
                player2_score += random_number
                if player2_score > 21:
                    print(player2_username + "'s score is greater than 21. Score set to 0 and automatically passed.")
                    print("------------------------------------")
                    player2_score = 0
                    player2_passed = True
                else:
                    print(player2_username + "'s new total is " + str(player2_score) + ".")
                    print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
            else:
                print(player2_username + " has passed.")
                print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
                player2_passed = True

        # Once both players have passed display both players scores before calculating who wins
        else:
            print(colorama.Fore.LIGHTWHITE_EX + player1_username + "'s final score equals " + str(player1_score) + ".")
            print(player2_username + "'s final score equals " + str(player2_score) + ".")
            print("")

            if player1_score > player2_score:
                print(player1_username + " wins by " + str(player1_score - player2_score) + " points!")
            elif player1_score < player2_score:
                print(player2_username + " wins by " + str(player2_score - player1_score) + " points!")
            else:
                print("Both players scored the same amount of points Draw!")

            print("------------------------------------")
            print("")
            # Asking player if they would like to play again
            choice = validated_input("Would you like to play again (yes/no): ", ["yes", "no"])
            if choice == "yes":
                os.system("cls")
                intro()
            else:
                print("Thanks for playing. Goodbye!")
                exit()

def simulation():
    # Initialize both player and cpu decks, scores and pass state
    cpu1_deck = []
    for i in range(10):
        cpu1_deck.append(random.randint(1, 10))
    cpu1_score = 0
    cpu1_passed = False

    cpu2_deck = []
    for i in range(10):
        cpu2_deck.append(random.randint(1, 10))
    cpu2_score = 0
    cpu2_passed = False

    # Main game loop
    while True:
        if not cpu1_passed:
            print(colorama.Fore.LIGHTGREEN_EX + "CPU 1's turn!")
            print("CPU 1 currently has " + str(cpu1_score) + " score.")
            print("CPU 1's current deck = " + str(cpu1_deck))
            # CPU AI
            # Firstly CPU checks all numbers in deck and sees if drawing them would put their score over 21
            # If the number will but them over 21, 1 is added to risk if it won't put them over 21 1 is added to safe
            risk = 0
            safe = 0
            for i in cpu1_deck:
                if cpu1_score + i > 21:
                    risk += 1
                else:
                    safe += 1
            # Deciding whether to pass or roll
            # If player has passed and cpu's score is higher than players cpu will also pass
            if (cpu2_passed == True) and cpu1_score > cpu2_score:
                choice = "pass"
            # If the percentage of safe numbers tact could be drawn is over 50% cpu will choose to roll
            elif (safe + risk / 100) * safe > 50:
                choice = "roll"
            # And even if the percentage of risky numbers is more than safe numbers if the player has passed and has a higher score than the cpu,
            # the cpu will choose to roll anyway as it's better than just accepting defeat
            elif (cpu2_passed == True) and cpu1_score < cpu2_score:
                choice = "roll"
            else:
                choice = "pass"
            print("CPU 1 has chose to " + choice)
            print("")
            if choice == "roll":
                print("")
                random_index = random.randint(0, len(cpu1_deck) - 1)
                random_number = cpu1_deck[random_index]
                # pop() function removes number from deck after it has been rolled once
                cpu1_deck.pop(random_index)
                print("CPU 1 rolled a " + str(random_number) + ".")
                cpu1_score += random_number
                # Making sure cpus score is not over 21 as that would cause them to lose
                if cpu1_score > 21:
                    print("CPU 1's score is greater than 21. Score set to 0 and automatically passed.")
                    print("------------------------------------")
                    cpu1_score = 0
                    cpu1_passed = True
                else:
                    print("CPU 1's new total is " + str(cpu1_score) + ".")
                    print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
            else:
                print("CPU 1 has passed.")
                print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
                cpu1_passed = True

        if not cpu2_passed:
            print(colorama.Fore.LIGHTBLUE_EX + "CPU 2's turn!")
            print("CPU 2 currently has " + str(cpu2_score) + " score.")
            print("CPU 2's current deck = " + str(cpu2_deck))
            # CPU AI
            # Firstly CPU checks all numbers in deck and sees if drawing them would put their score over 21
            # If the number will but them over 21, 1 is added to risk if it won't put them over 21 1 is added to safe
            risk = 0
            safe = 0
            for i in cpu2_deck:
                if cpu2_score + i > 21:
                    risk += 1
                else:
                    safe += 1
            # Deciding whether to pass or roll
            # If player has passed and cpu's score is higher than players cpu will also pass
            if (cpu1_passed == True) and cpu2_score > cpu1_score:
                choice = "pass"
            # If the percentage of safe numbers tact could be drawn is over 50% cpu will choose to roll
            elif (safe + risk / 100) * safe > 50:
                choice = "roll"
            # And even if the percentage of risky numbers is more than safe numbers if the player has passed and has a higher score than the cpu,
            # the cpu will choose to roll anyway as its better than just accepting defeat
            elif (cpu1_passed == True) and cpu2_score < cpu1_score:
                choice = "roll"
            else:
                choice = "pass"
            print("CPU 2 has chose to " + choice)
            print("")
            if choice == "roll":
                print("")
                random_index = random.randint(0, len(cpu2_deck) - 1)
                random_number = cpu2_deck[random_index]
                # pop() function removes number from deck after it has been rolled once
                cpu2_deck.pop(random_index)
                print("CPU 2 rolled a " + str(random_number) + ".")
                cpu2_score += random_number
                # Making sure cpus score is not over 21 as that would cause them to lose
                if cpu2_score > 21:
                    print("CPU 2's score is greater than 21. Score set to 0 and automatically passed.")
                    print("------------------------------------")
                    cpu2_score = 0
                    cpu2_passed = True
                else:
                    print("CPU 2's new total is " + str(cpu2_score) + ".")
                    print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
            else:
                print("CPU 2 has passed.")
                print(colorama.Fore.LIGHTWHITE_EX + "------------------------------------")
                cpu2_passed = True

        # Once both player and cpu have passed display both players scores before calculating who wins
        else:
            print(colorama.Fore.LIGHTWHITE_EX + "CPu 1's final score equals " + str(cpu1_score) + ".")
            print("CPU 2's final score equals " + str(cpu2_score) + ".")
            print("")

            if cpu1_score > cpu2_score:
                print("CPU 1 wins by " + str(cpu1_score - cpu2_score) + " points!")
            elif cpu1_score < cpu2_score:
                print("CPU 2 wins by " + str(cpu2_score - cpu1_score) + " points!")
            else:
                print("Both cpu's scored the same amount of points Draw!")

            print("------------------------------------")
            print("")
            # Asking player if they would like to play again
            choice = validated_input("Would you like to play again (yes/no): ", ["yes", "no"])
            if choice == "yes":
                os.system("cls")
                intro()
            else:
                print("Thanks for playing. Goodbye!")
                exit()

intro()