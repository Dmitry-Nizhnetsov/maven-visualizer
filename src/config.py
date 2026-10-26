import argparse


class ConfigError(Exception):
    """Ошибка конфигурации."""
    pass


def create_parser():
    """Создает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Maven Visualizer")

    parser.add_argument(
        "--package", "-p", required=True, help="Имя пакета"
    )
    parser.add_argument(
        "--repo", "-r", default=None, help="URL репозитория"
    )
    parser.add_argument(
        "--test-repo", default=None, help="Путь к тестовому файлу"
    )
    parser.add_argument(
        "--test-mode", action="store_true", help="Тестовый режим"
    )
    parser.add_argument(
        "--ascii-tree", action="store_true", help="Вывод деревом"
    )
    parser.add_argument(
        "--filter", default=None, help="Фильтр (подстрока)"
    )
    parser.add_argument(
        "--output", default="graph.dot", help="Выходной файл Graphviz"
    )
    return parser


def validate_args(args):
    """Проверяет корректность переданных аргументов."""
    if args.test_mode:
        if not args.test_repo:
            raise ConfigError("В режиме --test-mode нужен --test-repo")
    else:
        if not args.repo:
            raise ConfigError("Укажите --repo или включите --test-mode")
        if args.test_repo:
            raise ConfigError("--test-repo работает только с --test-mode")


def parse_args(argv=None):
    """Главная функция разбора аргументов."""
    parser = create_parser()
    args = parser.parse_args(argv)
    validate_args(args)
    return args


def print_config(args):
    """Выводит параметры в формате ключ-значение."""
    print("=" * 40)
    print("Параметры запуска:")
    print(f"  package_name:   {args.package}")
    print(f"  repo_url:       {args.repo}")
    print(f"  test_repo_path: {args.test_repo}")
    print(f"  test_mode:      {args.test_mode}")
    print(f"  ascii_tree:     {args.ascii_tree}")
    print("=" * 40)