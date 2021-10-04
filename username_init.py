import io
import file_grab

# username_init checks if we want to scrape the jstris api leaderboards and outputs a list of usernames
# the usernames are stored in "unorderedname.txt"
def all_names_leaderboards(game, mode):
    currentfirstposition = -500
    nextfirstposition = 0
    listofusernames = []

    while nextfirstposition == currentfirstposition + 500:

        file_grab.leaderboards_file(game=game, mode=mode, offset=str(nextfirstposition), writeorappend="w")
        currentfirstposition = nextfirstposition

        with open("leaderboard.txt", "r") as filename:
            c = 0
            listofstuff = filename.readlines()
            listofstuff = listofstuff[0]

            # example format from jstris api
            # [{"id":36350620,"pos":1,"game":61.454,"ts":"2021-06-15 15:55:03","name":"qwerty"},

            # checks last username position

            lastpos = listofstuff.rindex('"pos"')
            lastgame = listofstuff.rindex('"game"')
            nextfirstposition = int(listofstuff[lastpos + 6: lastgame - 1])
            print(nextfirstposition)

            # gets the usernames

            while len(listofstuff) > 1:
                endbracket = listofstuff.index('}')
                begusername = listofstuff.index('name')
                listofusernames.append(listofstuff[begusername + 7: endbracket - 1] + '\n')
                listofstuff = listofstuff[endbracket + 2:]
            a = 0
    return listofusernames

def username_init():
    # Getting usernames needed

    conditiongetusernames = False

    # Checking if the username file is empty

    with open("unorderedname.txt", "r") as filename:
        listofusernames = filename.readlines()
        if len(listofusernames) < 1:
            conditiongetusernames = True

    # gather usernames if file is empty; if already have username, gather usernames from file

    if conditiongetusernames == True:
        listofusernames = all_names_leaderboards(game="3", mode="3")
        with open("unorderedname.txt", "w") as filename:
            filename.writelines(listofusernames)
    else:
        with open("unorderedname.txt", "r") as filename:
            listofusernames = filename.readlines()

    # Converts Back into Unicode

    with io.open("unorderedname.txt", 'rb') as f:
        stringofusernames = f.read()
    stringofusernames = stringofusernames.decode("unicode_escape")
    listofusernames = []
    while ("\n" in stringofusernames) == True:
        nindex = stringofusernames.index("\n")
        listofusernames.append(stringofusernames[: nindex - 1])
        stringofusernames = stringofusernames[nindex + 1:]

    return listofusernames