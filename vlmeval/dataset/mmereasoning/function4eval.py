import json
import sympy
import re
# input the answer dict (json.loads(extract_answer))
def calculate_answer_function_1(response_dict, answer_dict=None):
    try:
        expect_keys = ['A', 'B', 'C']
        for k in expect_keys:
            if k not in response_dict.keys():
                return False
        if response_dict["A"] / response_dict['B'] == 3 and response_dict["C"] / response_dict['B'] == 2:
            return True
        else:
            return False
    except:
        return False

def calculate_answer_function_2(response_dict, answer_dict=None):
    try:
        expect_keys = ['A', 'B', 'C', 'D', 'E', 'F']
        for k in expect_keys:
            if k not in response_dict.keys():
                return False
        if response_dict['A'] + response_dict['B'] + response_dict['C'] != 25:
            return False
        if response_dict['C'] + response_dict['E'] + response_dict['F'] != 25:
            return False
        if response_dict['A'] + response_dict['D'] + response_dict['F'] != 25:
            return False
        return True
    except:
        return False

def calculate_answer_function_3(response_dict, answer_dict=None):
    expect_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    for k in expect_keys:
        if k not in response_dict.keys():
            return False
    values = set(response_dict.values())
    expect_values = set(range(1, 16))
    if values != expect_values:
        return False
    diamond_list = [
        ['A', 'D', 'E', 'H'],
        ['C', 'E', 'G', 'H'],
        ['I', 'G', 'J', 'H'],
        ['N', 'M', 'J', 'H'],
        ['O', 'M', 'H', 'L'],
        ['K', 'L', 'H', 'F'],
        ['B', 'F', 'H', 'D']
    ]
    for diamond in diamond_list:
        total_value = 0
        for key in diamond:
            total_value += response_dict[key]
        if total_value != 30:
            return False
    return True

def calculate_answer_function_4(response_dict, answer_dict=None):
    expect_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    for k in expect_keys:
        if k not in response_dict.keys():
            return False
    values = set(response_dict.values())
    expect_values = set(range(1, 10))
    if values != expect_values:
        return False
    line_list = [
        ['A', 'B', 'E', 'D'],
        ['B', 'C', 'E', 'F'],
        ['D', 'E', 'G', 'H'],
        ['E', 'F', 'H', 'I'],
        ['B', 'D', 'H', 'F'],
        ['A', 'C', 'I', 'G']
    ]
    for line in line_list:
        total_value = 0
        for key in line:
            total_value += response_dict[key]
        if total_value != 20:
            return False
    return True

def calculate_answer_function_5(response_dict, answer_dict=None):
    expect_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
    for k in expect_keys:
        if k not in response_dict.keys():
            return False
    values = list(response_dict.values())
    for v in values:
        if v not in [20, 15, 10, 5]:
            return False
    num_dict = {}
    for v in values:
        num_dict[v] = num_dict.get(v, 0) + 1
    if num_dict.get(20, 0) > 5 or num_dict.get(15, 0) > 3 or num_dict.get(10, 0) > 3 or num_dict.get(5, 0) > 6:
        return False
    
    line_list = [
        ['A', 'B', 'C'],
        ['A', 'G', 'O'],
        ['O', 'P', 'Q'],
        ['C', 'K', 'Q'],
        ['A', 'D', 'I', 'N', 'Q'],
        ['C', 'F', 'I', 'L', 'O'],
        ['B', 'E', 'I', 'M', 'P'],
        ['G', 'H', 'I', 'J', 'K'],
        
    ]
    for line in line_list:
        total_value = 0
        for key in line:
            total_value += response_dict[key]
        if total_value != 55:
            return False
    return True

def calculate_answer_function_6(response_dict, answer_dict=None):
    expect_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']
    for k in expect_keys:
        if k not in response_dict.keys():
            return False
    values = set(response_dict.values())
    expect_values = set(range(1, 20))
    if values != expect_values:
        return False
    line_list = [
        ['A', 'J', 'S'],
        ['C', 'J', 'Q'],
        ['E', 'J', 'O'],
        ['G', 'J', 'M'],
        ['I', 'J', 'K'],
        ['L', 'J', 'H'],
        ['N', 'J', 'F'],
        ['P', 'J', 'D'],
        ['R', 'J', 'B'] 
    ]
    for line in line_list:
        total_value = 0
        for key in line:
            total_value += response_dict[key]
        if total_value != 30:
            return False
    return True

def calculate_answer_function_7(response_dict, answer_dict=None):
    expect_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    for k in expect_keys:
        if k not in response_dict.keys():
            return False
    values = set(response_dict.values())
    expect_values = set(range(1, 13))
    if values != expect_values:
        return False
    line_list = [
        ['A', 'C', 'F', 'H'],
        ['A', 'D', 'G', 'K'],
        ['B', 'C', 'D', 'E'],
        ['H', 'I', 'J', 'K'],
        ['B', 'F', 'I', 'L'],
        ['E', 'G', 'J', 'L']
    ]
    for line in line_list:
        total_value = 0
        for key in line:
            total_value += response_dict[key]
        if total_value != 26:
            return False
    return True

def calculate_answer_function_8(response_dict, answer_dict=None):
    expect_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
    for k in expect_keys:
        if k not in response_dict.keys():
            return False
    values = list(response_dict.values())
    for v in values:
        if v < 1 or v > 15:
            return False
    if len(values) != len(set(values)):
        return False
    line_list = [
        ['A', 'B', 'C'],
        ['A', 'F', 'K'],
        ['B', 'D', 'E'],
        ['B', 'E', 'H'],
        ['C', 'H', 'M'],
        ['D', 'G', 'J'],
        ['E', 'G', 'I'],
        ['F', 'I', 'L'],
        ['H', 'J', 'I'],
        ['K', 'L', 'M']
    ]
    for line in line_list:
        total_value = 0
        for key in line:
            total_value += response_dict[key]
        if total_value != 20:
            return False
    return True

def calculate_answer_function_9(response_dict, answer_dict=None):
    expect_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']
    for k in expect_keys:
        if k not in response_dict.keys():
            return False
    values = set(response_dict.values())
    expect_values = set(range(1, 20))
    if values != expect_values:
        return False
    
    line_list = [
        ['A', 'B', 'C'],
        ['A', 'D', 'H'],
        ['A', 'E', 'J'],
        ['C', 'F', 'J'],
        ['C', 'G', 'L'],
        ['H', 'I', 'J'],
        ['H', 'M', 'Q'],
        ['J', 'K', 'L'],
        ['J', 'N', 'Q'],
        ['J', 'O', 'S'],
        ['L', 'P', 'S'],
        ['Q', 'R', 'S']
    ]
    for line in line_list:
        total_value = 0
        for key in line:
            total_value += response_dict[key]
        if total_value != 22:
            return False
    return True

def calculate_answer_function_10(response_dict, answer_dict=None):
    expect_keys = ['A', 'B', 'C', 'D', 'E', 'F']
    for k in expect_keys:
        if k not in response_dict.keys():
            return False
    values = set(response_dict.values())
    expect_values = set(range(1, 7))
    if values != expect_values:
        return False
    line_1 = response_dict['A'] + response_dict['B'] + response_dict['D']
    line_2 = response_dict['D'] + response_dict['E'] + response_dict['F']
    line_3 = response_dict['A'] + response_dict['C'] + response_dict['F']
    return line_1 == line_2 == line_3

def calculate_answer_function_11(response_dict, answer_dict=None):
    expect_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    for k in expect_keys:
        if k not in response_dict.keys():
            return False
    values = set(response_dict.values())
    expect_values = set([1, 2, 3, 5, 7, 8])
    if values != expect_values:
        return False

    if response_dict['A'] + response_dict['C'] + 9 != 19:
        return False
    if response_dict['B'] + response_dict['C'] + response_dict['D'] != 19:
        return False
    if response_dict['F'] + response_dict['E'] + response_dict['D'] != 19:
        return False
    if response_dict['E'] + response_dict['G'] + 6 != 19:
        return False
    return True

def calculate_answer_function_12(response_dict, answer_dict=None):
    expect_keys = ['A', 'C', 'T', 'D', 'O', 'G', 'P', 'E', 'T', 'S']
    for k in expect_keys:
        if k not in response_dict.keys():
            return False
    num_1 = response_dict['C'] * 100 + response_dict['A'] * 10 + response_dict['T']
    num_2 = response_dict['D'] * 100 + response_dict['O'] * 10 + response_dict['G']
    num_3 = response_dict['P'] * 1000 + response_dict['E'] * 100 + response_dict['T'] * 10 + response_dict['S']
    return num_1 + num_2 == num_3

def match_answer_function(response_dict, answer_dict):
    for key, value in answer_dict.items():
        cur_response = response_dict.get(key, None)
        if isinstance(cur_response, list):
            cur_response = set(cur_response)
        if isinstance(value, list):
            value = set(value)
        if cur_response != value:
            return False
    return True

def match_coordinate_function(response_list, answer_list):
    response_coor = []
    for coor in response_list:
        response_coor.append(str(coor['row']) + str(coor['column']))
    
    answer_coor = []
    if isinstance(answer_list, dict):
        answer_list = [answer_list]
    for coor in answer_list:
        answer_coor.append(str(coor['row']) + str(coor['column']))
    
    return response_coor == answer_coor

# answer justify: answer in xxx
def multiple_match_function(response_dict, answer_list):
    assert len(response_dict) == 1
    response = list(response_dict.values())[0]
    if isinstance(response, list):
        response = set(response)
        answer_list = [set(ans) for ans in answer_list]
        return response in answer_list
    else:
        return response in answer_list

def compare_expression_function(response_dict, anwser_list):
    extract_equation = response_dict['equation']
    extract_expr = sympy.parse_expr(extract_equation.split('=')[0], evaluate=False)
    is_same = False
    for answer_eq in anwser_list:
        if is_same == True:
            return True
        is_cur_same = False
        answer_expr = sympy.parse_expr(answer_eq.split('=')[0], evaluate=False)
        if extract_expr.func != answer_expr.func:
            is_cur_same = False
            continue
            
        # for addition and multiplication, check if the set of arguments is the same
        if extract_expr.func in (sympy.Add, sympy.Mul):
            args1 = extract_expr.args
            args2 = answer_expr.args
                
            # if the number of arguments is different, the expressions are not the same
            if len(args1) != len(args2):
                is_cur_same = False
                continue
            # check if the set of arguments is the same
            is_cur_same = (set(str(arg) for arg in args1) == set(str(arg) for arg in args2))
        # for other functions, check if the expression is the same
        else:
            is_cur_same = (extract_expr == answer_expr)
        is_same = is_cur_same
    return is_same

def choice_function(response, answer):
    try:
        answer = eval(answer)
    except:
        pass
    if isinstance(answer, list):
        answer = ','.join(answer)
    else:
        answer = str(answer)
    response_list = [ans.strip() for ans in response.split(',')]
    answer_list = [ans.strip() for ans in answer.split(',')]
    return set(response_list) == set(answer_list)


def calculate_answer_function_hashi(response_list, answer=None, special_info=None):
    if response_list is None or special_info is None or len(response_list) == 0:
        return False
    bridges = response_list
    # special_info = json.loads(special_info)
    init_islands = special_info["init_islands"]
    # init_islands be like:
    # [
    # {"cord": "b1", "requirement": 2}, 
    # {"cord": "f8", "requirement": 1}
    # ]

    def is_valid_hashi(init_islands, bridges):
        from collections import defaultdict

        # Helper function to parse coordinates
        def parse_coordinate(cord):
            letter, number = cord[0], int(cord[1:])
            return ord(letter) - ord('a'), number

        # Rule 1: Distinct islands check
        for bridge in bridges:
            if bridge['start'] == bridge['end']:
                return False, "Rule 1 violated: Bridge starts and ends at the same island."

        # Group islands by coordinates for quick lookup
        island_requirements = {island['cord']: island['requirement'] for island in init_islands}
        existing_islands = set(island_requirements.keys())

        # Check for total bridge connections per island
        bridge_count = defaultdict(int)
        connection_count = defaultdict(int)

        # Check each bridge for validity
        for bridge in bridges:
            start = bridge['start']
            end = bridge['end']
            number = bridge['number']

            # Rule 6: Island existence check
            if start not in existing_islands or end not in existing_islands:
                return False, f"Rule 6 violated: One or both islands ({start}, {end}) do not exist."

            # Rule 3: Orthogonal Check
            start_x, start_y = parse_coordinate(start)
            end_x, end_y = parse_coordinate(end)
            if start_x != end_x and start_y != end_y:
                return False, f"Rule 3 violated: Bridge between {start} and {end} is not orthogonal."

            # Rule 4: Maximum two bridges between pair of islands
            pair = tuple(sorted([start, end]))
            connection_count[pair] += number
            if connection_count[pair] > 2:
                return False, f"Rule 4 violated: More than two bridges between {start} and {end}."

            # Count connections for each island
            bridge_count[start] += number
            bridge_count[end] += number

        # Rule 5: Check if each island's requirement is met
        for island, requirement in island_requirements.items():
            if bridge_count[island] != requirement:
                return False, f"Rule 5 violated: Island {island} has {bridge_count[island]} bridges, requires {requirement}."

        # Rule 2: Cross-check - Ensure no crossing bridges
        occupied_lines = set()
        for bridge in bridges:
            start_x, start_y = parse_coordinate(bridge['start'])
            end_x, end_y = parse_coordinate(bridge['end'])

            # Generate the line path between start and end
            if start_x == end_x:  # Vertical line
                y_min, y_max = sorted([start_y, end_y])
                for y in range(y_min + 1, y_max):
                    line_segment = (start_x, y)
                    if line_segment in occupied_lines:
                        return False, f"Rule 2 violated: Crossing bridge at ({chr(start_x + ord('a'))}{y})."
                    occupied_lines.add(line_segment)

            elif start_y == end_y:  # Horizontal line
                x_min, x_max = sorted([start_x, end_x])
                for x in range(x_min + 1, x_max):
                    line_segment = (x, start_y)
                    if line_segment in occupied_lines:
                        return False, f"Rule 2 violated: Crossing bridge at ({chr(x + ord('a'))}{start_y})."
                    occupied_lines.add(line_segment)

        return True, "Hashi: All rules satisfied."

    validity, message = is_valid_hashi(init_islands, bridges)
    print(message)
    return validity


def calculate_answer_function_skyscraper(response_list, answer=None, special_info=None):
    if response_list is None or special_info is None or len(response_list) == 0:
        return False

    grid = response_list
    visible_skyscrapers = special_info["visible_skyscrapers"]
    # visible_skyscrapers be like:
    # [
    #     [3,2,1],
    #     [3,2,1],
    #     [1,None,2],
    #     [1,2,None]
    # ]
    # represent the following case:
    # [
    #     [None,  3,      2,      1,      None],
    #     [3,     None,   None,   None,   1],
    #     [2,     None,   None,   None,   None],
    #     [1,     None,   None,   None,   2],
    #     [None,  1,      2,      None,   None]
    # ]


    # Verify if the base matrix has been changed
    base_matrix = special_info['base_matrix']
    size = len(base_matrix)
    for i in range(size):
        for j in range(size):
            if base_matrix[i][j] is not None and base_matrix[i][j]!=response_list[i][j]:
                # print("Mismatch with base matrix")
                return False
            
    
    for i in range(size):
        if len(set(grid[i])) != size or len(set(row[i] for row in grid)) != size:
            # print("repeat height on one row or colomn")
            return False

    def count_higher_than_previous(lst, target_count):
        count = 1  # Start with 1 since the first number is always higher than "nothing before it"
        max_so_far = lst[0]
        for i in range(1, len(lst)):
            if lst[i] > max_so_far:
                count += 1
                max_so_far = lst[i]
        return count == target_count
    
    # Verify the skyscraper rule
    hori = grid
    vert = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]
    
    for index, h in enumerate(visible_skyscrapers[0]):
        if h is None:
            continue
        if not count_higher_than_previous(vert[index], h):
            # print("wrong visible towers")
            return False
    
    for index, h in enumerate(visible_skyscrapers[1]):
        if h is None:
            continue
        if not count_higher_than_previous(hori[index], h):
            # print("wrong visible towers")
            return False
    
    for index, h in enumerate(visible_skyscrapers[2]):
        if h is None:
            continue
        if not count_higher_than_previous(hori[index][::-1], h):
            # print("wrong visible towers")
            return False
    
    for index, h in enumerate(visible_skyscrapers[3]):
        if h is None:
            continue
        if not count_higher_than_previous(vert[index][::-1], h):
            # print("wrong visible towers")
            return False
    # print("Skyscraper: All rules satisfied.")
    return True


def calculate_answer_function_sudoku_4(response_list, answer=None, special_info=None):
    if response_list is None or special_info is None or len(response_list) == 0:
        return False
    
    def is_valid_sudoku_4x4(grid):
        # Check rows and columns
        for i in range(4):
            if len(set(grid[i])) != 4 or len(set(row[i] for row in grid)) != 4:
                # print("repeat numbers in row or colomn")
                return False

        # Check 2x2 sub-grids
        sub_grids = [
            [grid[r][c] for r in range(2) for c in range(2)],  # Top-left
            [grid[r][c] for r in range(2) for c in range(2, 4)],  # Top-right
            [grid[r][c] for r in range(2, 4) for c in range(2)],  # Bottom-left
            [grid[r][c] for r in range(2, 4) for c in range(2, 4)],  # Bottom-right
        ]
        for sub_grid in sub_grids:
            if len(set(sub_grid)) != 4:
                # print("repeat numbers in sub matrix")
                return False
        # print("Sudoku_4: All rules satisfied.")
        return True

    try:
        # Parse the response string into a Python list
        grid = response_list
        if not isinstance(grid, list) or len(grid) != 4 or not all(len(row) == 4 for row in grid):
            return False

        # Verify if the base matrix has been changed
        base_matrix = special_info['base_matrix']
        for i in range(4):
            for j in range(4):
                if base_matrix[i][j] is not None and base_matrix[i][j]!=grid[i][j]:
                    # print("Mismatch with base matrix")
                    return False

        # Validate the Sudoku grid
        return is_valid_sudoku_4x4(grid)
    except (ValueError, SyntaxError):
        return False
    

def calculate_answer_function_sudoku_6(response_list, answer=None, special_info=None):
    if response_list is None or special_info is None or len(response_list) == 0:
        return False
    
    def is_valid_sudoku_6x6(grid):
        # Check rows and columns
        for i in range(6):
            if len(set(grid[i])) != 6 or len(set(row[i] for row in grid)) != 6:
                return False

        # Check 2x2 sub-grids
        sub_grids = [
            [grid[r][c] for r in range(2) for c in range(3)],  # Top-left
            [grid[r][c] for r in range(2) for c in range(3, 6)],  # Top-right
            [grid[r][c] for r in range(2, 4) for c in range(3)],  # Middle-left
            [grid[r][c] for r in range(2, 4) for c in range(3, 6)],  # Middle-right
            [grid[r][c] for r in range(4, 6) for c in range(3)],  # Bottom-left
            [grid[r][c] for r in range(4, 6) for c in range(3, 6)],  # Bottom-right
        ]
        for sub_grid in sub_grids:
            if len(set(sub_grid)) != 6:
                return False
        return True

    try:
        # Parse the response string into a Python list
        grid = response_list
        if not isinstance(grid, list) or len(grid) != 6 or not all(len(row) == 6 for row in grid):
            return False
        
        # Verify if the base matrix has been changed
        base_matrix = special_info['base_matrix']
        for i in range(6):
            for j in range(6):
                if base_matrix[i][j] is not None and base_matrix[i][j]!=grid[i][j]:
                    return False
                
        # Validate the Sudoku grid
        return is_valid_sudoku_6x6(grid)
    except (ValueError, SyntaxError):
        return False
    
 
def calculate_answer_function_yinyang(response_list, answer=None, special_info=None):
    if response_list is None or special_info is None or len(response_list) == 0:
        return False
    
    def is_connected(matrix, value):
        rows, cols = len(matrix), len(matrix[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]

        def dfs(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols or visited[r][c] or matrix[r][c] != value:
                return
            visited[r][c] = True
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                dfs(r + dr, c + dc)

        # Find the first cell with the given value
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c] == value:
                    dfs(r, c)
                    break
            else:
                continue
            break

        # Check if all cells with the given value are visited
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c] == value and not visited[r][c]:
                    return False
        return True

    def has_2x2_block(matrix, value):
        rows, cols = len(matrix), len(matrix[0])
        for r in range(rows - 1):
            for c in range(cols - 1):
                # Check if a 2x2 block is formed by the same value
                if (
                    matrix[r][c] == value and
                    matrix[r][c + 1] == value and
                    matrix[r + 1][c] == value and
                    matrix[r + 1][c + 1] == value
                ):
                    return True
        return False

    # Check if the response is a 6x6 matrix
    if not isinstance(response_list, list) or len(response_list) != 6 or any(len(row) != 6 for row in response_list):
        return False

    # Verify if the base matrix has been changed
    base_matrix = special_info['base_matrix']
    for i in range(6):
        for j in range(6):
            if base_matrix[i][j] is not None and base_matrix[i][j]!=response_list[i][j]:
                print("Mismatch with base matrix")
                return False

    # Check if 0s and 1s form connected components
    if not is_connected(response_list, 0) or not is_connected(response_list, 1):
        print("not connected")
        return False

    # Check if there are any 2x2 blocks of 0s or 1s
    if has_2x2_block(response_list, 0) or has_2x2_block(response_list, 1):
        print("exist 2x2 block")
        return False
    print("Yinyang: All rules satisfied")
    return True   

def judge_24points_function(response, answer=None, special_info=None):
    left_formula = response.replace(' ', '').split('=')[0]
    try:
        if eval(left_formula) == 24:
            numbers = re.findall(r'\d+', left_formula)
            numbers = list(map(int, numbers))
            numbers.sort()
            expect_numbers = special_info['init_cards']
            expect_numbers.sort()
            if numbers == expect_numbers:
                return True
            else:
                return False
        else:
            return False

    except:
        return False

functions = {
    "calculate_answer_function_1": calculate_answer_function_1,
    "calculate_answer_function_2": calculate_answer_function_2,
    "calculate_answer_function_3": calculate_answer_function_3,
    "calculate_answer_function_4": calculate_answer_function_4,
    "calculate_answer_function_5": calculate_answer_function_5,
    "calculate_answer_function_6": calculate_answer_function_6,
    "calculate_answer_function_7": calculate_answer_function_7,
    "calculate_answer_function_8": calculate_answer_function_8,
    "calculate_answer_function_9": calculate_answer_function_9,
    "calculate_answer_function_10": calculate_answer_function_10,
    "calculate_answer_function_11": calculate_answer_function_11,
    "calculate_answer_function_12": calculate_answer_function_12,
    "match_answer_function": match_answer_function,
    "multiple_match_function": multiple_match_function,
    "compare_expression_function": compare_expression_function,
    "match_coordinate_function": match_coordinate_function,
    "choice_function": choice_function,
    "calculate_answer_function_hashi": calculate_answer_function_hashi,
    "calculate_answer_function_skyscraper": calculate_answer_function_skyscraper,
    "calculate_answer_function_sudoku_4": calculate_answer_function_sudoku_4,
    "calculate_answer_function_sudoku_6": calculate_answer_function_sudoku_6,
    "calculate_answer_function_yinyang": calculate_answer_function_yinyang,
    "judge_24points_function": judge_24points_function
}
