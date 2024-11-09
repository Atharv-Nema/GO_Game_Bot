import pygame
import sys
from game_implementation.rules_implementation import MoveManager
from display_class import VisualInterface

# Initialize Pygame
pygame.init()

# Set up display
board_size = 9
MOVE_MANAGER = MoveManager(board_size)
DRAWING_OBJECT = VisualInterface(MOVE_MANAGER)

def handle_click(board: str, index: int, button: int) -> str:
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
        board_list = list(board)
        board_list[index] = '-'  # Remove the piece if clicked again
        board = ''.join(board_list)
    return board

def main():
    board = MOVE_MANAGER.get_empty_board()  # Initialize empty board
    display_territory = False  # Toggle flag for showing territory
    pass_indicator = False # Toggle flag for the pass indicator
    running = True
    while running:
        DRAWING_OBJECT.draw_board(board)
        if display_territory:
            DRAWING_OBJECT.draw_territory(board)
        if pass_indicator:
            DRAWING_OBJECT.draw_pass_indicator()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                index = DRAWING_OBJECT.get_cell_index(pos)
                board = handle_click(board, index, event.button)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Toggle territory view with spacebar
                    display_territory = not display_territory
                if event.key == pygame.K_p:
                    pass_indicator = not pass_indicator
                

if __name__ == "__main__":
    main()