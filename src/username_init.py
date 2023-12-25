import io
import requests
import os

# username_init checks if we want to scrape the jstris api leaderboards and outputs a list of usernames
# the usernames are stored in "unorderedname.txt"

def get_usernames(game, mode, filename):
    # Checking if the username file is empty

    fetch_usernames = False

    if os.path.exists(filename) == False:
        f = open(filename, 'x')
        f.close()

    with open(filename, "r", encoding='utf-8') as f:
        list_of_usernames = f.readlines()
        if len(list_of_usernames) < 1:
            fetch_usernames = True

    # gather usernames from jstris api if unorderedname.txt is empty
    # if already have usernames, gather usernames from unorderedname.txt
    if fetch_usernames:
        list_of_usernames = all_names_leaderboards(game=game, mode=mode)
        with open(filename, "w", encoding='utf-8') as f:
            f.writelines(list_of_usernames)
    else:
        with open(filename, "r") as f:
            list_of_usernames = f.readlines()

    # convert usernames back into unicode

    with io.open(filename, 'rb') as f:
        stringofusernames = f.read()
    stringofusernames = stringofusernames.decode("unicode_escape")
    list_of_usernames = stringofusernames.split('\n')
    c = 0
    # you need this to prevent the \r at the end of each name
    while len(list_of_usernames) > c:
        if list_of_usernames[c] == '\r':
            list_of_usernames[c] = listofusernames[c][:-1]
        c += 1


    return list_of_usernames

# Uses jstris api to grab all usernames on public leaderboards of a specific gamemode
def all_names_leaderboards(game, mode):
    num_usernames = 500
    nextfirstposition = 0
    list_of_usernames = []

    while num_usernames == 500:

        curr_usernames = leaderboards_to_usernames(game=game, mode=mode, offset=str(nextfirstposition), writeorappend="w")
        num_usernames = len(curr_usernames)
        list_of_usernames.extend(curr_usernames)
        nextfirstposition += 500
        print(f"Usernames Scraped: {nextfirstposition}")

    return list_of_usernames

def leaderboards_to_usernames(game, mode, offset = "0", writeorappend = 'w'):
    # game:
    # 1 = sprint, 3 = cheese, 4 = survival, 5 = ultra

    # mode: (for sprint/cheese)
    # 1 = 40L/10L, 2 = 20L/18L, 3 = 100L, 4 = 1000L
    # any other gamemode should be 1

    # offset:
    # offset of users

    url = "https://jstris.jezevec10.com/api/leaderboard/" + game + "?mode=" + mode + "&offset=" + offset

    response = requests.get(url)
    data = response.json()
    names_list = []
    for i in data:
        names_list.append(i['name'] + "\n")

    return names_list