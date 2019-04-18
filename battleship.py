#!/usr/bin/env python3
import os
from random import choice, randint, random

# Class of ship  Size
# -------------  ----
# Carrier        5
# Battleship     4
# Cruiser        3
# Submarine      3
# Destroyer      2


class Ship(object):
    def __init__(self, name, size, coords=()):
        self._name = name
        self._size = size
        self._coords = coords
        self._hits = []

    def set_coords(self, coords):
        self._coords = coords

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size

    @property
    def coords(self):
        return self._coords

    def is_on_coord(self, coord):
        return coord in self._coords

    def take_hit(self, coord):
        self._hits.append(coord)

    @property
    def has_sunk(self):
        return len(self._hits) == self._size

    def __str__(self):
        return '<Ship name={0}>'.format(self._name)


class Game(object):
    def __init__(self, rows=9, cols=9):
        self._size = (rows, cols)
        self._columns = [chr(num + 96).upper() for num in range(1, cols + 1)]
        self._rows = [str(num) for num in range(1, rows + 1)]

        self._moves = []
        self._available_options = [
            col + row
            for col in self._columns
            for row in self._rows
        ]

        self._ships = (
            Ship('Carrier', 5),
            Ship('Battleship', 4),
            Ship('Cruiser', 3),
            Ship('Submarine', 3),
            Ship('Destroyer', 2),
        )

        for ship in self._ships:
            self.randomly_place_ship(ship)

    def randomly_place_ship(self, ship):
        horizontal = random() < 0.5

        if horizontal:
            row = str(choice(self._rows))
            start_col = randint(0, len(self._columns) - ship.size)
            end_col = start_col + ship.size
            coords = [
                self._columns[col] + row
                for col in range(start_col, end_col)
            ]
        else:
            col = choice(self._columns)
            start_row = randint(0, len(self._rows) - ship.size)
            end_row = start_row + ship.size
            coords = [
                col + str(self._rows[row])
                for row in range(start_row, end_row)
            ]

        coords_taken = self.coords_taken
        for coord in coords:
            if coord in coords_taken:
                self.randomly_place_ship(ship)
                return

        ship.set_coords(coords)

    def check_valid_move(self, move):
        if move in ('QUIT', 'EXIT'):
            exit(0)

        if move not in self._available_options:
            print(('Invalid move. A move consists of a letter and a '
                   'number, like B2, with a minimum of {first} and a '
                   'maximum of {last}.').format(
                first=self._available_options[0],
                last=self._available_options[-1],
            ))
        elif move in self._moves:
            print('Move {move} was already made. Pick another.'.format(
                move=move,
            ))
        else:
            return True
        return False

    def choose_move(self):
        move = None
        while move is None:
            i = input('Choose your next move: ').upper()
            if self.check_valid_move(i):
                move = i

        if move:
            self._moves.append(move)
            ship = self.ship_at_coord(move)
            if ship:
                ship.take_hit(move)
        return move

    def ship_at_coord(self, coord):
        for ship in self._ships:
            if ship.is_on_coord(coord):
                return ship
        return None

    def print_cell(self, coord):
        ship_on_cell = self.ship_at_coord(coord)
        cell = '·' if ship_on_cell else ' '
        if coord in self._moves:
            cell = 'X' if ship_on_cell else 'o'

        return cell

    def print_grid(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        cell_width = 3
        col_sep = ''
        lines = []

        top_row = ' ' * cell_width + col_sep + \
            col_sep.join([name.center(cell_width) for name in self._columns])
        # dash_row = col_sep.join(
        #     ['-' * cell_width for _ in range(0, len(self._columns) + 1)])
        # lines.append(dash_row)
        lines.append(top_row)
        # lines.append(dash_row)
        for row in self._rows:
            row_cells = []
            for col in self._columns:
                coord = col + row
                cell = self.print_cell(coord)
                row_cells.append(cell)
            lines.append(row.center(cell_width) + col_sep + col_sep.join(
                [cell.center(cell_width) for cell in row_cells]))
            # lines.append(dash_row)

        # [print('|' + line + '|') for line in lines]
        [print(line) for line in lines]

    def print_status(self):
        if self._moves:
            last_move = self._moves[-1]
            ship = self.ship_at_coord(last_move)
            if ship:
                print('Kaboooom!')
                if ship.has_sunk:
                    print('{ship} has sunk!'.format(ship=ship.name))
            else:
                print('Splash!')

            print('Last move: ' + last_move)
        else:
            print()

    @property
    def coords_taken(self):
        coords = []
        for ship in self._ships:
            for coord in ship.coords:
                coords.append(coord)
        return coords

    @property
    def turns(self):
        return len(self._moves)

    @property
    def ended(self):
        return all([ship.has_sunk for ship in self._ships])


if __name__ == "__main__":
    game = Game(9, 9)
    while not game.ended:
        game.print_grid()
        game.print_status()
        game.choose_move()

    game.print_grid()
    game.print_status()
    print("Congratulations! You sank all the ships in {turns} turns.".format(
        turns=game.turns,
    ))
