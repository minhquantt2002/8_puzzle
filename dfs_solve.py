def dfs(start, goal):
    visited = set()
    stack = [(start, [])]

    l = 0
    while stack:
        l += 1
        node, path = stack.pop()
        if node == goal:
            return path, l
        visited.add(tuple(node))
        for move, next_node in get_neighbors(node):
            l += 1
            if tuple(next_node) not in visited:
                stack.append((next_node, path + [move]))
    return []


def swap(node, i, j):
    new_node = node.copy()
    new_node[i], new_node[j] = new_node[j], new_node[i]
    return new_node


def get_neighbors(node):
    neighbors = []
    zero_idx = node.index(9)

    if zero_idx not in [0, 1, 2]:
        neighbors.append(('up', swap(node, zero_idx, zero_idx - 3)))
    if zero_idx not in [6, 7, 8]:
        neighbors.append(('down', swap(node, zero_idx, zero_idx + 3)))
    if zero_idx not in [0, 3, 6]:
        neighbors.append(('left', swap(node, zero_idx, zero_idx - 1)))
    if zero_idx not in [2, 5, 8]:
        neighbors.append(('right', swap(node, zero_idx, zero_idx + 1)))
    return neighbors