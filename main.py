from datetime import datetime

from aiohttp import web


def write_to_file(client_ip, access_date):
    with open("visits.txt", "a", encoding="utf-8") as f:
        f.write(f"{client_ip} {access_date}\n")


def api_visits_day(day):
    with open("visits.txt", "r", encoding="utf-8") as f:
        line = f.readline().strip()
        visits = 0
        while line:
            client_ip, access_date = line.split(" ")
            if access_date == day:
                visits += 1
            line = f.readline().strip()
    return visits


def api_visits_month(month):
    with open("visits.txt", "r", encoding="utf-8") as f:
        line = f.readline().strip()
        visits = 0
        while line:
            client_ip, access_date = line.split(" ")
            if access_date[:7] == month:
                visits += 1
            line = f.readline().strip()
    return visits


def api_visits_year(year):
    with open("visits.txt", "r", encoding="utf-8") as f:
        line = f.readline().strip()
        visits = 0
        while line:
            client_ip, access_date = line.split(" ")
            if access_date[:4] == year:
                visits += 1
            line = f.readline().strip()
    return visits


def api_visits_all():
    with open("visits.txt", "r", encoding="utf-8") as f:
        line = f.readline()
        visits = 0
        while line:
            visits += 1
            line = f.readline()
    return visits


def api_uniq_visits_day(ip, day):
    with open("visits.txt", "r", encoding="utf-8") as f:
        line = f.readline().strip()
        visits = 0
        while line:
            client_ip, access_date = line.split(" ")
            if access_date == day and client_ip == ip:
                visits += 1
            line = f.readline().strip()
    return visits


def api_uniq_visits_month(ip, month):
    with open("visits.txt", "r", encoding="utf-8") as f:
        line = f.readline().strip()
        visits = 0
        while line:
            client_ip, access_date = line.split(" ")
            if access_date[:7] == month and client_ip == ip:
                visits += 1
            line = f.readline().strip()
    return visits


def api_uniq_visits_year(ip, year):
    with open("visits.txt", "r", encoding="utf-8") as f:
        line = f.readline().strip()
        visits = 0
        while line:
            client_ip, access_date = line.split(" ")
            if access_date[:4] == year and client_ip == ip:
                visits += 1
            line = f.readline().strip()
    return visits


def api_uniq_visits_all(ip):
    with open("visits.txt", "r", encoding="utf-8") as f:
        line = f.readline()
        visits = 0
        while line:
            client_ip, access_date = line.split(" ")
            if client_ip == ip:
                visits += 1
            line = f.readline()
    return visits


visits = api_visits_all()


async def handle(request):
    client_ip = request.remote
    access_date = datetime.now().strftime('%Y-%m-%d')
    write_to_file(client_ip, access_date)
    global visits
    visits += 1
    return web.Response(text=f"Сайт посетили {visits} раз(а)")


app = web.Application()
app.router.add_get('/', handle)
web.run_app(app)

