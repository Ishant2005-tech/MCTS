from copy import deepcopy
from config.config import *
from utils.utils import Node, display_in_order, display_as_tree
from utils.UCB1 import UCB1
from src.board import TTTBoard
import numpy as np
# rng = np.random.default_rng(RNG_SEED)
np.random.seed(RNG_SEED)

class RandomAgent:
    def __init__(self):
        self.name = "RandomAgent"

    def get_move(self, board: TTTBoard):
        if board.is_game_over():
            return
        return np.random.choice(board.available_moves)

class MCTS:
    def __init__(self, board:TTTBoard):
        self.root = Node(level=0)
        self.board = board

    def select(self, node:Node):
        if node.is_leaf:
            if node.visits == 0:
                node.visits += 1
                print("visits = 0")
                node.action = np.random.choice(self.board.available_moves)
                print("action: ", node.action)
                # print(len(self.board.available_moves))
                # print(type(node))
                return node
            else:
                print("expanding")
                # print(len(self.board.available_moves))
                for action in self.board.available_moves:
                    child = Node(parent = node, action = action)
                    node.children.append(child)
                
                selected_node = node.children[0]
                selected_node.visits += 1
                return selected_node
        
        UCB1_values = [UCB1(child) for child in node.children]
        print("UCB1_values: ", UCB1_values)
        print("Actions: ", [child.action for child in node.children])
        best_scoring_child = node.children[np.argmax(UCB1_values)]
        # print("best_scoring_child.avg: ", best_scoring_child.avg)
        return self.select(best_scoring_child)

    def expand(self):
        pass
    def simulate(self, node: Node):
        board = deepcopy(self.board)
        board.play_turn(node.action)
        board.display()

        while True:
            if board.is_game_over():
                if board.outcome == O:
                    node.wins -= O
                break            
            move = np.random.choice(board.available_moves)
            board.play_turn(move)
            board.display()
        print("Outcome:", board.outcome)
        return board.outcome

    def backpropagate(self, node:Node):
        
        wins = node.wins
        
        while not node.is_root:
            node.parent.wins+=wins
            node = node.parent
            node.visits+=1

    def loop(self, max_iterations = 10):
        itr = 0
        while itr < max_iterations:
            itr += 1
            selected_node = self.select(self.root)

            self.simulate(selected_node)
            self.backpropagate(selected_node)
            print("selected node.visits: ", selected_node.visits, "selected_node.wins: ", 
                  selected_node.wins, "selected_node.action: ", selected_node.action)
            
        
    def evaluate_tree(self):
        path = [self.root]
        paths_dict = dict()
        self.dfs(self.root, paths_dict, path)
        return paths_dict

    def dfs(self, node:Node, paths_dict: dict, path: list, path_wins = 0):   
        if node.is_leaf:
            tuple_path = tuple(path)
            paths_dict[tuple_path] = path_wins
        # path.append(node)
        for child in node.children:
            self.dfs(child, paths_dict, path + [child], path_wins + child.wins)


class MCTSagent:
    def __init__(self):
        self.name = "MCTSagent"
        self.root = Node(level=0)
    
    def get_move(self, board: TTTBoard):
        algo = MCTS(board)
        algo.loop()
        return algo.evaluate_tree()
        

if __name__ == "__main__":
    board = TTTBoard()
    agent = MCTSagent()
    board.play_turn(2)
    # board.board[1][1] = X
    test = MCTS(board=board)
    test.loop()
    # display_in_order(test.root)
    return_dict = dict()
    return_dict = display_as_tree(test.root, return_dict)
    # print(return_dict)
    return_list = [0] * len(return_dict)
    for key in return_dict:
        return_list[key] = (return_dict[key])
    
    # for i in return_list:
    #     print(i, len(i))

    paths_dict = test.evaluate_tree()
    # print(paths_dict)
    maximum = -np.inf
    best_path = None
    for key, value in paths_dict.items():
        if value > maximum:
            maximum = value
            best_path = [i.action for i in key]
    
    print("Best path: ", best_path, "with value: ", maximum)

    print("Available moves: ", test.board.available_moves)
    breakpoint()