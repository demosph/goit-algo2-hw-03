import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Створюємо граф
G = nx.DiGraph()

# Додаємо ребра та пропускні здатності (таблиця із завдання)
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

# Додаємо всі ребра до графа
G.add_weighted_edges_from(edges)

# Позиції для малювання графа
pos = {
    "Термінал 1": (2, 2),
    "Термінал 2": (10, 2),
    "Склад 1": (4, 3),
    "Склад 2": (8, 3),
    "Склад 3": (4, 1),
    "Склад 4": (8, 1),
    "Магазин 1": (0, 4),
    "Магазин 2": (2, 4),
    "Магазин 3": (4, 4),
    "Магазин 4": (6, 4),
    "Магазин 5": (8, 4),
    "Магазин 6": (10, 4),
    "Магазин 7": (0, 0),
    "Магазин 8": (2, 0),
    "Магазин 9": (4, 0),
    "Магазин 10": (6, 0),
    "Магазин 11": (8, 0),
    "Магазин 12": (10, 0),
    "Магазин 13": (12, 0),
    "Магазин 14": (14, 0),
}

# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent, node_index_map):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False

# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink, node_index_map):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent, node_index_map):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node

        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow

# Створюємо мапу індексів для вузлів
node_index_map = {node: idx for idx, node in enumerate(G.nodes)}

# Перетворюємо ребра у матрицю пропускних здатностей
num_nodes = len(G.nodes)
capacity_matrix = [[0] * num_nodes for _ in range(num_nodes)]

for u, v, data in G.edges(data=True):
    u_idx = node_index_map[u]
    v_idx = node_index_map[v]
    capacity_matrix[u_idx][v_idx] = data['weight']

# Обчислюємо максимальний потік
source = node_index_map["Термінал 2"]
sink = node_index_map["Магазин 14"]

max_flow = edmonds_karp(capacity_matrix, source, sink, node_index_map)

# Виводимо результат
print(f"Максимальний потік з {list(node_index_map.keys())[source]} до {list(node_index_map.keys())[sink]}: {max_flow}")

# Малюємо граф
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=12, font_weight="bold", arrows=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Відображаємо граф
plt.show()