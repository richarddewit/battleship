#!/usr/bin/env python3
import os

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


class Grid(object):
    def __init__(self, rows, cols):
        self._size = (rows, cols)
        self._columns = [chr(num + 96).upper() for num in range(1, cols + 1)]
        self._rows = [str(num) for num in range(1, rows + 1)]

        self._moves = []
        self._available_options = [
            col + row
            for col in self._columns
            for row in self._rows
        ]

        # TODO: Place all 5 ships randomly
        self._ships = (
            Ship('Carrier', 5, ('F4', 'F5', 'F6', 'F7', 'F8')),
            Ship('Cruiser', 3, ('B2', 'B3', 'B4')),
            Ship('Destroyer', 2, ('H6', 'I6')),
        )

    def choose_move(self):
        move = None
        while move is None:
            i = input('Choose your next move: ').upper()
            if i in ('QUIT', 'EXIT'):
                exit(0)

            if i not in self._available_options:
                print('Invalid move. A move consists of a letter and a number, like B2, with a minimum of {first} and a maximum of {last}.'.format(
                    first=self._available_options[0],
                    last=self._available_options[-1],
                ))
            elif i in self._moves:
                print('Move {move} was already made. Pick another.'.format(
                    move=i,
                ))
            else:
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
        self.game_ended
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
    def turns(self):
        return len(self._moves)

    @property
    def game_ended(self):
        return all([ship.has_sunk for ship in self._ships])


if __name__ == "__main__":
    grid = Grid(9, 9)
    while not grid.game_ended:
        grid.print_grid()
        grid.print_status()
        grid.choose_move()

    grid.print_grid()
    grid.print_status()
    print("Congratulations! You sank all the ships in {turns} turns.".format(
        turns=grid.turns,
    ))
