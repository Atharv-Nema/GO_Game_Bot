from game_implementation.rules_implementation import MoveManager
from game_bots.bot import Bot
from display_class import VisualInterface
import pygame
import sys
import time

class HumanBot(Bot):
    '''This is a bot that implements a simple minimax strategy'''
    def __init__(self, move_manager, my_piece):
        self.move_manager: MoveManager = move_manager
        self.my_piece = my_piece
        self.previous_states: set = set()
        self.drawing_obj = VisualInterface(move_manager)
        
    def make_move(self, board: str, other_pass: bool) -> int:
        self.previous_states.add(board)
        running = True
        display_territory = False
        while running:
            self.drawing_obj.draw_board(board)
            if other_pass:
                self.drawing_obj.draw_pass_indicator()
            pygame.display.flip()

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    index = self.drawing_obj.get_cell_index(pos)
                    if self.move_manager.is_valid_move(board, index, self.my_piece):
                        new_board = self.move_manager.make_move(board, index, self.my_piece)
                        if new_board in self.previous_states:
                            print("KO happened")
                            continue
                        self.drawing_obj.draw_board(new_board)
                        self.previous_states.add(new_board)
                        # If you make a move, you cannot interact with the screen until the opponent has made a move
                        # May fix this using concurrency
                        pygame.display.flip()
                        return index
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Toggle territory view with spacebar
                        display_territory = not display_territory
                    
                    if event.key == pygame.K_p:
                        # This indicates an intention to pass
                        if other_pass:
                            # The game is over, I can now calculate the state and display the correct message
                            #TODO: Complete this
                            territory_str = self.move_manager.create_territory(board)
                            ct = 0
                            for i in territory_str:
                                if i == '-':
                                    ct += 0
                                elif i == self.my_piece:
                                    ct += 1
                                else:
                                    ct -= 1
                            if ct > 0:
                                self.drawing_obj.display_result("You won")
                            elif ct < 0:
                                self.drawing_obj.display_result("Bot won")
                            else:
                                self.drawing_obj.display_result("Draw")
                            
                        else:
                            self.drawing_obj.draw_pass_indicator()
                        pygame.display.flip()
                        time.sleep(2)
                        return -1

