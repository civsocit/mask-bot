from datetime import datetime


def get_date_and_name():
    d0 = datetime(day=28, month=4, year=2022)
    d1 = datetime.now()

    d_s = d1 - d0
    days = d_s.days

    d_gramar = {
        0: "дней",
        1: "день",
        2: "дня",
        3: "дня",
        4: "дня",
        5: "дней",
        6: "дней",
        7: "дней",
        8: "дней",
        9: "дней",
    }
    return days, d_gramar[days % 10]