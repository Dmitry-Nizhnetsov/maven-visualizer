def generate_graphviz(graph, output_path):
    """Генерирует файл .dot для Graphviz."""
    lines = ["digraph Dependencies {"]

    for node, children in graph.items():
        for child in children:
            lines.append(f'    "{node}" -> "{child}";')

    lines.append("}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return f"Граф сохранен в {output_path}"


def print_ascii_tree(graph, start_node, prefix="", is_last=True, visited=None):
    """Выводит граф в виде ASCII-дерева в консоль."""
    if visited is None:
        visited = set()

    if start_node in visited:
        print(f"{prefix}{'└── ' if is_last else '├── '}{start_node} (цикл)")
        return

    print(f"{prefix}{'└── ' if is_last else '├── '}{start_node}")
    visited.add(start_node)

    children = graph.get(start_node, [])
    for i, child in enumerate(children):
        is_last_child = (i == len(children) - 1)
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_ascii_tree(graph, child, new_prefix, is_last_child, visited)