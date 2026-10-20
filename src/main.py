import sys
from .config import parse_args, print_config, ConfigError


def main():
    """Точка входа для Этапа 1."""
    try:
        args = parse_args()
    except ConfigError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    print_config(args)

    if args.test_mode:
        print(f"\nТестовый режим: {args.test_repo}")
        return

    print("\nГотово к работе (сбор данных будет на Этапе 2).")


if __name__ == "__main__":
    main()