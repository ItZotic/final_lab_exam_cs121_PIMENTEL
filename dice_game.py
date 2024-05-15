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
        self.user_manager.load_users()
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
            self.logged_in_menu()
        else:
            print("1. Sign up")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")
            return choice

    def logged_in_menu(self):
        print("\n==========================================================")
        print("               ⚀⚁⚂ WELCOME TO THE LUCKY 38 ⚃⚄⚅            ")
        print("              ッ TEST YOUR LUCK AGAINST YES MAN ッ           ")
        print("==========================================================\n")
        print("1. Start game")
        print("2. Show top scores")
        print("3. Log out")
        choice = input("Enter your choice: ")
        if choice == "":
            print("No input. Returning to the menu.")
        elif choice == "1":
            self.play_game()
        elif choice == "2":
            self.show_top_scores()
        elif choice == "3":
            self.logout()
        else:
            print("Invalid choice. Please try again.")

    def play_game(self):
        print("\nInitializing game...")
        total_points = 0
        stages_won = 0
        for stage in range(1, 4):
            print(f"\nStage {stage}:")
            user_roll = random.randint(1, 6)
            cpu_roll = random.randint(1, 6)
            print(f"{self.current_user} rolled: {user_roll}")
            print(f"Yes Man rolled: {cpu_roll}")

            if user_roll > cpu_roll:
                print(f"{self.current_user} wins this round!")
                total_points += 1
                stages_won += 1
            elif user_roll < cpu_roll:
                print("Yes Man wins this round!")
            else:
                print("It's a tie!")
                stage -= 1
                continue

            choice = input("Do you want to continue to the next stage? (1 for yes, 0 for no): ")
            if choice == "0":
                break
        else:
            print(f"Congratulations! You won {stages_won} stage(s)!")
        
        print(f"Game over. You won {stages_won} stage(s) with a total of {total_points} points.")
        self.update_score(stages_won, total_points)

    def logout(self):
        print("\nLogging out... \nsee you again next time")
        self.current_user = None

    def update_score(self, stages_won, total_points):
        if self.current_user:
            self.scores.append(Score(self.current_user, len(self.scores) + 1, total_points, stages_won))
            self.save_score()
        else:
            print("Log in to update scores.")

    def show_top_scores(self):
        print("\nTop Scores:")
        sorted_scores = sorted(self.scores, key=lambda x: (x.points, x.wins), reverse=True)
        for i, score in enumerate(sorted_scores[:10], 1):
            print(f"{i}. {score.username}: Points - {score.points}, Wins - {score.wins}")

    def register(self):
        username = input("Create your username: ")
        password = input("Make a strong password: ")
        success, message = self.user_manager.register(username, password)
        print(message)
        if success:
            print("Nice! registration successfull.")
        else:
            print("Registration unsuccessfull, please try again.")

    def login(self):
        username = input("Enter USERNAME: ")
        password = input("Enter PASSWORD: ")
        if self.user_manager.login(username, password):
            self.current_user = username
            print(f"Welcome, {self.current_user}!")
        else:
            print("Login unsuccessfull, credentials missing or incorrect")
