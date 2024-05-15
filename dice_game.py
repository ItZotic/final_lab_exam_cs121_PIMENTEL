import os
import random

from user_manager import UserManager
from score import Score
from user import User

class DiceGame:
    def __init__(personal):
        personal.user_manager = UserManager()
        personal.scores = []
        personal.current_user = None
        personal.user_manager.load_users()
        personal.load_score()

    def load_score(personal):
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
                    personal.scores.append(score)

    def save_score(personal):
        scores_file = os.path.join('data', 'rankings.txt')
        with open(scores_file, 'w') as file:
            for score in personal.scores:
                file.write(f"{score.username},{score.game_id},{score.points},{score.wins}\n")

    def menu(personal):
        print("Welcome to the Dice Game!")
        if personal.current_user:
            print(f"Logged in as: {personal.current_user}")
            personal.logged_in_menu()
        else:
            print("1. Sign up")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")
            return choice

    def logged_in_menu(personal):
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
            personal.play_game()
        elif choice == "2":
            personal.show_top_scores()
        elif choice == "3":
            personal.logout()
        else:
            print("Invalid choice. Please try again.")

    def play_game(personal):
        print("\nInitializing game...")
        total_points = 0
        stages_won = 0
        for stage in range(1, 4):
            print(f"\nStage {stage}:")
            user_roll = random.randint(1, 6)
            cpu_roll = random.randint(1, 6)
            print(f"{personal.current_user} rolled: {user_roll}")
            print(f"Yes Man rolled: {cpu_roll}")

            if user_roll > cpu_roll:
                print(f"{personal.current_user} wins this round!")
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
        personal.update_score(stages_won, total_points)

    def logout(personal):
        print("\nLogging out... \nsee you again next time")
        personal.current_user = None

    def update_score(personal, stages_won, total_points):
        if personal.current_user:
            personal.scores.append(Score(personal.current_user, len(personal.scores) + 1, total_points, stages_won))
            personal.save_score()
        else:
            print("Log in to update scores.")

    def show_top_scores(personal):
        print("\nTop Scores:")
        sorted_scores = sorted(personal.scores, key=lambda x: (x.points, x.wins), reverse=True)
        for i, score in enumerate(sorted_scores[:10], 1):
            print(f"{i}. {score.username}: Points - {score.points}, Wins - {score.wins}")

    def register(personal):
        username = input("Create your username: ")
        password = input("Make a strong password: ")
        success, message = personal.user_manager.register(username, password)
        print(message)
        if success:
            print("Nice! registration successfull.")
        else:
            print("Registration unsuccessfull, please try again.")

    def login(personal):
        username = input("Enter USERNAME: ")
        password = input("Enter PASSWORD: ")
        if personal.user_manager.login(username, password):
            personal.current_user = username
            print(f"Welcome, {personal.current_user}!")
        else:
            print("Login unsuccessfull, credentials missing or incorrect")
