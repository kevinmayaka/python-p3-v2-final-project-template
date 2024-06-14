import sqlite3

class Attributes:
    def __init__(self, height, weight):
        self.height = height
        self.weight = weight

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Height must be a number")
        if value <= 0:
            raise ValueError("Height must be greater than zero")
        self._height = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Weight must be a number")
        if value <= 0:
            raise ValueError("Weight must be greater than zero")
        self._weight = value


class Skills:
    def __init__(self, shooting, passing):
        self.shooting = shooting
        self.passing = passing

    @property
    def shooting(self):
        return self._shooting

    @shooting.setter
    def shooting(self, value):
        if not isinstance(value, int):
            raise ValueError("Shooting skill must be an integer")
        if value < 0 or value > 100:
            raise ValueError("Shooting skill must be between 0 and 100")
        self._shooting = value

    @property
    def passing(self):
        return self._passing

    @passing.setter
    def passing(self, value):
        if not isinstance(value, int):
            raise ValueError("Passing skill must be an integer")
        if value < 0 or value > 100:
            raise ValueError("Passing skill must be between 0 and 100")
        self._passing = value


class Position:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Position name must be a string")
        if len(value) == 0:
            raise ValueError("Position name must be greater than zero characters")
        self._name = value


class Player:
    def __init__(self, name, position, height, weight, shooting, passing):
        self.name = name
        self.position = Position(position)
        self.attributes = Attributes(height, weight)
        self.skills = Skills(shooting, passing)
        self._games = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) == 0:
            raise ValueError("Name must be greater than zero characters")
        self._name = value

    @property
    def games(self):
        return self._games

    def add_game(self, game):
        if isinstance(game, Game):
            self._games.append(game)

    def all_game_scores(self):
        return [game.score for game in self._games]

    def save_to_db(self, conn):
        with conn:
            conn.execute('''
                INSERT INTO players (name, position, height, weight, shooting, passing)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.name, self.position.name, self.attributes.height, self.attributes.weight, self.skills.shooting, self.skills.passing))

    def delete_from_db(self, conn):
        with conn:
            conn.execute('DELETE FROM players WHERE name = ?', (self.name,))
            conn.execute('DELETE FROM games WHERE player_name = ?', (self.name,))

    @staticmethod
    def get_all_from_db(conn):
        cursor = conn.execute('SELECT * FROM players')
        players = cursor.fetchall()
        return [Player(p[1], p[2], p[3], p[4], p[5], p[6]) for p in players]

    def __repr__(self):
        return f"<Player: {self.name}, Position: {self.position.name}>"


class Game:
    def __init__(self, date, player_name, score):
        self.date = date
        self.player_name = player_name
        self.score = score

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, str):
            raise ValueError("Date must be a string")
        if len(value) == 0:
            raise ValueError("Date must be greater than zero characters")
        self._date = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError("Score must be an integer")
        if value < 0:
            raise ValueError("Score must be greater than or equal to zero")
        self._score = value

    def save_to_db(self, conn):
        with conn:
            conn.execute('''
                INSERT INTO games (date, player_name, score)
                VALUES (?, ?, ?)
            ''', (self.date, self.player_name, self.score))

    def delete_from_db(self, conn):
        with conn:
            conn.execute('DELETE FROM games WHERE date = ? AND player_name = ?', (self.date, self.player_name))

    @staticmethod
    def get_all_from_db(conn):
        cursor = conn.execute('SELECT * FROM games')
        games = cursor.fetchall()
        return [Game(g[1], g[2], g[3]) for g in games]

    def __repr__(self):
        return f"<Game: {self.date}, Score: {self.score}>"
