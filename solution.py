# Solution of Sudoku game by Rafael Paiva
# For the functions worked during the week, I assumed some similar codifications.
# Reference to the solution: Peter Norvig's page in http://norvig.com/sudoku.html
# Belo Horizonte, Brazil, February 21st, 2017.

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [s + t for s in A for t in B]


# All boxes available in a board
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = list()
diagonal_units.append([rs+cs for rs, cs in zip(rows, cols)])
diagonal_units.append([rs+cs for rs, cs in zip(rows, cols[::-1])])

unit_list = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values, box):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        The naked twins strategy is based on this concept: if two boxes within the same unit have
        only the same two digits, we can eliminate them from the other boxes in that unit.

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unit_list:
        # Creating a set makes things easier to find intersections between boxes
        unit = set(unit)
        set_of_peers = set(peers[box])
        # Find all instances of naked twins
        for peer in unit.intersection(set_of_peers):
            if not set(values[peer]).difference(set(values[box])):
                digit1 = values[box][0]
                digit2 = values[box][1]
                # Eliminate the naked twins as possibilities for their peers
                for item in unit.difference(set([box, peer])):
                    if digit1 in values[item]:
                        values[item].remove(digit1)
                    if digit2 in values[item]:
                        values[item].remove(digit2)
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    if len(grid) != 81:
        return -1
    else:
        new_grid = []
        for a in grid:
            if a == '.':
                new_grid.append('123456789')
            else:
                new_grid.append(a)
        return dict(zip(boxes, new_grid))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The Sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

        Go through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.

        Args:
            values: Sudoku in dictionary form.
        Returns:
            Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        number_assigned = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(number_assigned, '')
        if len(values[box]) == 1:
            assign_value(values, box, values[box])
        # if only two digits remain in a box, it's time to try naked_twins
        elif len(values[box]) == 2:
            naked_twins(values, box)
    return values


def only_choice(values):
    for unit in unit_list:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Counting previous values
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Strategy 1: Eliminate
        values = eliminate(values)
        # Strategy 2: Only Choice
        values = only_choice(values)
        # Check how many boxes have a determined value and compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[x]) == 1 for x in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False),
    # return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    if type(grid) is str:
        values = grid_values(grid)
    else:
        values = grid
    return search(values)


def solve_regular(grid):
    unit_list = row_units + column_units + square_units + diagonal_units
    units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)
    return solve(grid)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    """
    common_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    display(grid_values(common_sudoku_grid))
    display(solve_regular(common_sudoku_grid))
    naked_twins_grid = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
                            'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
                            'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
                            'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
                            'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
                            'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
                            'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
                            'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
                            'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
                            'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
                            'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}

    display(solve(naked_twins_grid))
    """

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')