import sys
from .config import parse_args, print_config, ConfigError
from .graph import build_dependency_graph, read_test_graph, GraphError


def main():
    """Точка входа для Этапа 3."""
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

    print("\nГраф успешно построен! Результат:")
    for node, children in graph.items():
        print(f"  {node} -> {children}")


if __name__ == "__main__":
    main()