import io
import requests
import os

# username_init checks if we want to scrape the jstris api leaderboards and outputs a list of usernames
# the usernames are stored in "unorderedname.txt"

def username_init(game, mode, filename):
    # Checking if the username file is empty

    conditiongetusernames = False

    if os.path.exists(filename) == False:
        f = open(filename, 'x')
        f.close()

    with open(filename, "r", encoding='utf-8') as f:
        listofusernames = f.readlines()
        if len(listofusernames) < 1:
            conditiongetusernames = True

    # gather usernames from jstris api if unorderedname.txt is empty
    # if already have usernames, gather usernames from unorderedname.txt
    if conditiongetusernames == True:
        listofusernames = all_names_leaderboards(game=game, mode=mode)
        with open(filename, "w", encoding='utf-8') as f:
            f.writelines(listofusernames)
    else:
        with open(filename, "r") as f:
            listofusernames = f.readlines()

    # convert usernames back into unicode

    with io.open(filename, 'rb') as f:
        stringofusernames = f.read()
    stringofusernames = stringofusernames.decode("unicode_escape")
    listofusernames = stringofusernames.split('\n')
    c = 0
    # you need this to prevent the \r at the end of each name
    while len(listofusernames) > c:
        listofusernames[c] = listofusernames[c][:-1]
        c += 1


    return listofusernames

# Uses jstris api to grab all usernames on public leaderboards of a specific gamemode
def all_names_leaderboards(game, mode):
    num_usernames = 500
    nextfirstposition = 0
    listofusernames = []

    while num_usernames == 500:

        curr_usernames = leaderboards_to_usernames(game=game, mode=mode, offset=str(nextfirstposition), writeorappend="w")
        num_usernames = len(curr_usernames)
        listofusernames.extend(curr_usernames)
        nextfirstposition += 500

    return listofusernames

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