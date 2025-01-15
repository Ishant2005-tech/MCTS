from config.config import *
from utils.utils import Node
import numpy as np

def UCB1(node:Node, c = 2):
    """
    Calculates the UCB1 score for a node.

    The UCB1 score is a way to balance exploration and exploitation in a tree search.
    It is calculated as the average value of the node plus a bonus term that rewards
    nodes that have not been visited as much.

    Parameters
    ----------
    node : Node
        The node to calculate the score for.
    c : float, default = 2
        The exploration bonus parameter. A higher value of c will result in more
        exploration and less exploitation.

    Returns
    -------
    float
        The UCB1 score for the node.
    """
    if node is None:
        return 0
    if node.visits == 0:
        return np.inf
    return node.avg + c * np.sqrt(2 * np.log(node.parent.visits) / node.visits)
