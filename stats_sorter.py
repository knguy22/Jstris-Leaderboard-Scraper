import io
from datetime import date
import stats_interpreter

# stats_sorter takes "unorderedstats.txt" and sorts each username for blocks ascending from lowest blocks (ascend
# from lowest time if blocks are equal);
# the ordered usernames are put into "orderedstats.txt"
def stats_sorter():

    # open the list of unordered least block runs; now have listofusernames

    listofusernames = []
    listofusernames = open_unordered_stats()


    # extract least block runs, index, and pps in list from each username's string; assigns them to tuple
    # use least blocks and pps to sort later

    listofblockruns = []
    listofblockruns = stats_string_to_blocks(listofusernames)
    # sorting algorithm

    listofblockruns = least_blocks_sorting_algorithm(listofblockruns)

    # prepares list of stats from unorderedstatstxt using sorted listofblockruns and writes unorderedstats into
    # orderedstats.txt

    write_stats_to_file(listofblockruns, listofusernames)

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
        timeindex = i.index("Time: ")
        blocksindex = i.index("Blocks: ")
        ppsindex = i.index("PPS: ")
        listofblockruns.append((int(i[blocksindex + 8: ppsindex - 2]),
                                stats_interpreter.clock_to_seconds(i[timeindex + 6: blocksindex - 2]), c))
        c += 1

    return listofblockruns

def least_blocks_sorting_algorithm(listofblockruns):
    # switches two indexes in a list if the lower index has a higher block count than the higher index
    # pretty inefficient; will change later
    # e checks if there has been any sorting for each time the entire list is run through
    # i is the number of iterations; is used for bubble sort
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
            # Compares time if the blocks are the same; lower time is lower number placement on the lsit
            if nextblocks == currentblocks:
                if listofblockruns[d + 1][1] < listofblockruns[d][1]:
                    listofblockruns[d + 1], listofblockruns[d] = listofblockruns[d], listofblockruns[d + 1]
                    e += 1
            d += 1

    return listofblockruns

def write_stats_to_file(listofblockruns, listofusernames):
    # final list of strings
    sortedlistofusernames = []
    for i in listofblockruns:
        sortedlistofusernames.append(listofusernames[i[2]])


    # convert to csv

    sortedlistofusernames = statsformattocsv(sortedlistofusernames)


    # encode for text

    c = 0
    while len(sortedlistofusernames) - c > 0:
        sortedlistofusernames[c] = sortedlistofusernames[c].encode("utf8")
        c += 1


    # write text to final document
    with open("orderedstats.csv", "wb") as f:
        f.writelines(sortedlistofusernames)

def statsformattocsv(sortedlistofusernames):
    # input
    # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

    # output
    # 9747.,Shenanigans,44:30.45,2155,0.81,4692,2020-05-24 00:16:44,https://jstris.jezevec10.com/replay/15847946
    csvlistofusernames = []
    currentcsvusername = ""

    today = date.today()
    csvlistofusernames.append("This leaderboard was last updated " + today.strftime("%B %d, %Y") + "\n")
    csvlistofusernames.append("Ranking,Username,Time,Blocks,PPS,Finesse,Date,Link\n")
    csvlistofusernames.append("\n")


    c = 1
    for i in sortedlistofusernames:
        currentcsvusername = i
        currentcsvusername = str(c) + ".," + currentcsvusername
        c += 1
        currentcsvusername = currentcsvusername.replace("  Time: ", ",")
        currentcsvusername = currentcsvusername.replace("  Blocks: ", ",")
        currentcsvusername = currentcsvusername.replace("  PPS: ", ",")
        currentcsvusername = currentcsvusername.replace("  Finesse: ", ",")
        currentcsvusername = currentcsvusername.replace("  Date: ", ",")
        currentcsvusername = currentcsvusername.replace("  Link: ", ",")
        currentcsvusername += "\n"
        csvlistofusernames.append((currentcsvusername))
    return csvlistofusernames
