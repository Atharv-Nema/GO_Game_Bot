N = 9 # Board size

def convert_to_1d(position: tuple[int, int]) -> int:
    """
    Takes in a 2D zero indexed coordinate and converts it into a 1D coordinate
    Parameters:
    position (tuple[str,str]): Of form (x, y)
    """
    x,y = position
    return x + y * N

def convert_to_2d(index: int) -> tuple[int, int]:
    y, x = divmod(index, N)
    return (x, y)

def generate_graph() -> list[list]: # May want to get a better structure
    graph = []
    for node in range(N*N):
        neighbours = []
        x, y = convert_to_2d(node)
        if x != 0:
            neighbours.append(convert_to_1d((x - 1, y)))
        if x != N - 1:
            neighbours.append(convert_to_1d((x + 1, y)))
        if y != 0:
            neighbours.append(convert_to_1d((x, y - 1)))
        if y != N - 1:
            neighbours.append(convert_to_1d((x, y + 1)))
        graph.append(neighbours)
    return graph

GRAPH = generate_graph() # Precomputing the neighbour graph

def get_liberty_count(board: str, index: int) -> int:
    """
    Returns the total count of the liberties of the block containing index
    Parameters:
    board (str): The go board
    index (int): The 1D index
    Returns:
    The total number of liberties
    """
    if board[index] == ' ':
        raise ValueError('The liberties of an empty cell is not defined')
    visited = set()
    liberty_count = 0
    stack = [index]
    visited.add(index)
    # Perform a simple dfs
    while stack:
        node = stack.pop()
        neighbours = GRAPH[node]
        for neighbour in neighbours:
            if neighbour not in visited:
                if board[neighbour] == ' ':
                    liberty_count += 1
                elif board[neighbour] == board[index]: # Same colour
                    stack.append(neighbour)
                visited.add(neighbour)
    return liberty_count

def remove_block(board: str, index: int) -> str:
    """
    Removes the block containing the index
    Parameters:
    board (str): The go board
    index (int): The 1D index
    Returns:
    The new board
    """
    board_list = list(board)
    initial_colour = board_list[index]
    if board[index] == ' ':
        raise ValueError('No block contains an empty cell')
    stack = [index]
    board_list[index] = ' '
    # Performing a simple dfs
    while stack:
        node = stack.pop()
        neighbours = GRAPH[node]
        for neighbour in neighbours:
            if board_list[neighbour] == initial_colour:
                board_list[neighbour] = ' '
                stack.append(neighbour)
    return ''.join(board_list)
             

def make_move(board: str, index: int, piece: str):
    if board[index] != ' ':
        raise ValueError("Cannot place a piece on a non empty cell")
    # Make the move
    board_list = list(board)
    board_list[index] = piece
    new_board = ''.join(board_list)

    
    neighbours = GRAPH[index]
    # Remove any blocks of opponent with zero liberties
    for neighbour in neighbours:
        if new_board[neighbour] != ' ' and new_board[neighbour] != piece:
            if get_liberty_count(new_board, neighbour) == 0:
                new_board = remove_block(new_board, neighbour)
    
    # If still no liberties exist for the current piece raise exception
    if get_liberty_count(new_board, index) == 0:
        raise ValueError("Cannot perform suicide")
    return new_board
    