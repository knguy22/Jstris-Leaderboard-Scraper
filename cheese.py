import requests
import io


# Grabs all files from internet
class filegrab:
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



# Interprets json to txt formatting to get the stats we want
class cheese_stats_interpreter:

    #Everything below will return an integer/float except for the date, link and timestring, which return a string

    #clock format to seconds
    def time(timestring):
        # example time thing in the file
        # <td><strong>1:47.<span class="time-mil">171</span></strong></td>
        # example without any milliseconds
        # <td><strong>3:27</strong></td>

        timestringbeginning = timestring.index("<td><strong>")
        timestringcolon = timestring.index(":")

        minutes = timestring[timestringbeginning + 12: timestringcolon]

        if len(timestring) > 35:
            timestringperiod = timestring.index('.')
            timestringms = timestring.index("time-mil")
            seconds = timestring[timestringcolon + 1: timestringperiod]
            milliseconds = timestring[timestringms + 10: timestringms + 13]
        else:
            # accounts for case without ms
            seconds = timestring[timestringcolon + 1: -15]
            milliseconds = 0

        return (60 * int(minutes) + int(seconds) + 0.001 * int(milliseconds))
    #seconds to clock format
    def time_reverse(timefloat):
        minutes = int(timefloat // 60)
        seconds = int(timefloat - 60 * minutes // 1)
        milliseconds = round(timefloat - (60 * minutes) - seconds,3)

        minutes = str(minutes)
        #deals with seconds when it's below 10 like 1:06
        if seconds < 10:
            seconds = "0" + str(seconds)
        else:
            seconds = str(seconds)
        milliseconds = str(milliseconds)



        timestring = minutes + ":" + seconds + "." + milliseconds[2:]
        return timestring

    def blocks(blocksstring):
        #example line
        #<td>236</td>
        if blocksstring[0] == " ":
            blocksstring = blocksstring[1:]
        blockstringend = blocksstring.rindex("</td>")
        blocksstring = int(blocksstring[4:blockstringend])
        return blocksstring

    def pps(ppsstring):
        #example line
        #<td>0.08</td>
        if ppsstring[0] == " ":
            ppsstring = ppsstring[1:]
        ppsstringend = ppsstring.rindex("</td>")
        ppsstring = float(ppsstring[4:ppsstringend])
        ppsstring = round(ppsstring,2)
        return ppsstring

    def finesse(finessestring):
        # example line
        # <td>48</td>
        if finessestring[0] == " ":
            finessestring = finessestring[1:]
        finessestringend = finessestring.rindex("</td>")
        finessestring = int(finessestring[4:finessestringend])
        return finessestring

    def date(datestring):
        #example
        #<td>2020-08-11 18:06:53</td>
        if datestring[0] == " ":
            datestring = datestring[1:]
        datestringend = datestring.rindex("</td>")
        datestring = datestring[4:datestringend]
        return datestring

    def link(linkstring):
        #example
        #<a href="https://jstris.jezevec10.com/replay/19483494" target="_blank">(V3)<img src="https://jstris.jezevec10.com/res/play.png"></a>
        if "https://jstris.jezevec10.com/replay/" in linkstring:
            linkstringend = linkstring.index("target") - 2
            linkstring = linkstring[9:linkstringend]
        else:
            linkstring = "-"
        return linkstring



# The following 3 classes are the bulk of the program;

# username_init checks if we want to scrape the jstris api leaderboards and outputs a list of usernames
# the usernames are stored in "unorderedname.txt"
class username_init:
    def all_names_leaderboards(game, mode):
        currentfirstposition = -500
        nextfirstposition = 0
        listofusernames = []

        while nextfirstposition == currentfirstposition + 500:

            filegrab.leaderboards_file(game=game, mode=mode, offset=str(nextfirstposition), writeorappend="w")
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
            listofusernames = username_init.all_names_leaderboards(game="3", mode="3")
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

# stats_gather takes that list of usernames and for each username
# finds the lowest block run with the replay's corresponding stats and link
# all of these things are stored in "unorderedstats.txt"
class stats_gather:
    def last_time_in_page():

        # returns integers

        with open("cheese.txt", "r", encoding="utf8") as filename:

            # set up stuff, get the file from cheese_file

            listofstuff = filename.readlines()
            c = 0
            lasttimeindex = 0

            # only the time uses this format

            while len(listofstuff) - c > 0:
                if "<td><strong>" in listofstuff[c]:
                    lasttimeindex = c
                c += 1

            if lasttimeindex == 0:
                return 0
            else:
                return cheese_stats_interpreter.time(listofstuff[lasttimeindex])

    def page_200_replays_stats():

        # returns integers

        with open("cheese.txt", "r", encoding='utf-8') as filename:

            # set up stuff, get the file from top200cheesemaker

            listofstuff = filename.readlines()
            allcheesestats = []
            # currentblock = 0
            # currentlink = ''
            c = 0

            # use the formatting of the time thing to find the line of the blocks, which is right after time taken;

            while len(listofstuff) - c > 0:
                if "<td><strong>" in listofstuff[c]:
                    currenttime = listofstuff[c]
                    currenttime = cheese_stats_interpreter.time(currenttime)

                    currentblock = listofstuff[c + 1]
                    currentblock = cheese_stats_interpreter.blocks(currentblock)

                    currentpps = listofstuff[c + 2]
                    currentpps = cheese_stats_interpreter.pps(currentpps)

                    currentfinesse = listofstuff[c + 3]
                    currentfinesse = cheese_stats_interpreter.finesse(currentfinesse)

                    currentdate = listofstuff[c + 4]
                    currentdate = cheese_stats_interpreter.date(currentdate)

                    currentlink = listofstuff[c + 6]
                    currentlink = cheese_stats_interpreter.link(currentlink)

                    allcheesestats.append(
                        (currenttime, currentblock, currentpps, currentfinesse, currentdate, currentlink))
                c += 1

        return allcheesestats

    def username_least_blocks(username):
        firstreplay = "0"
        lastreplay = 0
        minblocks = 10000

        while 1 == 1:

            #gets next cheese page
            url = "https://jstris.jezevec10.com/cheese?display=5&user=" + username + "&lines=100L&page=" + firstreplay
            filegrab.cheese_file(url)

            # checks if there are no replays left by checking if the last replay is identical to the last page's last replay
            lastreplay = firstreplay
            firstreplay = str(stats_gather.last_time_in_page())
            if firstreplay == lastreplay or float(firstreplay) < float(lastreplay):
                break

            # scrapes stats from current page
            currentpageblocks = stats_gather.page_200_replays_stats()
            c = 0
            replayindex = 0
            for i in currentpageblocks:
                if minblocks > i[1]:
                    minblocks = i[1]
                    minstats = i
                c += 1

        return minstats

    def stats_gather(listofusernames):
        # gathers unordered stats of everyone; saves it for later

        with open("unorderedstats.txt", "rb") as filename:
            listofstats = filename.readlines()
        with open("unorderedstats.txt", "a", encoding="UTF-8") as filename:
            currentindex = len(listofstats)
            while len(listofusernames) - currentindex > 0:
                # format
                # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720
                print(currentindex, listofusernames[currentindex])

                currentstats = stats_gather.username_least_blocks(listofusernames[currentindex])
                filename.write(listofusernames[currentindex] + "  ")
                filename.write("Time: " + cheese_stats_interpreter.time_reverse(currentstats[0]) + "  ")
                filename.write("Blocks: " + str(currentstats[1]) + "  ")
                filename.write("PPS: " + str(currentstats[2]) + "  ")
                filename.write("Finesse: " + str(currentstats[3]) + "  ")
                filename.write("Date: " + currentstats[4] + "  ")
                filename.write("Link: " + currentstats[5] + " \n")
                currentindex += 1

# stats_sorter takes "unorderedstats.txt" and sorts each username for blocks ascending from lowest blocks (ascend
# from lowest time if blocks are equal);
# the ordered usernames are put into "orderedstats.txt"
class stats_sorter:
    def stats_sorter():

        # open the list of unordered least block runs; now have listofusernames

        listofusernames = []
        listofusernames = stats_sorter.open_unordered_stats()


        # extract least block runs, index, and pps in list from each username's string; assigns them to tuple
        # use least blocks and pps to sort later

        listofblockruns = []
        listofblockruns = stats_sorter.stats_string_to_blocks(listofusernames)
        # sorting algorithm

        listofblockruns = stats_sorter.sorting_algorithm(listofblockruns)

        # prepares list of stats from unorderedstatstxt using sorted listofblockruns and writes unorderedstats into
        # orderedstats.txt

        stats_sorter.write_stats_to_file(listofblockruns, listofusernames)

    def open_unordered_stats():
        with io.open("unorderedstats.txt", encoding='utf-8') as f:
            stringofusernames = f.readlines()

        listofusernames = []
        for i in stringofusernames:
            listofusernames.append(i.rstrip())

        return listofusernames

    def stats_string_to_blocks(listofusernames):

        # string format:
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

        c = 0
        listofblockruns = []
        for i in listofusernames:
            blocksindex = i.index("Blocks: ")
            ppsindex = i.index("PPS: ")
            finesseindex = i.index("Finesse: ")
            listofblockruns.append((int(i[blocksindex + 8: ppsindex - 2]), float(i[ppsindex + 5: finesseindex - 2]), c))
            c += 1
        return listofblockruns

    def sorting_algorithm(listofblockruns):
        # switches two indexes in a list if the lower index has a higher block count than the higher index
        # pretty inefficient; will change later
        # e checks if there has been any sorting for each time the entire list is run through
        currentblocks = 0
        nextblocks = 0
        e = 1
        while e != 0:
            # d iterates through the entire list of runs over and over to sort
            d = 0
            e = 0
            while len(listofblockruns) - d - 1 > 0:
                currentblocks = listofblockruns[d][0]
                nextblocks = listofblockruns[d + 1][0]
                if nextblocks < currentblocks:
                    listofblockruns[d + 1], listofblockruns[d] = listofblockruns[d], listofblockruns[d + 1]
                    e += 1
                # Compares time if the blocks are the same; higher pps for same blocks means lower time
                if nextblocks == currentblocks:
                    if listofblockruns[d + 1][1] > listofblockruns[d][1]:
                        listofblockruns[d + 1], listofblockruns[d] = listofblockruns[d], listofblockruns[d + 1]
                        e += 1
                d += 1

        return listofblockruns

    def write_stats_to_file(listofblockruns, listofusernames):
        # final list of strings
        sortedlistofusernames = []
        for i in listofblockruns:
            sortedlistofusernames.append(listofusernames[i[2]])

        # encode for text

        c = 0
        while len(sortedlistofusernames) - c > 0:
            sortedlistofusernames[c] = str(c + 1) + ". " + sortedlistofusernames[c] + "\n"
            sortedlistofusernames[c] = sortedlistofusernames[c].encode("utf8")
            c += 1

        # write text to final document
        with open("orderedstats.txt", "wb") as f:
            f.writelines(sortedlistofusernames)


def main():

    #gathers list of usernames; saves usernames for later if not already there in unorderedname.txt

    listofusernames = username_init.username_init()

    #gets least block runs and respective stats from each player

    stats_gather.stats_gather(listofusernames)

    #gather list of blocks from each stats part

    stats_sorter.stats_sorter()


#To do
#Add gamemode support
#support not having minutes in time
#look into spreadsheets?
#Multithread requests