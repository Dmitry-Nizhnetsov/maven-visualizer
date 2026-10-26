import sys
from .config import parse_args, print_config, ConfigError
from .graph import build_dependency_graph, read_test_graph, GraphError
from .visualizer import generate_graphviz, print_ascii_tree


def main():
    """Точка входа (Этапы 3 и 5)."""
    try:
        args = parse_args()
    except ConfigError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    print_config(args)

    try:
        if args.test_mode:
            print(f"\nЧитаем тестовый граф из {args.test_repo}...")
            graph = read_test_graph(args.test_repo)
        else:
            print(f"\nСтроим граф для {args.package} (это может занять время)")
            graph = build_dependency_graph(args.repo, args.package)
    except GraphError as e:
        print(f"Ошибка графа: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nГраф успешно построен!")

    if args.ascii_tree:
        print("\nДерево зависимостей:")
        print_ascii_tree(graph, args.package)

    dot_filename = "dependencies.dot"
    msg = generate_graphviz(graph, dot_filename)
    print(f"\n{msg}")
    print("Вы можете открыть этот файл в Graphviz (или на edotor.net).")


if __name__ == "__main__":
    main()