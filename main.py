from dice_game import DiceGame

def main():
    game = DiceGame()
    while True:
        choice = game.menu()
        if choice == "1":
            game.register()
        elif choice == "2":
            game.login()
            while game.current_user:
                game.logged_in_menu()
        elif choice == "3":
            break
        elif choice == "":
            print("No input provided. Please enter a valid choice.")
        else:
            print("ERROR, INVALID RESPONSE")

if __name__ == "__main__":
    main()
