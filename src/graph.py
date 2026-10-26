from collections import deque
from .maven import get_direct_dependencies


class GraphError(Exception):
    """Ошибка при построении графа."""
    pass


def build_dependency_graph(repo_url, root_package):
    """Строит граф зависимостей (транзитивных)."""
    graph = {}
    queue = deque([root_package])
    visited = set([root_package])

    while queue:
        current_package = queue.popleft()
        try:
            deps = get_direct_dependencies(repo_url, current_package)
            dep_names = [d.full_name() for d in deps]
            graph[current_package] = dep_names
        except Exception:
            graph[current_package] = []
            continue

        for dep_name in graph[current_package]:
            if dep_name not in visited:
                visited.add(dep_name)
                queue.append(dep_name)

    return graph


def read_test_graph(file_path):
    """Читает тестовый граф из файла (формат A -> B, C)."""
    graph = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "->" in line:
                    parts = line.split("->")
                    node = parts[0].strip()
                    children = [x.strip() for x in parts[1].split(",")]
                    graph[node] = children
    except FileNotFoundError:
        raise GraphError(f"Тестовый файл не найден: {file_path}")
    return graph