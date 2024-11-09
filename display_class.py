import pygame
from game_implementation.rules_implementation import MoveManager

class VisualInterface:
    cell_size = 60

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    LINE_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = (210, 180, 140)
    PIECE_RADIUS = cell_size // 2 - 5
    TERRITORY_ALPHA = 128  # Semi-transparent alpha for territory
    PASS_INDICATOR_RADIUS = 10  # Radius of the pass indicator


    def __init__(self, move_manager: MoveManager):
        '''Initializes the visual interface'''
        self.move_manager = move_manager

        # Initialize pygame
        pygame.init()

        # Set up display
        self.board_size = move_manager.BOARD_SIZE
        self.width = self.board_size * self.cell_size
        self.height = self.board_size * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Go Board")

        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.result_font = pygame.font.Font(None, 72)

    def display_result(self, result: str):
        # Fill screen with background color
        self.screen.fill(self.BACKGROUND_COLOR)

        # Render winner text
        text_surface = self.result_font.render(result, True, self.RED)

        # Center the text on the screen
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_pass_indicator(self):
        """
        Draws a small blue dot in the bottom-right corner to indicate that a player has passed.
        """
        # Position for the pass indicator in the bottom-right corner
        x = self.width - self.cell_size // 4
        y = self.height - self.cell_size // 4
        pygame.draw.circle(self.screen, self.BLUE, (x, y), self.PASS_INDICATOR_RADIUS)

    def draw_territory(self, board: str):
        """
        Takes in the board and draws the territories
        """
        territory_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Create a transparent surface
        for i in range(self.board_size * self.board_size):
            row, col = divmod(i, self.board_size)
            x = col * self.cell_size + self.cell_size // 2
            y = (self.board_size - 1 - row) * self.cell_size + self.cell_size // 2  # Adjust for Go's coordinate system
            territory_str = self.move_manager.create_territory(board)
            if territory_str[i] == 'x':  # Black territory
                pygame.draw.circle(territory_surface, (0, 0, 0, self.TERRITORY_ALPHA), (x, y), self.PIECE_RADIUS)
            elif territory_str[i] == 'o':  # White territory
                pygame.draw.circle(territory_surface, (255, 255, 255, self.TERRITORY_ALPHA), (x, y), self.PIECE_RADIUS)

        # Blit the territory surface onto the screen
        self.screen.blit(territory_surface, (0, 0))

    def draw_board(self, board: str):
        """
        Takes in the board and draws it
        Parameters:
        board (Board): The board
        """
        self.screen.fill(self.BACKGROUND_COLOR)

        # Draw grid lines
        for i in range(self.board_size):
            pygame.draw.line(self.screen, self.LINE_COLOR, (i * self.cell_size + self.cell_size // 2, self.cell_size // 2), 
                            (i * self.cell_size + self.cell_size // 2, self.height - self.cell_size // 2), 2)
            pygame.draw.line(self.screen, self.LINE_COLOR, (self.cell_size // 2, i * self.cell_size + self.cell_size // 2), 
                            (self.width - self.cell_size // 2, i * self.cell_size + self.cell_size // 2), 2)

        # Draw pieces
        for i in range(self.board_size * self.board_size):
            cell = board[i]
            row, col = divmod(i, self.board_size)
            x = col * self.cell_size + self.cell_size // 2
            y = (self.board_size - 1 - row) * self.cell_size + self.cell_size // 2  # Adjusted for Go's coordinate system

            if cell == 'x':  # Black piece
                pygame.draw.circle(self.screen, self.BLACK, (x, y), self.PIECE_RADIUS)
            elif cell == 'o':  # White piece
                pygame.draw.circle(self.screen, self.WHITE, (x, y), self.PIECE_RADIUS)
                pygame.draw.circle(self.screen, self.BLACK, (x, y), self.PIECE_RADIUS, 2)  # Outline for white piece

        # Draw labels
        for i in range(self.board_size):
            # Draw numbers for rows (1 at the bottom, 9 at the top)
            text_surface = self.font.render(str(self.board_size - i), True, self.RED)
            self.screen.blit(text_surface, (0, i * self.cell_size + self.cell_size // 2 - text_surface.get_height() // 2))

            # Draw numbers for columns
            text_surface = self.font.render(chr(ord('A') + i), True, self.RED)
            self.screen.blit(text_surface, (i * self.cell_size + self.cell_size // 2 - text_surface.get_width() // 2, 0))

    def get_cell_index(self, pos: tuple[float, float]) -> int:
        """
        Takes in the position of the mouse and calculates the board's 1D index
        Parameters:
        pos (tuple[float, float]): The 2D pygame coordinates of the mouse pointer
        Returns:
        The 1D board index
        """
        x, y = pos
        row = self.board_size - 1 - (y // self.cell_size)  # Adjust for Go's coordinate system
        col = x // self.cell_size
        return row * self.board_size + col

