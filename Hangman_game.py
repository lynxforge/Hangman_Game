import random
import socket

def get_random_word():
    words = [
        "apple", "grape", "plane", "tiger", "house", "river",
        "brick", "snake", "chair", "smile", "bread", "light",
        "stone", "cloud", "music", "beach", "train", "grass"
    ]
    return random.choice(words)

stages = ['''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', '''
  +---+
  |   |
      |
      |
      |
      |
=========
''']

#============ Mode Selection ===================

print("1. Single Player")
print("2. Multiplayer (Same Wifi)")
mode = input("Choose mode: ")

# ================= MULTIPLAYER =================

def multiplayer_host(chosen_word):
    server = socket.socket()
    server.bind(("", 5555))
    server.listen(1)

    print("Waiting for player to join...")
    conn, addr = server.accept()
    print("Player joined: ", addr)

    lives = 6
    correct_letters = []
    guessed_letters = []
    turn = "HOST"

    while True:
        display = "".join([c if c in correct_letters else "_" for c in chosen_word])
        conn.send(f"STATE|{display}|{lives}".encode())

        print("\nWord:", display)
        print("Lives:", lives)
        print(stages[lives])

        if "_" not in display:
            conn.send(b"GAMEOVER|HOST")
            print("You win!")
            break

        if lives == 0:
            conn.send(b"GAMEOVER|JOIN")
            print("You lose!")
            break

        if turn == "HOST":
            guess = input("Your turn (guess): ").lower()
            turn = "JOIN"
        else:
            conn.send(b"YOURTURN")
            guess = conn.recv(1024).decode().lower()
            turn = "HOST"

        if guess in guessed_letters:
            continue

        guessed_letters.append(guess)

        if guess in chosen_word:
            correct_letters.append(guess)
        else:
            lives -= 1

    conn.close()
    server.close()

def multiplayer_join():
    ip = input("Enter host IP address: ")
    client = socket.socket()
    client.connect((ip, 5555))

    while True:
        data = client.recv(1024).decode()

        if data.startswith("STATE"):
            _, display, lives = data.split("|")
            lives = int(lives)

            print("\nWord:", display)
            print("Lives:", lives)
            print(stages[lives])

        elif data == "YOURTURN":
            guess = input("Your turn (guess): ").lower()
            client.send(guess.encode())

        elif data.startswith("GAMEOVER"):
            winner = data.split("|")[1]
            if winner == "JOIN":
                print("You win!")
            else:
                print("You lose!")
            break

    client.close()

# ============== MULTIPLAYER ENTRY ==============

if mode == "2":
    choice = input("1.Host game\n2.Join game\nChoose: ")

    if choice == "1":
        multiplayer_host(get_random_word())
    else:
        multiplayer_join()

    exit()

# TODO-1: - Create a variable  called 'lives' to keep  track of the number of lives left.
# Set 'lives' to equal 6.

lives = 6
chosen_word = get_random_word()
correct_letters = []
guessed_letters = []

print("_" * len(chosen_word))

while True:
    guess = input("Guess a letter: ").lower()

    if guess in guessed_letters:
        print("Already guessed!")
        continue

    guessed_letters.append(guess)

    if guess in chosen_word:
        correct_letters.append(guess)
    else:
        lives -= 1

    display = "".join([c if c in correct_letters else "_" for c in chosen_word])
    print(display)

    # TODO-2: - If guess is not a letter in the chosen_word, Then reduce 'lives' by 1.
    # If lives goes down to 0 then the game should stop and it should print "You lose." 

    print(stages[lives])

    if "_" not in display:
        print("You win!")
        break

    if lives == 0:
        print("GAME OVER")
        break
