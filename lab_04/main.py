print("Задание 1")

tree = {
    "Завод": ["Основное производство", "Логистика", "Техническая служба"],
    "Основное производство": ["Литейный цех", "Сборочный цех"],
    "Логистика": ["Склад готовой продукции", "Транспортный отдел"],
    "Сборочный цех": ["Участок монтажа"],
    "Техническая служба": [],
    "Литейный цех": [],
    "Склад готовой продукции": [],
    "Транспортный отдел": [],
    "Участок монтажа": [],
}

def children(tree, node):
    return [c for c in tree.get(node,[]) if c in tree]

def get_leaves(tree, node, acc=None):
    if acc is None:
        acc=[]
    kids=children(tree,node)
    if not kids:
        acc.append(node)
        return acc
    for child in kids:
        get_leaves(tree,child, acc)
    return acc

def tree_height(tree,node):
    kids=children(tree,node)
    if not kids: return 0
    return 1+max(tree_height(tree,c) for c in kids)

def find_path(tree, target, node="Завод", path=None):
    if path is None:
        path = [node]
    if target in tree.get(node,[]):
        return path+[target]
    for child in children(tree, node):
        found = find_path(tree,target, child,path+[child])
        if found:
            return found
    return None

print(find_path(tree, 'Участок монтажа'))

print("Задание 2")

keys = [45, 25, 65, 15, 35, 55, 75, 60]
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(node, key):
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left, key)
    elif key > node.key:
        node.right = insert(node.right, key)
    return node

def inorder(node, acc=None):
    if acc is None:
        acc = []
    if node is None:
        return acc
    inorder(node.left, acc)
    acc.append(node.key)
    inorder(node.right, acc)
    return acc

class BST:
    def __init__(self):
        self.root = None                 
    def insert(self, key):
        self.root = insert(self.root, key)   # та же функция insert
    def search(self, key):
        return search(self.root, key)

def search(node, key, visited=None):
    if visited is None:
        visited = []
    if node is None:
        return False, visited
    visited.append(node.key)
    if key == node.key:
        return True, visited
    if key < node.key:
        return search(node.left, key, visited)
    return search(node.right, key, visited)

def bst_height(node):
    if node is None:
        return -1
    return 1 + max(bst_height(node.left), bst_height(node.right))

bst = BST()
for k in keys:
    bst.insert(k)

print(bst.search(60))
print(bst.search(58))
print(bst_height(bst.root))

keys2 = [15, 25, 35, 45, 55, 60, 65, 75]

bst2 = BST()
for k in keys2:
    bst2.insert(k)

print(bst_height(bst2.root))

print("Задание 3")

vertices = ["A", "B", "C", "D", "E", "F", "G"]
edges = [
    ("A", "B"), ("A", "C"),
    ("B", "D"), ("C", "D"),
    ("C", "E"), ("D", "E"),
    ("E", "F"), ("E", "C"),
]

graph= {p:[] for p in vertices}
for u, v in edges:
    graph[u].append(v)

print(graph)

def build_matrix(graph):
    vertices = list(graph)
    index = {v: i for i, v in enumerate(vertices)}
    matrix = [[0] * len(vertices) for _ in vertices]
    for src, dsts in graph.items():
        for dst in dsts:
            matrix[index[src]][index[dst]] = 1
    return vertices, matrix

p_vertices, p_matrix = build_matrix(graph)
print("       " + " ".join(v[:7].rjust(8) for v in p_vertices))
for i, v in enumerate(p_vertices):
    print(v.ljust(7) + " ".join(str(c).rjust(8) for c in p_matrix[i]))

symmetric = p_matrix == [list(row) for row in zip(*p_matrix)]
target = "C"
idx = p_vertices.index(target)
print(f"исходящих у {target}: ", sum(p_matrix[idx]))
print(f"входящих у {target}: ", sum(row[idx] for row in p_matrix))

def in_out_degrees(graph):
    """Количество входящих и исходящих рёбер каждой вершины."""
    result = {v: [0, len(adj)] for v, adj in graph.items()}
    for adj in graph.values():
        for nb in adj:
            result[nb][0] += 1
    return result

print("вершина   входящие  исходящие")
for v, (inn, out) in in_out_degrees(graph).items():
    print(v.ljust(10), str(inn).center(8), str(out).center(9))

degrees = in_out_degrees(graph)
for v, (inn, out) in degrees.items():
    if inn == 0 and out == 0:
        print("Изолированная вершина:", v)          

from collections import deque

def shortest_path(graph, start, end):
    if start == end:
        return [start]
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nb in graph.get(node, []):
            if nb not in parent:
                parent[nb] = node
                if nb == end:                   
                    route = [end]
                    while parent[route[-1]] is not None:
                        route.append(parent[route[-1]])
                    return list(reversed(route))
                queue.append(nb)
    return None

def has_cycle(graph):
    for u, adj in graph.items():
        for v in adj:                   
            back = shortest_path(graph, v, u) 
            if back is not None:
                return back + [v]     
    return None

cycle = has_cycle(graph)
print("цикл в графе:", " → ".join(cycle) if cycle else None)

print("Задание 4")
for s, t in [("A", "F"), ("A", "G"), ("F", "A")]:
    p = shortest_path(graph, s, t)
    if p:
        print(f"{s} → {t}: {' → '.join(p)}  (переходов: {len(p) - 1})")
    else:
        print(f"{s} → {t}: пути нет")