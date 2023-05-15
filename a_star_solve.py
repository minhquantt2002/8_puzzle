from queue import PriorityQueue


class Node:
    def __init__(self, state, parent, action, cost, heuristic):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic
    # Hàm so sánh 2 node dựa trên tổng chi phí và heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def a_star_search(initial_state, goal_state, get_successors, heuristic):
    # Khởi tạo node ban đầu
    initial_node = Node(initial_state, None, None, 0,
                        heuristic(initial_state, goal_state))

    # Tạo hàng đợi ưu tiên và thêm node ban đầu vào
    frontier = PriorityQueue()
    frontier.put(initial_node)

    # Tạo set để lưu trạng thái đã duyệt
    explored = set()
    l = 0
    while not frontier.empty():
        # Lấy node có chi phí thấp nhất từ hàng đợi ưu tiên
        current_node = frontier.get()
        l += 1
        # Kiểm tra xem node hiện tại có phải là trạng thái đích
        if current_node.state == goal_state:
            path = []
            while current_node.parent is not None:
                path.append(current_node.action)
                current_node = current_node.parent
            path.reverse()
            return path, l

        # Thêm node hiện tại vào set đã duyệt
        explored.add(current_node.state)

        # Lấy các node con của node hiện tại
        successors = get_successors(current_node.state)

        # Duyệt qua các node con
        for action, state, cost in successors:
            # Kiểm tra xem trạng thái đã được duyệt chưa
            if state in explored:
                continue

            # Tạo node mới
            new_node = Node(state, current_node, action,
                            current_node.cost + cost, heuristic(state, goal_state))

            # Thêm node mới vào hàng đợi ưu tiên
            frontier.put(new_node)

    # Nếu không tìm được đường đi tới trạng thái đích, trả về None
    return None

# Define function to get successors


def get_successors(state):
    successors = []
    zero_index = state.index(9)

    # Move up
    if zero_index >= 3:
        new_state = list(state)
        new_state[zero_index], new_state[zero_index -
                                         3] = new_state[zero_index-3], new_state[zero_index]
        successors.append(('up', tuple(new_state), 1))

    # Move down
    if zero_index <= 5:
        new_state = list(state)
        new_state[zero_index], new_state[zero_index +
                                         3] = new_state[zero_index+3], new_state[zero_index]
        successors.append(('down', tuple(new_state), 1))

    # Move left
    if zero_index % 3 != 0:
        new_state = list(state)
        new_state[zero_index], new_state[zero_index -
                                         1] = new_state[zero_index-1], new_state[zero_index]
        successors.append(('left', tuple(new_state), 1))

    # Move right
    if zero_index % 3 != 2:
        new_state = list(state)
        new_state[zero_index], new_state[zero_index +
                                         1] = new_state[zero_index+1], new_state[zero_index]
        successors.append(('right', tuple(new_state), 1))

    return successors


def a_star(initial_state):
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 9)

    def heuristic(state, goal_state):
        count = 0
        for i in range(len(state)):
            if state[i] != goal_state[i]:
                count += 1
        return count
    return a_star_search(initial_state, goal_state, get_successors, heuristic)
