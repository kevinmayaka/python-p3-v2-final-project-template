#!/usr/bin/env python3

import sqlite3
#from models import Game, Player
from models import *

class CLI:
    def __init__(self):
        self.conn = sqlite3.connect('basketball.db')
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    height REAL,
                    weight REAL,
                    shooting INTEGER,
                    passing INTEGER
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    player_name TEXT NOT NULL,
                    score INTEGER,
                    FOREIGN KEY(player_name) REFERENCES players(name)
                )
            ''')

    def menu(self):
        while True:
            print("\nBasketball Training Camp CLI")
            print("1. Manage Players")
            print("2. Manage Games")
            print("3. Exit")
            choice = input("Choose an option: ")
            if choice == "1":
                self.manage_players()
            elif choice == "2":
                self.manage_games()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    def manage_players(self):
        while True:
            print("\nManage Players")
            print("1. Create Player")
            print("2. Delete Player")
            print("3. Display All Players")
            print("4. View Player Games")
            print("5. Find Player by Name")
            print("6. Back to Main Menu")
            choice = input("Choose an option: ")
            if choice == "1":
                self.create_player()
            elif choice == "2":
                self.delete_player()
            elif choice == "3":
                self.display_all_players()
            elif choice == "4":
                self.view_player_games()
            elif choice == "5":
                self.find_player_by_name()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")

    def create_player(self):
        try:
            name = input("Enter player name: ")
            position = input("Enter player position: ")
            height = float(input("Enter player height: "))
            weight = float(input("Enter player weight: "))
            shooting = int(input("Enter player shooting skill (0-100): "))
            passing = int(input("Enter player passing skill (0-100): "))
            player = player(name, position, height, weight, shooting, passing)
            player.save_to_db(self.conn)
            print(f"Player {name} created successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def delete_player(self):
        name = input("Enter the name of the player to delete: ")
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM players WHERE name = ?', (name,))
            player = cursor.fetchone()
            if player:
                self.conn.execute('DELETE FROM players WHERE name = ?', (name,))
                self.conn.execute('DELETE FROM games WHERE player_name = ?', (name,))
                print(f"Player {name} deleted successfully.")
            else:
                print(f"Player {name} not found.")

    def display_all_players(self):
        players = Player.get_all_from_db(self.conn)
        if not players:
            print("No players available.")
        else:
            for player in players:
                print(player)

    def view_player_games(self):
        name = input("Enter player name: ")
        cursor = self.conn.execute('SELECT * FROM players WHERE name = ?', (name,))
        player = cursor.fetchone()
        if player:
            cursor = self.conn.execute('SELECT * FROM games WHERE player_name = ?', (name,))
            games = cursor.fetchall()
            if not games:
                print(f"Player {name} has no games.")
            else:
                for game in games:
                    print(Game(game[1], game[2], game[3]))
        else:
            print(f"Player {name} not found.")

    def find_player_by_name(self):
        name = input("Enter player name: ")
        cursor = self.conn.execute('SELECT * FROM players WHERE name = ?', (name,))
        player = cursor.fetchone()
        if player:
            print(Player(player[1], player[2], player[3], player[4], player[5], player[6]))
        else:
            print(f"Player {name} not found.")

    def manage_games(self):
        while True:
            print("\nManage Games")
            print("1. Create Game")
            print("2. Delete Game")
            print("3. Display All Games")
            print("4. Back to Main Menu")
            choice = input("Choose an option: ")
            if choice == "1":
                self.create_game()
            elif choice == "2":
                self.delete_game()
            elif choice == "3":
                self.display_all_games()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def create_game(self):
        try:
            date = input("Enter game date: ")
            player_name = input("Enter player name: ")
            score = int(input("Enter game score: "))
            cursor = self.conn.execute('SELECT * FROM players WHERE name = ?', (player_name,))
            player = cursor.fetchone()
            if player:
                game = Game(date, player_name, score)
                game.save_to_db(self.conn)
                print(f"Game on {date} for player {player_name} created successfully.")
            else:
                print(f"Player {player_name} not found.")
        except ValueError as e:
            print(f"Error: {e}")

    def delete_game(self):
        date = input("Enter the date of the game to delete: ")
        player_name = input("Enter the name of the player: ")
        cursor = self.conn.execute('SELECT * FROM games WHERE date = ? AND player_name = ?', (date, player_name))
        game = cursor.fetchone()
        if game:
            with self.conn:
                self.conn.execute('DELETE FROM games WHERE date = ? AND player_name = ?', (date, player_name))
            print(f"Game on {date} for player {player_name} deleted successfully.")
        else:
            print(f"Game on {date} for player {player_name} not found.")

    def display_all_games(self):
        games = Game.get_all_from_db(self.conn)
        if not games:
            print("No games available.")
        else:
            for game in games:
                print(game)

if __name__ == "__main__":
    cli = CLI()
    cli.menu()
