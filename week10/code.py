# --- Alpha-Beta Pruning Implementation ---

import math

# Minimax with Alpha-Beta Pruning
def alphabeta(depth, node_index, maximizing_player, values, alpha, beta, max_depth):
    """
    depth: current depth in the game tree
    node_index: index of the current node in the list of values
    maximizing_player: boolean, True if it's the maximizing player's turn
    values: list of terminal node values
    alpha, beta: alpha-beta values for pruning
    max_depth: maximum depth of the tree
    """
    # Base case: if we reach the leaf node
    if depth == max_depth:
        return values[node_index]

    if maximizing_player:
        best = -math.inf
        # Explore left and right child
        for i in range(2):
            val = alphabeta(depth + 1, node_index * 2 + i, False, values, alpha, beta, max_depth)
            best = max(best, val)
            alpha = max(alpha, best)
            # Prune
            if beta <= alpha:
                break
        return best
    else:
        best = math.inf
        # Explore left and right child
        for i in range(2):
            val = alphabeta(depth + 1, node_index * 2 + i, True, values, alpha, beta, max_depth)
            best = min(best, val)
            beta = min(beta, best)
            # Prune
            if beta <= alpha:
                break
        return best

# --- Example Game Tree ---

# Terminal node values (leaf nodes)
values = [3, 5, 6, 9]

# Tree depth = log2(len(values)) = 2
max_depth = 2

# Run alpha-beta pruning
best_value = alphabeta(0, 0, True, values, -math.inf, math.inf, max_depth)

print("1BM23CS304 Sarim")
print(f"The optimal value is: {best_value}")
