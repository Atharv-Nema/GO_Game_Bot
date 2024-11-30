from game_implementation.rules_implementation import MoveManager
from game_bots.bot import Bot
import numpy as np

class MCTSNode:
    def __init__(self, board: str, other_pass: bool, my_piece, move_manager: MoveManager, is_terminal = False, result = None):
        self.C = 2
        self.Q = 0
        self.N = 0
        self.is_terminal = False
        self.board = board
        self.move_manager = move_manager
        self.other_pass = other_pass
        self.my_piece = my_piece
        self.children_nodes: dict[int, MCTSNode] = dict() # From moves to children nodes
        self.is_expanded = False
        if is_terminal:
            self.is_terminal = True
            self.Q = result
            return
    
    def simulate_game(self, heuristic):
        # Instead of simulating the game, I just use the heuristic function
        if self.is_terminal:
            self.N += 1
            return self.Q
        result = heuristic(self.board, self.my_piece, self.other_pass) # Note: heuristic lies in [-1, 1]
        self.Q = self.Q - (result - self.Q) / (self.N + 1)
        self.N += 1
        return result
        
    
    def expand(self, heuristic) -> tuple[float, int]:
        if self.N != 1:
            breakpoint()
        if self.is_terminal:
            raise ValueError("Trying to expand a terminal node")
        
        if self.is_expanded:
            raise ValueError("Already expanded")
        else:
            self.is_expanded = True
            # Expand the node
            valid_moves = self.move_manager.get_next_moves(self.board, self.my_piece)
            other_piece = 'x' if self.my_piece == 'o' else 'o'

            # Case 1: other_pass is true
            if self.other_pass:
                territory_str = self.move_manager.create_territory(self.board)
                ct = 0
                for ch in territory_str:
                    if ch == '-':
                        continue
                    elif ch == self.my_piece:
                        ct += 1
                    else:
                        ct -= 1
                if ct > 0:
                    # We have won, the only move that needs to be made is to play pass
                    # To represent this, we add a terminal child to ourselves, and return 1
                    terminal_node = MCTSNode(self.board, True, other_piece, self.move_manager, True, -1) # As the other guy has lost
                    terminal_node.simulate_game(heuristic)
                    self.children_nodes = dict()
                    self.children_nodes[-1] = terminal_node
                    self.Q = 1 # I won
                    self.N += 1
                    return (1, 1) # We did one trial ig
                
                elif ct == 0:
                    terminal_node = MCTSNode(self.board, True, other_piece, self.move_manager, True, 0) # Draw
                    self.children_nodes[-1] = terminal_node
                
                else:
                    terminal_node = MCTSNode(self.board, True, other_piece, self.move_manager, True, 1) # Opponent lost
                    self.children_nodes[-1] = terminal_node

            # Case 2: other_pass is not true
            else:
                node = MCTSNode(self.board, True, other_piece, self.move_manager)
                self.children_nodes[-1] = node
            
            for move in valid_moves:
                new_board = self.move_manager.make_move(self.board, move, self.my_piece)
                node = MCTSNode(new_board, False, other_piece ,self.move_manager)
                self.children_nodes[move] = node
            
            # Now, I will choose all the children and update their heuristic stuff
            simul_results = 0
            for move in self.children_nodes:
                # Simulate the child stuff for all of these moves
                simul_results += self.children_nodes[move].simulate_game(heuristic)
            N_extra = len(self.children_nodes)
            # Update my own stuff
            self.Q = (self.Q * self.N + simul_results) / (N_extra + self.N)
            return (simul_results / N_extra, N_extra)

    def get_choosing_preference(self, N_parent):
        self.N != 0
        # Why the - sign? Because it is always the parent that calls and it wants the worst state for us
        return -self.Q + self.C * ((np.log(N_parent) / self.N) ** 0.5)
    
    def simulate(self, heuristic) -> tuple[float, int]:
        '''Returns the result of the simulation'''
        if self.N == 0:
            breakpoint()

        if self.is_terminal:
            self.N += 1
            return (self.Q, 1)
        
        if not self.is_expanded:
            ans = self.expand(heuristic)
            self.is_expanded = True
            return ans
        else:
            # Choose the node to explore based on the heuristic
            Max = None
            max_move = None
            for move in self.children_nodes:
                child_preference = self.children_nodes[move].get_choosing_preference(self.N)
                if Max is None or Max < child_preference:
                    Max = child_preference
                    max_move = move
            assert Max is not None
            # Now just simulate that node lah
            (Q_new, N_extra) = self.children_nodes[max_move].simulate(heuristic)
            self.Q = (self.Q * self.N + (-Q_new) * N_extra) / (N_extra + self.N)
            self.N = self.N + N_extra
            return (-Q_new, N_extra)

class HeuristicMCTSBot(Bot):
    '''
    This bot implements MCTS. However, instead of random simulations, it uses a heuristic to evaluate
    the outcome
    '''
    def __init__(self, move_manager: MoveManager, my_piece):
        self.previous_states = set()
        self.move_manager: MoveManager = move_manager
        self.my_piece = my_piece
        self.mcts_tree = MCTSNode(move_manager.get_empty_board(), False, 'x', move_manager)
        self.mcts_tree.simulate_game(self.heuristic)

    def heuristic(self, board: str, my_piece: str, other_pass: bool):
        # For now, I will just use the territories count
        territory_str = self.move_manager.create_territory(board)
        ct = 0
        for i in territory_str:
            if i == '-':
                ct += 0
            elif i == my_piece:
                ct += 1
            else:
                ct -= 1
        if ct > 0 and other_pass:
            return 1 # Because we can just pass and we win
        return 2 / (1 + np.exp(-ct)) - 1
        
    def make_move(self, board: str, other_pass: bool) -> int:
        '''Returns the move to make based on the mcts'''
        if not ('x' not in board and 'o' not in board and other_pass == False):
            if not self.mcts_tree.is_expanded:
                self.mcts_tree.expand(self.heuristic)

            # Now, find the child node that is the node that is resulting in the (board, other_pass pair)

            child_nodes = self.mcts_tree.children_nodes
            for move in child_nodes:
                if child_nodes[move].my_piece != self.my_piece:
                    breakpoint()
                if child_nodes[move].board == board and child_nodes[move].other_pass == other_pass:
                    # Yay, we have found the node
                    self.mcts_tree = child_nodes[move]
                    break
            else:
                assert ValueError("Something has gone wrong")
        
        # Now just do MCTS simulations
        N_SIMULS = 500
        for _ in range(N_SIMULS):
            self.mcts_tree.simulate(self.heuristic)
        
        # Now choose the move
        child_nodes = self.mcts_tree.children_nodes
        best_move = None
        best_val = -1e10
        for move in child_nodes:
            if -child_nodes[move].Q > best_val:
                best_val = -child_nodes[move].Q
                best_move = move
        assert best_move is not None
        self.mcts_tree = child_nodes[best_move]
        return best_move 
    
    def receive_result(self, result: str):
        pass

