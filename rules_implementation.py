from typing import Union

class Board:
    """The internal representation of the board"""
    def __init__(self, board_str: str, territory_str: str):
        """
        Parameters:
        board_str (str): The string that represents the position of pieces
        on the board
        territory_str (str): The string that represents the current territory 
        situation of the board
        """
        self.board_str = board_str
        self.territory_str = territory_str

    def __getitem__(self, key: int):
        """Returns the piece at index key"""
        return self.board_str[key]


class MoveManager:
    """Class that manages moves"""
    def __init__(self, board_size: int):
        self.BOARD_SIZE = board_size
        self.GRAPH = self.generate_graph() # Neighbours graph

    def create_territory(self, board_str: str) -> str:
        """Creates the territory string from its board string"""
        N = self.BOARD_SIZE
        white_territory_list = [False for i in range(N * N)]
        black_territory_list = [False for i in range(N * N)]
        def spread_color(color_territory_list, node):
            color_territory_list[node] = True
            for neighbour in self.GRAPH[node]:
                if board_str[neighbour] == '-' and (not color_territory_list[neighbour]):
                    spread_color(color_territory_list, neighbour)
        for node in range(N*N):
            if board_str[node] == 'o':
                spread_color(white_territory_list, node)
            if board_str[node] == 'x':
                spread_color(black_territory_list, node)
        final_territory_list = []
        for i in range(N * N):
            if not (black_territory_list[i] ^ white_territory_list[i]):
                final_territory_list.append('-')
            elif black_territory_list[i] and not white_territory_list[i]:
                final_territory_list.append('x')
            elif white_territory_list[i] and not black_territory_list[i]:
                final_territory_list.append('o')
        return ''.join(final_territory_list)

            
    def create_board(self, board_str: str) -> Board:
        """Takes in the board_str and creates the board"""
        return Board(board_str, self.create_territory(board_str))

    def convert_to_1d(self, position: tuple[int, int]) -> int:
        """
        Takes in a 2D zero indexed coordinate and converts it into a 1D coordinate
        Parameters:
        position (tuple[int, int]): Of form (x, y)
        """
        x,y = position
        return x + y * self.BOARD_SIZE

    def convert_to_2d(self, index: int) -> tuple[int, int]:
        """
        Takes in a 1D zero indexed coordinate and converts it into a 2D coordinate
        Parameters:
        index (int): The 1d index
        """
        y, x = divmod(index, self.BOARD_SIZE)
        return (x, y)

    def generate_graph(self) -> list[list]:
        """
        Generates the neighbour graph
        Returns:
        A list of list(GRAPH) where GRAPH[x] is the list of 1d indices that neighbour
        1d index x
        """
        N = self.BOARD_SIZE
        graph = []
        for node in range(N*N):
            neighbours = []
            x, y = self.convert_to_2d(node)
            if x != 0:
                neighbours.append(self.convert_to_1d((x - 1, y)))
            if x != N - 1:
                neighbours.append(self.convert_to_1d((x + 1, y)))
            if y != 0:
                neighbours.append(self.convert_to_1d((x, y - 1)))
            if y != N - 1:
                neighbours.append(self.convert_to_1d((x, y + 1)))
            graph.append(neighbours)
        return graph

    def get_liberty_count(self, board: Union[str, Board], index: int) -> int:
        """
        Returns the total count of the liberties of the block containing index
        Parameters:
        board (Union[Board, str]): The go board or the board string
        index (int): The 1D index
        Returns:
        The total number of liberties
        """
        if board[index] == '-':
            raise ValueError('The liberties of an empty cell is not defined')
        visited = set()
        liberty_count = 0
        stack = [index]
        visited.add(index)
        # Perform a simple dfs
        while stack:
            node = stack.pop()
            neighbours = self.GRAPH[node]
            for neighbour in neighbours:
                if neighbour not in visited:
                    if board[neighbour] == '-':
                        liberty_count += 1
                    elif board[neighbour] == board[index]: # Same colour
                        stack.append(neighbour)
                    visited.add(neighbour)
        return liberty_count

    def remove_block(self, board_str: str, index: int) -> str:
        """
        Removes the block containing the index
        Parameters:
        board_str (str): The string that represents the pieces on the board
        index (int): The 1D index
        Returns:
        The new board string
        """
        board_list = list(board_str)
        initial_colour = board_list[index]
        if board_str[index] == '-':
            raise ValueError('No block contains an empty cell')
        stack = [index]
        board_list[index] = '-'
        # Performing a simple dfs
        while stack:
            node = stack.pop()
            neighbours = self.GRAPH[node]
            for neighbour in neighbours:
                if board_list[neighbour] == initial_colour:
                    board_list[neighbour] = '-'
                    stack.append(neighbour)
        return ''.join(board_list)
                

    def make_move(self, board: Board, index: int, piece: str) -> Board:
        """
        Returns the board after the move has been made
        Parameters:
        board (Board): The go board
        index (int): The 1d index where a piece is to be placed
        piece(str): The piece to be placed
        Returns:
        The new board
        """
        if board[index] != '-':
            raise ValueError("Cannot place a piece on a non empty cell")
        # Make the move
        board_list = list(board.board_str)
        board_list[index] = piece
        new_board = ''.join(board_list)

        
        neighbours = self.GRAPH[index]
        # Remove any blocks of opponent with zero liberties
        for neighbour in neighbours:
            if new_board[neighbour] != '-' and new_board[neighbour] != piece:
                if self.get_liberty_count(new_board, neighbour) == 0:
                    new_board = self.remove_block(new_board, neighbour)
        
        # If still no liberties exist for the current piece raise exception
        if self.get_liberty_count(new_board, index) == 0:
            raise ValueError("Cannot perform suicide")
        return self.create_board(new_board)
    