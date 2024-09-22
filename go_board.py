import pygame
import sys
from rules_implementation import Board, MoveManager

# Initialize Pygame
pygame.init()

# Set up display
board_size = 9
MOVE_MANAGER = MoveManager(board_size)
cell_size = 60
width = board_size * cell_size
height = board_size * cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Go Board")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (210, 180, 140)
PIECE_RADIUS = cell_size // 2 - 5

# Fonts
font = pygame.font.Font(None, 36)

def draw_board(board: Board):
    """
    Takes in the board and draws it
    Parameters:
    board (Board): The board
    """
    screen.fill(BACKGROUND_COLOR)

    # Draw grid lines
    for i in range(board_size):
        pygame.draw.line(screen, LINE_COLOR, (i * cell_size + cell_size // 2, cell_size // 2), 
                         (i * cell_size + cell_size // 2, height - cell_size // 2), 2)
        pygame.draw.line(screen, LINE_COLOR, (cell_size // 2, i * cell_size + cell_size // 2), 
                         (width - cell_size // 2, i * cell_size + cell_size // 2), 2)

    # Draw pieces
    for i in range(board_size * board_size):
        cell = board[i]
        row, col = divmod(i, board_size)
        x = col * cell_size + cell_size // 2
        y = (board_size - 1 - row) * cell_size + cell_size // 2  # Adjusted for Go's coordinate system

        if cell == 'x':  # Black piece
            pygame.draw.circle(screen, BLACK, (x, y), PIECE_RADIUS)
        elif cell == 'o':  # White piece
            pygame.draw.circle(screen, WHITE, (x, y), PIECE_RADIUS)
            pygame.draw.circle(screen, BLACK, (x, y), PIECE_RADIUS, 2)  # Outline for white piece

    # Draw labels
    for i in range(board_size):
        # Draw numbers for rows (1 at the bottom, 9 at the top)
        text_surface = font.render(str(board_size - i), True, RED)
        screen.blit(text_surface, (0, i * cell_size + cell_size // 2 - text_surface.get_height() // 2))

        # Draw numbers for columns
        text_surface = font.render(chr(ord('A') + i), True, RED)
        screen.blit(text_surface, (i * cell_size + cell_size // 2 - text_surface.get_width() // 2, 0))

def get_cell_index(pos: tuple[float, float]) -> int:
    """
    Takes in the position of the mouse and calculates the board's 1D index
    Parameters:
    pos (tuple[float, float]): The 2D pygame coordinates of the mouse pointer
    Returns:
    The 1D board index
    """
    x, y = pos
    row = board_size - 1 - (y // cell_size)  # Adjust for Go's coordinate system
    col = x // cell_size
    return row * board_size + col

def handle_click(board: Board, index: int, button: int) -> Board:
    """
    Handles the event of clicking the go board. A click on an already existing
    piece indicates removal. A left click indicates adding a white piece while
    a left click indicates adding a black piece.

    Parameters:
    board (Board): The internal representation of the go board
    index (int): The 1D index of the position where the click occured
    button (int): Represents which button was clicked

    Returns:
    The modified board object
    """
    if board[index] == '-':
        # 1 means left click i.e. white('o'), 3 is right click i.e. black('x')
        piece = 'o' if button == 1 else 'x'
        try:
            board = MOVE_MANAGER.make_move(board, index, piece)
        except ValueError as v:
            print(str(v))
    else:
        board_list = list(board.board_str)
        board_list[index] = '-'  # Remove the piece if clicked again
        board = MOVE_MANAGER.create_board(''.join(board_list))
    return board

def main():
    board = MOVE_MANAGER.create_board('-' * 81)  # Initialize empty board
    
    running = True
    while running:
        draw_board(board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                index = get_cell_index(pos)
                board = handle_click(board, index, event.button)
                

if __name__ == "__main__":
    main()