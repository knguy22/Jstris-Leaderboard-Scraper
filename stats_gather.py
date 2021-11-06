from stats_interpreter import my_stats
from stats_interpreter import jstris_stats
import requests
import time
import os


# stats_gather takes that list of usernames and for each username
# finds desired replay from each user with the replay's corresponding stats and link
# all of these things are stored in "unorderedstats.txt"


# used for forming leaderboards where each player only has one replay
def indiv_player_stats_gather(listofusernames, game, mode):
    # gathers unordered stats of everyone; saves it for later in unorderedstats.txt

    # checks how much of the stats have been gathered so far; this program is meant to be stopped and run again in
    # accordance to the user's schedule; all stats scraped so far has been saved

    if os.path.exists("unorderedstats.txt") is False:
        f = open("unorderedstats.txt", 'x')
        f.close()

    with open("unorderedstats.txt", "r", encoding='utf-8') as filename:
        listofstats = filename.readlines()
        currentindex = len(listofstats)

    my_session = requests.session()

    while len(listofusernames) - currentindex > 0:
        print(currentindex + 1, listofusernames[currentindex])

        # format for each player assigned to currentstats:
        # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

        if game == "1":
            currentstats = username_best_replay.username_pc_sprint(listofusernames[currentindex], game, mode, my_session)
        elif game == "3":
            currentstats = username_best_replay.username_least_blocks(listofusernames[currentindex], game, mode, my_session)
        elif game == "5":
            currentstats = username_best_replay.username_ultra_ppb(listofusernames[currentindex], game, my_session)
        else:
            raise "invalid game"

        write_finalstats_to_file(currentstats, game)

        currentindex += 1

# sorts for all games in general (supports least blocks so far)
def all_games_stats_gather(listofusernames, game, mode):

    if os.path.exists("unorderedstats.txt") == False:
        f = open("unorderedstats.txt", 'x')
        f.close()

    with open("unorderedstats.txt", "r", encoding='utf-8') as filename:
        for line in filename:
            pass
        lastusername = my_stats.unordered_username(line)

        c = 1
        for i in listofusernames:
            if lastusername == i:
                currentindex = c
            c += 1

    my_session = requests.session()

    while len(listofusernames) - currentindex > 0:
        print(currentindex + 1, listofusernames[currentindex])

        currentstats = page_replay_stats.username_all_replay_stats(listofusernames[currentindex], game, mode, my_session)
        for i in currentstats:
            write_finalstats_to_file(i, game)

        currentindex += 1

    file_stuff.duplicate_deleter('unorderedstats.txt')

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
    with open("userleaderboard.txt", "r", encoding='utf8') as filename:

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
    def username_leaderboard_file(url, file_output, my_session = 0):
        time.sleep(1.5)
        # userleaderboard.txt is how all of the page's data will be stored
        # t1 = time.time()
        if my_session == 0:
            r = requests.get(url)
        else:
            r = my_session.get(url)
        # t2 = time.time()
        # print(t1-t2)
        with open(file_output, "w", encoding="utf-8") as filename:
            filename.write(r.text)
            print('request sent')
        file_stuff.file_treater('userleaderboard.txt')

    def file_treater(file_output):

        # takes file and rewrites it to be more friendly to data handling

        with open(file_output, 'r', encoding='utf-8') as filename:
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

        with open(file_output, 'w', encoding='utf-8') as filename:
            filename.writelines(listofstuff)

    def duplicate_deleter(file_input):

        if os.path.exists("newstats.txt") == False:
            f = open("newstats.txt", 'x')
            f.close()
        elif os.path.exists("newstats.txt") == True:
            os.remove("newstats.txt")
            f = open("newstats.txt", 'x')
            f.close()

        with open(file_input, 'r', encoding = 'utf-8') as f:
            stuff = f.readlines()
            new_stuff = []
            previous_line = 0
            for line in stuff:
                if line != previous_line:
                    new_stuff.append(line)
                previous_line = line
            with open('newstats.txt', 'a', encoding='utf-8') as g:
                g.writelines(new_stuff)

        os.remove(file_input)
        os.rename('newstats.txt', file_input)


class page_replay_stats:
    # Gets every replay of a user for a specific game and mode
    def username_all_replay_stats(username, game, mode, my_session):
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
            file_stuff.username_leaderboard_file(url, 'userleaderboard.txt', my_session)

            # adds current page replays to list of all other replays so far
            allpagesstats.extend(page_replay_stats.page_200_replays_stats('userleaderboard.txt'))

            # checks if there are no pages left
            if check_200_replays() == False:
                break

            # sets up next url
            current_last_replay = str(last_time_in_page(game))


        return allpagesstats


    # Convert 200 replay data in userleaderboard.txt into list of tuple of stats
    def page_200_replays_stats(file_input):

        # returns integers where there can be integers (Ex: blocks) and returns strings for others( Ex: date)

        with open(file_input, "r", encoding='utf-8') as filename:

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
                    currentusername = listofstuff[c-2]
                    currentusername = jstris_stats.username(currentusername)

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
                        (currentusername, currenttime, currentblock, currentpps, currentfinesse, currentdate, currentlink))
                c += 1

        return allstats

    def ultra_page_200_replays_stats(file_input):

        # returns integers where there can be integers (Ex: blocks) and returns strings for others( Ex: date)

        with open(file_input, "r", encoding='utf-8') as filename:

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
                    currentusername = listofstuff[c-2]
                    currentusername = jstris_stats.username(currentusername)

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
                        (currentusername,currentscore, currentblock, currentppb , currentpps, currentfinesse, currentdate, currentlink))
                c += 1

        return allstats

# Eventually separate into different class in order to do other things besides grab each user's least blocks
# Sprint PC runs?

class username_best_replay:
    def username_least_blocks(username, game, mode, my_session):
        current_last_replay = "0"
        minblocks = 10 ** 20

        gamemode = username_best_replay.game_to_string(game)
        lines = username_best_replay.mode_to_string(game, mode)

        while 1 == 1:

            # gets next cheese page
            url = "https://jstris.jezevec10.com/{}?display=5&user={}&lines={}&page={}".format(gamemode, username, lines, current_last_replay)
            file_stuff.username_leaderboard_file(url, 'userleaderboard.txt', my_session)

            # Searches if there is a new least blocks
            currentpageblocks = page_replay_stats.page_200_replays_stats('userleaderboard.txt')
            c = 0
            for i in currentpageblocks:
                if minblocks > i[2]:
                    minblocks = i[2]
                    minstats = i
                c += 1

            # checks if there are no pages left
            if check_200_replays() == False:
                break

            # Sets up next url
            current_last_replay = str(last_time_in_page(game))

        return minstats

    def username_pc_sprint(username, game, mode, my_session):
        current_last_replay = "0"
        pcsprint = False

        # converts game and mode to their respective strings to search in url
        gamemode = username_best_replay.game_to_string(game)
        lines = username_best_replay.mode_to_string(game, mode)

        while 1 == 1:

            # gets next page
            url = "https://jstris.jezevec10.com/{}?display=5&user={}&lines={}&page={}".format(gamemode, username, lines, current_last_replay)

            file_stuff.username_leaderboard_file(url, 'userleaderboard.txt', my_session)

            # scrapes stats from current page
            # difference between this and username_least_blocks is that this breaks right away when a pc finish is found
            currentpageblocks = page_replay_stats.page_200_replays_stats('userleaderboard.txt')
            for i in currentpageblocks:
                if int(int(lines[:-1]) * 2.5) == i[2]:
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

    def username_ultra_ppb(username, game, my_session):
        current_last_replay = "100000000000"
        maxstats = False
        maxppb = 0

        # converts game and mode to their respective strings to search in url

        gamemode = username_best_replay.game_to_string(game)

        while 1 == 1:

            # gets current page
            url = "https://jstris.jezevec10.com/" + gamemode + "?display=5&user=" + username + "&page=" + current_last_replay
            url = "https://jstris.jezevec10.com/{}?display=5&user={}&page={}".format(gamemode, username, current_last_replay)

            file_stuff.username_leaderboard_file(url, 'userleaderboard.txt', my_session)

            # scrapes stats from current page
            # difference between this and username_least_blocks is that this breaks right away when a pc finish is found
            currentpageppb = page_replay_stats.ultra_page_200_replays_stats('userleaderboard.txt')
            for i in currentpageppb:
                if i[2] > maxppb:
                    print(i)
                    maxppb = i[3]
                    maxstats = i

            # checks if there are no pages left
            if check_200_replays() == False:
                break

            # Sets up next url
            current_last_replay = str(last_time_in_page(game))

        return maxstats

    def game_to_string(game):
        if game == '1':
            return 'sprint'
        elif game == '3':
            return 'cheese'
        elif game == '5':
            return 'ultra'
        else:
            raise 'not valid game'

    def mode_to_string(game, mode):
        if game == "1":
            if mode == "2":
                return "20L"
            elif mode == "1":
                return "40L"
            elif mode == "3":
                return "100L"
            elif mode == "4":
                return "1000L"
            else:
                raise 'invalid mode'
        elif game == "3":
            if mode == "1":
                return "10L"
            elif mode == "2":
                return "18L"
            elif mode == "3":
                return "100L"
            else:
                raise 'invalid mode'
        else:
            raise 'invalid game'



# Write user's final pb or replay and corresponding stats to unorderedstats.txt
def write_finalstats_to_file(currentstats, game):
    if game != "5":
        with open("unorderedstats.txt", "a", encoding="UTF-8") as filename:
            if type(currentstats) != bool:
                filename.write(my_stats.tuple_to_statsstring(currentstats))
            elif type(currentstats) == bool:
                filename.write("No valid run;\n")
            else:
                raise "error"

    # fix me; actually make this compatible with ultra
    elif game == "5":
        pass
        # with open("unorderedstats.txt", "a", encoding="UTF-8") as filename:
        #     if type(currentstats) != bool:
        #         filename.write(username + "  ")
        #         filename.write("Time: " + jstris_stats.clock_to_seconds(str(currentstats[0]) + "  "))
        #         filename.write("Blocks: " + str(currentstats[1]) + "  ")
        #         filename.write("PPS: " + str(currentstats[2]) + "  ")
        #         filename.write("Finesse: " + str(currentstats[3]) + "  ")
        #         filename.write("Date: " + currentstats[4] + "  ")
        #         filename.write("Link: " + currentstats[5] + " \n")
        #     elif type(currentstats) == bool:
        #         filename.write("No valid run;\n")
        #     else:
        #         raise "error"

