from config.config import *

def indices_from_move(move):
    move -= 1
    return move // BOARD_SIZE, move % BOARD_SIZE


class Node:
    def __init__(self, parent = None, action = None, level = None):
        self.children: list[Node] = []
        self.parent: Node = parent
        if level is None and parent is not None and parent.level is not None:
            self.level = parent.level + 1
        else:
            self.level = level
        self.action = action
        self.wins = 0
        self.visits = 0
    @property
    def avg(self):
        if self.visits == 0:
            return 0
        return self.wins / self.visits

    @property
    def is_leaf(self):
        return self.children == []

    @property
    def is_root(self):
        return self.parent is None
    

def display_in_order(node: Node):
    if node.is_leaf:
        # print('leaf')
        return
    for child in node.children:
        display_in_order(child)
        print(f'child.wins: {child.wins}, child.visits: {child.visits}, child.action: {child.action}')

    print(f'node.wins: {node.wins}, node.visits: {node.visits}, node.action: {node.action}')

def display_as_tree(node: Node, return_dict:dict):
    if node.is_leaf:
        return return_dict
    for child in node.children:
        return_dict.update(display_as_tree(child, return_dict))
        if child.level not in return_dict:
            return_dict[child.level] = []
        return_dict[child.level].append('*')


    if node.level not in return_dict:
        return_dict[node.level] = []
    return_dict[node.level].append('*')

    return return_dict


    """
    BFS
    """
    # visited = dict()
    # visited[node] = True
    # print('* ')
    # queue = [node]
    # while len(queue) > 0:
    #     node = queue.pop(0)
    #     for child in node.children:
    #         if not visited.get(child):
    #             print('* ', end='')
    #             visited[child] = True
    #             # print(f'({child.action})')
    #             queue.append(child)
        
    
if __name__ == "__main__":
    print('Hello')