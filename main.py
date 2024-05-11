from dice_game import DiceGame

def main():
    game = DiceGame()
    while True:
        choice = game.menu()
        if choice == "1":
            game.register()
        elif choice == "2":
            game.login()
        elif choice == "3":
            game.logout()
            break
        else:
            print("ERROR, Invalid response")

if __name__ == "__main__":
    main()
