import heapq
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional

State = Tuple[int, ...]  # 9-length tuple representing the board in row-major order
MOVE_DIRS = {
    'U': -3,  # move blank up
    'D':  3,  # move blank down
    'L': -1,  # move blank left
    'R':  1,  # move blank right
}

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    count: int
    state: State = field(compare=False)

def is_solvable(state: State) -> bool:
    """8-puzzle is solvable iff number of inversions is even."""
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv % 2 == 0

def index_to_rc(i: int) -> Tuple[int, int]:
    return divmod(i, 3)  # (row, col)

def rc_to_index(r: int, c: int) -> int:
    return r * 3 + c

def neighbors(state: State) -> List[Tuple[str, State]]:
    """Generate (move, next_state) pairs by sliding a tile into the blank."""
    z = state.index(0)
    zr, zc = index_to_rc(z)
    results = []

    # Up
    if zr > 0:
        t = list(state)
        swap_idx = rc_to_index(zr - 1, zc)
        t[z], t[swap_idx] = t[swap_idx], t[z]
        results.append(('U', tuple(t)))

    # Down
    if zr < 2:
        t = list(state)
        swap_idx = rc_to_index(zr + 1, zc)
        t[z], t[swap_idx] = t[swap_idx], t[z]
        results.append(('D', tuple(t)))

    # Left
    if zc > 0:
        t = list(state)
        swap_idx = rc_to_index(zr, zc - 1)
        t[z], t[swap_idx] = t[swap_idx], t[z]
        results.append(('L', tuple(t)))

    # Right
    if zc < 2:
        t = list(state)
        swap_idx = rc_to_index(zr, zc + 1)
        t[z], t[swap_idx] = t[swap_idx], t[z]
        results.append(('R', tuple(t)))

    return results

def reconstruct_path(parent: Dict[State, Tuple[Optional[State], Optional[str]]],
                     goal: State) -> Tuple[List[State], List[str]]:
    states = []
    moves = []
    cur = goal
    while cur is not None:
        p, m = parent[cur]
        states.append(cur)
        if m is not None:
            moves.append(m)
        cur = p
    states.reverse()
    moves.reverse()
    return states, moves

def uniform_cost_search(start: State, goal: State):
    """Dijkstra/UCS with unit step costs."""
    if not is_solvable(start):
        return None, None, None  # unsolvable

    # g-costs (path cost so far)
    g: Dict[State, int] = {start: 0}
    parent: Dict[State, Tuple[Optional[State], Optional[str]]] = {start: (None, None)}

    # Priority queue of (cost, tie-breaker, state)
    frontier: List[PrioritizedItem] = []
    counter = 0
    heapq.heappush(frontier, PrioritizedItem(0, counter, start))
    counter += 1

    visited = set()

    while frontier:
        node = heapq.heappop(frontier)
        cost, state = node.priority, node.state

        if state in visited:
            continue
        visited.add(state)

        if state == goal:
            path_states, path_moves = reconstruct_path(parent, goal)
            return path_states, path_moves, cost  # optimal

        for move, nxt in neighbors(state):
            new_cost = cost + 1  # unit step cost
            if nxt not in g or new_cost < g[nxt]:
                g[nxt] = new_cost
                parent[nxt] = (state, move)
                heapq.heappush(frontier, PrioritizedItem(new_cost, counter, nxt))
                counter += 1

    return None, None, None  # no solution (shouldn't happen if solvable)

def pretty_print(state: State):
    for r in range(3):
        row = state[r*3:(r+1)*3]
        print(' '.join('_' if x == 0 else str(x) for x in row))
    print()

if __name__ == "__main__":
    # Example:
    # Start state (row-major). 0 denotes blank.
    start = (1, 2, 3,
             4, 0, 6,
             7, 5, 8)

    goal = (1, 2, 3,
            4, 5, 6,
            7, 8, 0)

    states, moves, cost = uniform_cost_search(start, goal)

    if states is None:
        print("This start state is unsolvable.")
    else:
        print(f"Solution found with cost {cost} in {len(moves)} moves:")
        print("Moves:", ' '.join(moves))
        print("\nSequence of states:")
        for s in states:
            pretty_print(s)
