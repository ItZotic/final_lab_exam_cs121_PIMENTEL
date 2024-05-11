import os
import random

from user_manager import UserManager
from score import Score
from user import User

class DiceGame:
    def __init__(self):
        self.user_manager = UserManager()
        self.scores = []
        self.current_user = None
        self.load_score()

    def load_score(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        scores_file = os.path.join('data', 'rankings.txt')
        if os.path.exists(scores_file):
            with open(scores_file, 'r') as file:
                for line in file:
                    username, game_id, points, wins = line.strip().split(',')
                    score = Score(username, game_id)
                    score.points = int(points)
                    score.wins = int(wins)
                    self.scores.append(score)

    def save_score(self):
        scores_file = os.path.join('data', 'rankings.txt')
        with open(scores_file, 'w') as file:
            for score in self.scores:
                file.write(f"{score.username},{score.game_id},{score.points},{score.wins}\n")

    def menu(self):
        print("Welcome to the Dice Game!")
        if self.current_user:
            print(f"Logged in as: {self.current_user}")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        return choice

    def register(self):
        print("\nRegistration")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        success, message = self.user_manager.register(username, password)
        print(message)

    def login(self):
        print("\nLogin")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        success, message = self.user_manager.login(username, password)
        if success:
            self.current_user = username
            print(f"Welcome, {self.current_user}!")
            self.play_game()
        else:
            print(message)

    def play_game(self):
        print("\nStarting the game...")
        for stage in range(1, 4):
            print(f"\nStage {stage}:")
            user_roll = random.randint(1, 6)
            cpu_roll = random.randint(1, 6)
            print(f"{self.current_user} rolled: {user_roll}")
            print(f"The CPU rolled: {cpu_roll}")

            if user_roll > cpu_roll:
                print(f"{self.current_user} wins this round!")
            elif user_roll < cpu_roll:
                print("The CPU wins this round!")
            else:
                print("It's a tie!")
                stage -= 1
                continue

            choice = input("Do you want to continue to the next stage? (1 for yes, 0 for no): ")
            if choice == "0":
                break
        else:
            print("Congratulations! You won all stages!")
            return

        print("Game over. You didn't win any stages.")

    def logout(self):
        print("\nLogging out...")
        self.current_user = None

    def show_top_scores(self):
        print("\nTop 10 Scores")

if __name__ == "__main__":
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
            print("Invalid choice. Please try again.")
