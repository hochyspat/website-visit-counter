import sys

from aiohttp import web

from visit_counter import VisitCounter


def main():
    app = web.Application()
    counter = VisitCounter()

    app.router.add_get("/", counter.handle)

    host = input(
        "Введите ip-адрес хоста:"
        "(например, 127.0.0.1, 0.0.0.0, или локальный IP)"
    ).strip()
    print("сервер: http://<введенный ip>:8080")

    try:
        web.run_app(app, host=host, port=8080)
    except OSError as e:
        print(f"Ошибка запуска сервера: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
