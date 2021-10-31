from stats_interpreter import my_stats
from stats_interpreter import jstris_stats
import requests
import time
import os


# stats_gather takes that list of usernames and for each username
# finds desired replay from each user with the replay's corresponding stats and link
# all of these things are stored in "unorderedstats.txt"

def indiv_player_stats_gather(listofusernames, game, mode):
    # gathers unordered stats of everyone; saves it for later in unorderedstats.txt

    # checks how much of the stats have been gathered so far; this program is meant to be stopped and run again in
    # accordance to the user's schedule; all stats scraped so far has been saved

    if os.path.exists("unorderedstats.txt") == False:
        f = open("unorderedstats.txt", 'x')
        f.close()

    with open("unorderedstats.txt", "r") as filename:
        listofstats = filename.readlines()
        currentindex = len(listofstats)

    while len(listofusernames) - currentindex > 0:
        print(currentindex + 1, listofusernames[currentindex])

        # format for each player:
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

        if game == "1":
            currentstats = username_best_replay.username_pc_sprint(listofusernames[currentindex], game, mode)
        elif game == "3":
            currentstats = username_best_replay.username_least_blocks(listofusernames[currentindex], game, mode)
        elif game == "5":
            currentstats = username_best_replay.username_ultra_ppb(listofusernames[currentindex], game)
            
        write_finalstats_to_file(listofusernames[currentindex], currentstats, game)

        currentindex += 1
        time.sleep(3)

# sorts for all games in general (supports least blocks so far)
def all_games_stats_gather(listofusernames, game, mode):

    if os.path.exists("unorderedstats.txt") == False:
        f = open("unorderedstats.txt", 'x')
        f.close()

    with open("unorderedstats.txt", "r") as filename:
        for line in filename:
            pass
        lastusername = my_stats.unordered_username(line)

        c = 1
        for i in listofusernames:
            if lastusername == i:
                currentindex = c
            c += 1


    while len(listofusernames) - currentindex > 0:
        print(currentindex + 1, listofusernames[currentindex])

        currentstats = page_replay_stats.username_all_replay_stats(listofusernames[currentindex], game, mode)
        for i in currentstats:
            write_finalstats_to_file(listofusernames[currentindex], i, game)

        currentindex += 1
        time.sleep(3)

    file_stuff.duplicate_deleter()

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
                return jstris_stats.jstris_time(listofstuff[lasttimeindex])
            elif game == "5":
                return jstris_stats.jstris_score(listofstuff[lasttimeindex])

# Check if there are 200 replays in the page
def check_200_replays():
    first_replay = 0
    last_replay = 0
    with open("userleaderboard.txt", "r", encoding= 'utf8') as filename:

        listofstuff = filename.readlines()
        checking_first_replay = True


        c = 0
        # Getting the first number of the replay (like 1st place) and last number
        while len(listofstuff) - c > 0:
            d = 0
            if "<td><strong>" in listofstuff[c]:
                if checking_first_replay == True:
                    while 1 == 1:
                        try:
                            int(listofstuff[c-d])
                        except:
                            pass
                        else:
                            first_replay = int(listofstuff[c-d])
                            break
                        d += 1
                    checking_first_replay = False
                else:
                    while 1 == 1:
                        try:
                            int(listofstuff[c-d])
                        except:
                            pass
                        else:
                            last_replay = int(listofstuff[c-d])
                            break
                        d += 1
            c += 1

        if last_replay - first_replay == 199:
            return True

        return False



# Grabs each user's leaderboard page from internet and store in userleaderboard.txt

class file_stuff:
    def username_leaderboard_file(url):
        # userleaderboard.txt is how all of the page's data will be stored
        r = requests.get(url)
        with open("userleaderboard.txt", "w", encoding="utf-8") as filename:
            filename.write(r.text)
            print('request sent')
        file_stuff.file_treater()

    def file_treater(self):

        # takes file and rewrites it to be more friendly to data handling

        with open('userleaderboard.txt', 'r', encoding='utf-8') as filename:
            listofstuff = filename.readlines()
            c = 0
            total_indices = len(listofstuff)
            while total_indices - c > 0:
                if listofstuff[c] == '\n':
                    listofstuff.pop(c)
                    total_indices -= 1
                    c -= 1
                if listofstuff[c][0] == ' ':
                    listofstuff[c] = listofstuff[c][1:]
                c += 1

        with open('userleaderboard.txt', 'w', encoding='utf-8') as filename:
            filename.writelines(listofstuff)

    def duplicate_deleter(self):

        if os.path.exists("newstats.txt") == False:
            f = open("newstats.txt", 'x')
            f.close()
        elif os.path.exists("newstats.txt") == True:
            os.remove("newstats.txt")
            f = open("newstats.txt", 'x')
            f.close()

        previous_replay = ''
        non_duplicate_list = []
        with open('unorderedstats.txt', 'r', encoding='utf-8') as filename:
            c = 0
            while len(filename) - c > 0:
                current_replay = filename.readline()
                if current_replay != previous_replay:
                    non_duplicate_list.append(current_replay)
                if len(non_duplicate_list) == 10000:
                    with open("newstats.txt", 'a', encoding='utf-8') as filename:
                        filename.writelines(non_duplicate_list)
                        non_duplicate_list = []
                previous_replay = current_replay
                c += 1

        os.rename('newstats.txt', 'unorderedstats.txt')
        os.remove('newstats.txt')


class page_replay_stats:
    # Gets every replay of a user for a specific game and mode
    def username_all_replay_stats(username, game, mode):
        current_last_replay = "0"
        allpagesstats = []

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

        while 1 == 1:

            #gets next page
            url = "https://jstris.jezevec10.com/" + gamemode + "?display=5&user=" + username + "&lines=" + lines + "&page=" + current_last_replay
            file_stuff.username_leaderboard_file(url)
            time.sleep(3)

            # adds current page replays to list of all other replays so far
            allpagesstats.extend(page_replay_stats.page_200_replays_stats())

            # checks if there are no pages left
            if check_200_replays() == False:
                break

            # sets up next url
            current_last_replay = str(last_time_in_page(game))


        return allpagesstats


    # Convert 200 replay data in userleaderboard.txt into list of tuple of stats
    def page_200_replays_stats(parameter):

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
                    currenttime = jstris_stats.jstris_time(currenttime)

                    currentblock = listofstuff[c + 1]
                    currentblock = jstris_stats.blocks(currentblock)

                    currentpps = listofstuff[c + 2]
                    currentpps = jstris_stats.pps(currentpps)

                    currentfinesse = listofstuff[c + 3]
                    currentfinesse = jstris_stats.finesse(currentfinesse)

                    currentdate = listofstuff[c + 4]
                    currentdate = jstris_stats.date(currentdate)

                    currentlink = listofstuff[c + 6]
                    currentlink = jstris_stats.link(currentlink)

                    allstats.append(
                        (currenttime, currentblock, currentpps, currentfinesse, currentdate, currentlink))
                c += 1

        return allstats

    def ultra_page_200_replays_stats(parameter):

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
                    currentscore = jstris_stats.jstris_score(currentscore)

                    currentblock = listofstuff[c + 1]
                    currentblock = jstris_stats.blocks(currentblock)

                    currentppb = listofstuff[c + 2]
                    currentppb = jstris_stats.ppb(currentppb)

                    currentpps = listofstuff[c + 3]
                    currentpps = jstris_stats.pps(currentpps)

                    currentfinesse = listofstuff[c + 4]
                    currentfinesse = jstris_stats.finesse(currentfinesse)

                    currentdate = listofstuff[c + 5]
                    currentdate = jstris_stats.date(currentdate)

                    currentlink = listofstuff[c + 7]
                    currentlink = jstris_stats.link(currentlink)

                    allstats.append(
                        (currentscore, currentblock, currentppb , currentpps, currentfinesse, currentdate, currentlink))
                c += 1

        return allstats

# Eventually separate into different class in order to do other things besides grab each user's least blocks
# Sprint PC runs?

class username_best_replay:
    def username_least_blocks(username, game, mode):
        current_last_replay = "0"
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

        while 1 == 1:

            # gets next cheese page
            url = "https://jstris.jezevec10.com/" + gamemode + "?display=5&user=" + username + "&lines=" + lines + "&page=" + current_last_replay
            file_stuff.username_leaderboard_file(url)

            # Searches if there is a new least blocks
            currentpageblocks = page_replay_stats.page_200_replays_stats()
            c = 0
            for i in currentpageblocks:
                if minblocks > i[1]:
                    minblocks = i[1]
                    minstats = i
                c += 1

            # checks if there are no pages left
            if check_200_replays() == False:
                break

            # Sets up next url
            current_last_replay = str(last_time_in_page(game))

        return minstats

    def username_pc_sprint(username, game, mode):
        current_last_replay = "0"
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

            # gets next page
            url = "https://jstris.jezevec10.com/" + gamemode + "?display=5&user=" + username + "&lines=" + lines + "&page=" + current_last_replay
            file_stuff.username_leaderboard_file(url)
            time.sleep(3)

            # scrapes stats from current page
            # difference between this and username_least_blocks is that this breaks right away when a pc finish is found
            currentpageblocks = page_replay_stats.page_200_replays_stats()
            for i in currentpageblocks:
                if int(int(lines[:-1]) * 2.5) == i[1]:
                    pcsprint = i
                    print("True:", pcsprint)
                    return pcsprint

            # checks if there are no pages left
            if check_200_replays() == False:
                break

            # Sets up next url
            current_last_replay = str(last_time_in_page(game))

        print(pcsprint)
        return pcsprint

    def username_ultra_ppb(username, game):
        current_last_replay = "100000000000"
        maxstats = False
        maxppb = 0

        # converts game and mode to their respective strings to search in url

        if game == "5":
            gamemode = "ultra"

        while 1 == 1:

            # gets current page
            url = "https://jstris.jezevec10.com/" + gamemode + "?display=5&user=" + username + "&page=" + current_last_replay
            file_stuff.username_leaderboard_file(url)
            time.sleep(3)

            # scrapes stats from current page
            # difference between this and username_least_blocks is that this breaks right away when a pc finish is found
            currentpageppb = page_replay_stats.ultra_page_200_replays_stats()
            for i in currentpageppb:
                if i[2] > maxppb:
                    print(i)
                    maxppb = i[2]
                    maxstats = i

            # checks if there are no pages left
            if check_200_replays() == False:
                break

            # Sets up next url
            current_last_replay = str(last_time_in_page(game))

        return maxstats

# Write user's final pb or replay and corresponding stats to unorderedstats.txt
def write_finalstats_to_file(username, currentstats, game):
    if game != "5":
        with open("unorderedstats.txt", "a", encoding="UTF-8") as filename:
            if type(currentstats) != bool:
                filename.write(username + "  ")
                filename.write("Time: " + jstris_stats.seconds_to_clock(currentstats[0]) + "  ")
                filename.write("Blocks: " + str(currentstats[1]) + "  ")
                filename.write("PPS: " + str(currentstats[2]) + "  ")
                filename.write("Finesse: " + str(currentstats[3]) + "  ")
                filename.write("Date: " + currentstats[4] + "  ")
                filename.write("Link: " + currentstats[5] + " \n")
            elif type(currentstats) == bool:
                filename.write("No valid run;\n")
            else:
                raise "error"

    elif game == "5":
        with open("unorderedstats.txt", "a", encoding="UTF-8") as filename:
            if type(currentstats) != bool:
                filename.write(username + "  ")
                filename.write("Time: " + jstris_stats.clock_to_seconds(str(currentstats[0]) + "  "))
                filename.write("Blocks: " + str(currentstats[1]) + "  ")
                filename.write("PPS: " + str(currentstats[2]) + "  ")
                filename.write("Finesse: " + str(currentstats[3]) + "  ")
                filename.write("Date: " + currentstats[4] + "  ")
                filename.write("Link: " + currentstats[5] + " \n")
            elif type(currentstats) == bool:
                filename.write("No valid run;\n")
            else:
                raise "error"

