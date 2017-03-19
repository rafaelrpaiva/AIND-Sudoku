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

unit_list = row_units + column_units + square_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

diag_unit_list = row_units + column_units + square_units + diagonal_units
diag_units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
diag_peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        The naked twins strategy is based on this concept: if two boxes within the same unit have
        only the same two digits, we can eliminate them from the other boxes in that unit.

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    ntwins = []
    # Part 1: filter the boxes and peers to find the instances of naked twins in the present board
    for box in values:
        if len(values[box]) == 2:
            for peer in peers[box]:
                if box < peer and values[peer] == values[box]:
                    ntwins.append([box, peer])
    # Part 2: eliminate naked twins values
    for n in ntwins:
        nt_units = [u for u in unit_list if n[0] in u and n[1] in u]
        for each_unit in nt_units:
            # Eliminate the naked twins as possibilities
            for item in each_unit:
                if item != n[0] and item != n[1]:
                    values[item] = values[item].replace(values[n[0]][0], '')
                    assign_value(values, item, values[item])  # to visualize the data

                    values[item] = values[item].replace(values[n[0]][1], '')
                    assign_value(values, item, values[item])  # to visualize the data
    if len([box for box in values.keys() if len(values[box]) == 0]):
        return False
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
        for peer in diag_peers[box]:
            values[peer] = values[peer].replace(number_assigned, '')
        if len(values[box]) == 1:
            assign_value(values, box, values[box])
    return values


def only_choice(values):
    for unit in diag_unit_list:
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
        # Strategy 2: Naked Twins
        values = naked_twins(values)
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


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

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
    possible_solutions_1 = [
        {'G7': '6', 'G6': '3', 'G5': '2', 'G4': '9', 'G3': '1', 'G2': '8', 'G1': '7', 'G9': '5', 'G8': '4', 'C9': '1',
         'C8': '5', 'C3': '8', 'C2': '237', 'C1': '23', 'C7': '9', 'C6': '6', 'C5': '37', 'A4': '2357', 'A9': '8',
         'A8': '6', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'F6': '125', 'F7': '35', 'F8': '9',
         'F9': '7', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'C4': '4',
         'B8': '3', 'B9': '4', 'I9': '9', 'I8': '7', 'I1': '23', 'I3': '23', 'I2': '6', 'I5': '5', 'I4': '8', 'I7': '1',
         'I6': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'E8': '1', 'A7': '27', 'A6': '257', 'E5': '347',
         'E4': '6', 'E7': '345', 'E6': '579', 'E1': '8', 'E3': '79', 'E2': '37', 'H8': '2', 'H9': '3', 'H2': '9',
         'H3': '5', 'H1': '4', 'H6': '17', 'H7': '8', 'H4': '17', 'H5': '6', 'D8': '8', 'D9': '6', 'D6': '279',
         'D7': '34', 'D4': '237', 'D5': '347', 'D2': '1', 'D3': '79', 'D1': '5'},
        {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8', 'H5': '6', 'F9': '7',
         'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8', 'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23',
         'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5', 'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9',
         'A4': '2357', 'A7': '27', 'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
         'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2', 'F6': '125',
         'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '79', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235',
         'F5': '8', 'E2': '3', 'F7': '35', 'F8': '9', 'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17',
         'D3': '79', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6',
         'D6': '279', 'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}
        ]

    if naked_twins(naked_twins_grid) in possible_solutions_1:
        print("Naked twins is working!")

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')