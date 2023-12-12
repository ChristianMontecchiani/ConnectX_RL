import numpy as np
import math
import random

from connect4state import ConnectFourState

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def print_tree(self, indent="", last='updown'):
        print(indent, end="")
        if last == 'updown':
            print("└──", end="")
            indent += "    "
        else:
            print("├──", end="")
            indent += "|   "

        print(f"visits: {self.visits}, value: {self.value}, move: {self.state.last_move}")

        child_count = len(self.children)
        for i, child in enumerate(self.children):
            last = 'updown' if i == child_count - 1 else 'leftright'
            child.print_tree(indent, last)

def mcts_search(root, num_iterations=1):
    for _ in range(num_iterations):
        node = root
        count = 0 
        while not node.state.is_terminal():
            count+=1
            if not node.children:
                # Expand the node if it's not fully expanded
                node.print_tree()
                new_node = expand(node)
                if new_node is not None:
                    node = new_node
                else:
                    break

            else:
                # Select the child node with the highest UCB score
                node = select(node)

        # Simulate from the selected node to the end of the game
        result = simulate(node.state)

        # Backpropagate the result through the tree
        backpropagate(node, result)

    # Choose the best move based on the most visited child
    best_child = max(root.children, key=lambda child: child.visits)
    return best_child.state.last_move

def expand(node):
    """Expand by adding a child corresponding to a valid move"""
    valid_moves = node.state.get_valid_moves()
    
    if valid_moves:
        move = random.choice(valid_moves)
        new_state = node.state.copy_and_apply_move(move)
        child = MCTSNode(new_state, parent=node)
        node.children.append(child)
        return child
    else:
        # Handle the case where there are no valid moves left
        return None  # Returning the current node without expansion

def select(node):
    """ Use the Upper Confidence Bound  formula to select a child"""
    exploration_weight = 1.0
    ucb_scores = [child.value / child.visits + exploration_weight * math.sqrt(math.log(node.visits) / child.visits)
                if child.visits > 0 else float('inf') for child in node.children]
    selected_child = node.children[np.argmax(ucb_scores)]
    return selected_child

def simulate(state):
    # Simulate the game from the current state until a terminal state is reached
    while not state.is_terminal():
        valid_moves = state.get_valid_moves()
        move = random.choice(valid_moves)
        state = state.copy_and_apply_move(move)
    return state.get_result()

def backpropagate(node, result):
    # Backpropagate the result through the tree
    while node is not None:
        node.visits += 1
        node.value += result
        node = node.parent



if __name__ == "__main__":
    game_state = ConnectFourState()
    root_node = MCTSNode(game_state)

    while not game_state.is_terminal():
        # Use MCTS to find the best move
        best_move = mcts_search(root_node, num_iterations=100)

        # Apply the best move to the current state
        game_state.make_move(best_move)

        # Update the root node for the next iteration
        root_node = next((child for child in root_node.children if child.state.last_move == best_move), None)

        # Print the current state of the game
        print(game_state.board)

    winner = game_state.check_winner()
    if winner:
        print(f"Player {winner} wins!")
    else:
        print("It's a tie!")
