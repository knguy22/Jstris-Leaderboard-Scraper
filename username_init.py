import io
import requests

# username_init checks if we want to scrape the jstris api leaderboards and outputs a list of usernames
# the usernames are stored in "unorderedname.txt"

def username_init(game, mode):
    # Checking if the username file is empty

    conditiongetusernames = False
    with open("unorderedname.txt", "r") as filename:
        listofusernames = filename.readlines()
        if len(listofusernames) < 1:
            conditiongetusernames = True

    # gather usernames from jstris api if unorderedname.txt is empty
    # if already have usernames, gather usernames from unorderedname.txt

    if conditiongetusernames == True:
        listofusernames = all_names_leaderboards(game=game, mode=mode)
        with open("unorderedname.txt", "w") as filename:
            filename.writelines(listofusernames)
    else:
        with open("unorderedname.txt", "r") as filename:
            listofusernames = filename.readlines()

    # convert usernames back into unicode

    with io.open("unorderedname.txt", 'rb') as f:
        stringofusernames = f.read()
    stringofusernames = stringofusernames.decode("unicode_escape")
    listofusernames = []
    while ("\n" in stringofusernames) == True:
        nindex = stringofusernames.index("\n")
        listofusernames.append(stringofusernames[: nindex - 1])
        stringofusernames = stringofusernames[nindex + 1:]

    return listofusernames

# Uses jstris api to grab all usernames on public leaderboards of a specific gamemode
def all_names_leaderboards(game, mode):
    currentfirstposition = -500
    nextfirstposition = 0
    listofusernames = []

    while nextfirstposition == currentfirstposition + 500:

        leaderboards_file(game=game, mode=mode, offset=str(nextfirstposition), writeorappend="w")
        currentfirstposition = nextfirstposition

        with open("leaderboard.txt", "r") as filename:
            c = 0

            # jstris api only returns a single line containing all 500 usernames
            listofstuff = filename.readline()

            # checks last username position; if last username's index is less than 500, there are no more usernames
            # left after this page; the while statement will check

            # example format from jstris api
            # [{"id":36350620,"pos":1,"game":61.454,"ts":"2021-06-15 15:55:03","name":"qwerty"},

            lastpos = listofstuff.rindex('"pos"')
            lastgame = listofstuff.rindex('"game"')
            nextfirstposition = int(listofstuff[lastpos + 6: lastgame - 1])
            print(nextfirstposition)

            # scrapes the usernames

            while len(listofstuff) > 1:
                endbracket = listofstuff.index('}')
                begusername = listofstuff.index('name')
                listofusernames.append(listofstuff[begusername + 7: endbracket - 1] + '\n')
                listofstuff = listofstuff[endbracket + 2:]

    return listofusernames

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
