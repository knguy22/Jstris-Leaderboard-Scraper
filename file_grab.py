import requests

# Grabs all files from internet
def cheese_file(url):
    # cheese.txt is how all of the cheese page's data will be stored
    r = requests.get(url)
    filename = open("cheese.txt", "w", encoding="utf-8")
    filename.write(r.text)
    filename.close()

def leaderboards_file(game, mode, offset, writeorappend):
    # game:
    # 1 = sprint, 3 = cheese, 4 = survival, 5 = ultra

    # mode: (for sprint/cheese)
    # 1 = 40L/10L, 2 = 20L/18L, 3 = 100L, 4 = 1000L
    # any other gamemode should be 1

    # offset:
    # offset of users

    url = "https://jstris.jezevec10.com/api/leaderboard/" + game + "?mode=" + mode + "&offset=" + offset

    response = requests.get(url)
    data = response.text.encode().decode()

    filename = open("leaderboard.txt", writeorappend)
    filename.write(data + "\n")
    filename.close()
