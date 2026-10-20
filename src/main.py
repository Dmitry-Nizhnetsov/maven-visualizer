import sys
from .config import parse_args, print_config, ConfigError
from .maven import get_direct_dependencies, MavenError


def main():
    """Точка входа в программу."""
    try:
        args = parse_args()
    except ConfigError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    print_config(args)

    if args.test_mode:
        print(f"\nТестовый режим: {args.test_repo}")
        print("Прямые зависимости будут прочитаны на Этапе 3.")
        return

    print(f"\nЗапрашиваем данные для {args.package}...")

    try:
        deps = get_direct_dependencies(args.repo, args.package)
    except MavenError as e:
        print(f"Ошибка Maven: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\nПрямые зависимости ({len(deps)}):")
    if len(deps) == 0:
        print("  (нет зависимостей)")
    else:
        for dep in deps:
            print(f"  {dep.full_name()}")


if __name__ == "__main__":
    main()