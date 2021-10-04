import cheese_stats_interpreter
import file_grab

# stats_gather takes that list of usernames and for each username
# finds the lowest block run with the replay's corresponding stats and link
# all of these things are stored in "unorderedstats.txt"
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
        file_grab.cheese_file(url)

        # checks if there are no replays left by checking if the last replay is identical to the last page's last replay
        lastreplay = firstreplay
        firstreplay = str(last_time_in_page())
        if firstreplay == lastreplay or float(firstreplay) < float(lastreplay):
            break

        # scrapes stats from current page
        currentpageblocks = page_200_replays_stats()
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

            currentstats = username_least_blocks(listofusernames[currentindex])
            filename.write(listofusernames[currentindex] + "  ")
            filename.write("Time: " + cheese_stats_interpreter.time_reverse(currentstats[0]) + "  ")
            filename.write("Blocks: " + str(currentstats[1]) + "  ")
            filename.write("PPS: " + str(currentstats[2]) + "  ")
            filename.write("Finesse: " + str(currentstats[3]) + "  ")
            filename.write("Date: " + currentstats[4] + "  ")
            filename.write("Link: " + currentstats[5] + " \n")
            currentindex += 1