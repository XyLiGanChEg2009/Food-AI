def log(*kwargs):
    print(*kwargs)
    with open("result.txt", "a", encoding="utf-8") as f:
        f.write("\n" + " ".join(list(map(str, kwargs))))


def init_log():
    with open("result.txt", "w", encoding="utf-8") as f:
        f.close()