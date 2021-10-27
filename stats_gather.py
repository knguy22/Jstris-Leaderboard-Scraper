import stats_interpreter
import requests
import time
import os


# stats_gather takes that list of usernames and for each username
# finds desired replay from each user with the replay's corresponding stats and link
# all of these things are stored in "unorderedstats.txt"

def stats_gather(listofusernames, game, mode):
    # gathers unordered stats of everyone; saves it for later in unorderedstats.txt

    # checks how much of the stats have been gathered so far; this program is meant to be stopped and run again in
    # accordance to the user's schedule; all stats scraped so far has been saved

    if os.path.exists("unorderedstats.txt") == False:
        f = open("unorderedstats.txt", 'x')
        f.close()

    with open("unorderedstats.txt", "rb") as filename:
        listofstats = filename.readlines()
        currentindex = len(listofstats)

    while len(listofusernames) - currentindex > 0:
        print(currentindex + 1, listofusernames[currentindex])

        # format for each player:
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

        if game == "1":
            currentstats = username_pc_sprint(listofusernames[currentindex], game, mode)
        elif game == "3":
            currentstats = username_least_blocks(listofusernames[currentindex], game, mode)
        elif game == "5":
            currentstats = username_ultra_ppb(listofusernames[currentindex], game, mode)
            
        write_finalstats_to_file(listofusernames[currentindex], currentstats, game)

        currentindex += 1
        time.sleep(3)

# Get time value of last replay in page
def last_time_in_page(game):

    # returns integers
    with open("userleaderboard.txt", "r", encoding="utf8") as filename:

        # set up stuff, get the file from user_leaderboard_file

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
            if game != "5":
                return stats_interpreter.jstris_time(listofstuff[lasttimeindex])
            elif game == "5":
                return stats_interpreter.jstris_score(listofstuff[lasttimeindex])

# Grabs each user's leaderboard page from internet and store in userleaderboard.txt
def username_leaderboard_file(url):
    # userleaderboard.txt is how all of the page's data will be stored
    r = requests.get(url)
    filename = open("userleaderboard.txt", "w", encoding="utf-8")
    filename.write(r.text)
    filename.close()

# Convert 200 replay data in userleaderboard.txt into list of tuple of stats
def page_200_replays_stats():

    # returns integers where there can be integers (Ex: blocks) and returns strings for others( Ex: date)

    with open("userleaderboard.txt", "r", encoding='utf-8') as filename:

        listofstuff = filename.readlines()
        allstats = []

        # use the formatting of the time thing to find the line of the blocks, which is right after time taken;


        # uses <td><strong>, which is formatting for time, to find where all the other stats are in reference to each
        # timestamp on page

        # Example format on page (last - is a replay that has been deleted
        # streasure</a>
        # </td>
        # <td><strong>288:57.<span class="time-mil">800</span></strong></td>
        # <td>1167</td>
        # <td>0.07</td>
        # <td>1542</td>
        # <td>2021-01-07 01:23:52</td>
        # <td>
        # -

        c = 0
        while len(listofstuff) - c > 0:

            if "<td><strong>" in listofstuff[c]:
                currenttime = listofstuff[c]
                currenttime = stats_interpreter.jstris_time(currenttime)

                currentblock = listofstuff[c + 1]
                currentblock = stats_interpreter.blocks(currentblock)

                currentpps = listofstuff[c + 2]
                currentpps = stats_interpreter.pps(currentpps)

                currentfinesse = listofstuff[c + 3]
                currentfinesse = stats_interpreter.finesse(currentfinesse)

                currentdate = listofstuff[c + 4]
                currentdate = stats_interpreter.date(currentdate)

                currentlink = listofstuff[c + 6]
                currentlink = stats_interpreter.link(currentlink)

                allstats.append(
                    (currenttime, currentblock, currentpps, currentfinesse, currentdate, currentlink))
            c += 1

    return allstats

def ultra_page_200_replays_stats():

    # returns integers where there can be integers (Ex: blocks) and returns strings for others( Ex: date)

    with open("userleaderboard.txt", "r", encoding='utf-8') as filename:

        listofstuff = filename.readlines()
        allstats = []

        # uses <td><strong>, which is formatting for beginning of line, to find where all the other stats are in reference to each
        # score on page

        # Example format on page (last - is a replay that has been deleted
        # fortissim2</a>
        # </td>
        # <td><strong>180,855</strong></td>
        # <td>477</td>
        # <td>379.15</td>
        # <td>3.98</td>
        # <td>46</td>
        # <td>2021-09-08 20:05:17</td>
        # <td>
        # <a href="https://jstris.jezevec10.com/replay/40744031" target="_blank">(V3)<img src="https://jstris.jezevec10.com/res/play.png"></a>

        c = 0
        while len(listofstuff) - c > 0:

            if "<td><strong>" in listofstuff[c]:
                currentscore = listofstuff[c]
                currentscore = stats_interpreter.jstris_score(currentscore)

                currentblock = listofstuff[c + 1]
                currentblock = stats_interpreter.blocks(currentblock)

                currentppb = listofstuff[c + 2]
                currentppb = stats_interpreter.ppb(currentppb)

                currentpps = listofstuff[c + 3]
                currentpps = stats_interpreter.pps(currentpps)

                currentfinesse = listofstuff[c + 4]
                currentfinesse = stats_interpreter.finesse(currentfinesse)

                currentdate = listofstuff[c + 5]
                currentdate = stats_interpreter.date(currentdate)

                currentlink = listofstuff[c + 7]
                currentlink = stats_interpreter.link(currentlink)

                allstats.append(
                    (currentscore, currentblock, currentppb , currentpps, currentfinesse, currentdate, currentlink))
            c += 1

    return allstats


# Write user's final pb or replay and corresponding stats to unorderedstats.txt
def write_finalstats_to_file(username, currentstats, game):
    if game != "5":
        with open("unorderedstats.txt", "a", encoding="UTF-8") as filename:
            if type(currentstats) != bool:
                filename.write(username + "  ")
                filename.write("Time: " + stats_interpreter.time_reverse(currentstats[0]) + "  ")
                filename.write("Blocks: " + str(currentstats[1]) + "  ")
                filename.write("PPS: " + str(currentstats[2]) + "  ")
                filename.write("Finesse: " + str(currentstats[3]) + "  ")
                filename.write("Date: " + currentstats[4] + "  ")
                filename.write("Link: " + currentstats[5] + " \n")
            elif type(currentstats) == bool:
                filename.write("No valid run;\n")
            else:
                raise "error"
                raise currentstats

    elif game == "5":
        with open("unorderedstats.txt", "a", encoding="UTF-8") as filename:
            if type(currentstats) != bool:
                filename.write(username + "  ")
                filename.write("Time: " + stats_interpreter.time_reverse(currentstats[0]) + "  ")
                filename.write("Blocks: " + str(currentstats[1]) + "  ")
                filename.write("PPS: " + str(currentstats[2]) + "  ")
                filename.write("Finesse: " + str(currentstats[3]) + "  ")
                filename.write("Date: " + currentstats[4] + "  ")
                filename.write("Link: " + currentstats[5] + " \n")
            elif type(currentstats) == bool:
                filename.write("No valid run;\n")
            else:
                raise "error"
                raise currentstats



# Eventually separate into different class in order to do other things besides grab each user's least blocks
# Sprint PC runs?

def username_least_blocks(username, game, mode):
    current_last_replay = "0"
    previous_last_replay = 0
    minblocks = 10 ** 20

    # converts game and mode to their respective strings to search in url
    if game == "1":
        gamemode = "sprint"
        if mode == "2":
            lines = "20L"
        elif mode == "1":
            lines = "40L"
        elif mode == "3":
            lines = "100L"
        elif mode == "4":
            lines = "1000L"
        else:
            "invalid mode"
            return -69
    elif game == "3":
        gamemode = "cheese"
        if mode == "1":
            lines = "10L"
        elif mode == "2":
            lines = "18L"
        elif mode == "3":
            lines = "100L"
        else:
            raise "invalid mode"
            return -69

    while 1 == 1:

        #gets next cheese page
        url = "https://jstris.jezevec10.com/" + gamemode + "?display=5&user=" + username + "&lines=" + lines + "&page=" + current_last_replay
        username_leaderboard_file(url)

        # checks if there are no replays left by checking if the last replay is identical to the last page's last replay
        previous_last_replay = current_last_replay
        current_last_replay = str(last_time_in_page(game))
        if current_last_replay == previous_last_replay or float(current_last_replay) < float(previous_last_replay):
            break

        # scrapes stats from current page
        # this works for perfect clear sprints too because slower perfect clear finish won't override the faster one
        # which appears in the leaderboard first
        currentpageblocks = page_200_replays_stats()
        c = 0
        replayindex = 0
        for i in currentpageblocks:
            if minblocks > i[1]:
                minblocks = i[1]
                minstats = i
            c += 1

    return minstats

def username_pc_sprint(username, game, mode):
    current_last_replay = "0"
    previous_last_replay = 0
    pcsprint = False

    # converts game and mode to their respective strings to search in url
    if game == "1":
        gamemode = "sprint"
        if mode == "2":
            lines = "20L"
        elif mode == "1":
            lines = "40L"
        elif mode == "3":
            lines = "100L"
        elif mode == "4":
            lines = "1000L"
        else:
            "invalid mode"
            return -69

    while 1 == 1:

        #gets next page
        url = "https://jstris.jezevec10.com/" + gamemode + "?display=5&user=" + username + "&lines=" + lines + "&page=" + current_last_replay
        username_leaderboard_file(url)
        time.sleep(1)

        # checks if there are no replays left by checking if the last replay is identical to the last page's last replay
        previous_last_replay = current_last_replay
        current_last_replay = str(last_time_in_page(game))
        if current_last_replay == previous_last_replay or float(current_last_replay) < float(previous_last_replay):
            break

        # scrapes stats from current page
        # difference between this and username_least_blocks is that this breaks right away when a pc finish is found
        currentpageblocks = page_200_replays_stats()
        print(time.asctime())
        c = 0
        replayindex = 0
        for i in currentpageblocks:
            if int(int(lines[:-1]) * 2.5) ==  i[1]:
                pcsprint = i
                print("True:", pcsprint)
                return pcsprint
            c += 1
    
    print(pcsprint)
    return pcsprint

def username_ultra_ppb(username, game):
    current_last_replay = "100000000000"
    previous_last_replay = 0
    maxstats = False
    maxppb = 0

    # converts game and mode to their respective strings to search in url

    if game == "5":
        gamemode = "ultra"

    while 1 == 1:

        # gets next page
        url = "https://jstris.jezevec10.com/" + gamemode + "?display=5&user=" + username + "&page=" + current_last_replay
        username_leaderboard_file(url)
        time.sleep(1)

        # checks if there are no replays left by checking if the last replay is identical to the last page's last replay
        previous_last_replay = current_last_replay
        current_last_replay = str(last_time_in_page(game))

        if current_last_replay == previous_last_replay:
            break

        # scrapes stats from current page
        # difference between this and username_least_blocks is that this breaks right away when a pc finish is found
        currentpageppb = ultra_page_200_replays_stats()

        for i in currentpageppb:
            if i[2] > maxppb:
                maxppb = i[2]
                maxstats = i

        print(time.asctime())


    return maxstats