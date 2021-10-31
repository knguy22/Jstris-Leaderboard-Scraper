import io
from datetime import date
from stats_interpreter import my_stats

# stats_sorter takes "unorderedstats.txt" and sorts each username for blocks ascending from lowest blocks (ascend
# from lowest time if blocks are equal);
# the ordered usernames are put into "orderedstats.txt"
def stats_sorter(game):

    # open the list of unordered least block runs; now have listofusernames

    listofusernames = []
    listofusernames = open_unordered_stats()



    # cheese least blocks

    if game == "3":
        listofblockruns = stats_string_to_blocks(listofusernames)
        listofblockruns = least_blocks_sorting_algorithm(listofblockruns)

    # pc sprint finish

    elif game == "1":
        listofpcruns = stats_string_to_pc_sprint(listofusernames)
        listofpcruns = sprint_pc_sorting_algorithm(listofpcruns)

    # prepares list of stats from unorderedstatstxt using sorted listofblockruns and writes unorderedstats into
    # orderedstats.txt

    write_stats_to_file(listofpcruns, listofusernames)

def open_unordered_stats():
    with io.open("unorderedstats.txt", encoding='utf-8') as f:
        stringofusernames = f.readlines()

    listofusernames = []
    for i in stringofusernames:
        listofusernames.append(i.rstrip())

    return listofusernames

def stats_string_to_blocks(listofusernames):
    # extract least block runs, index, and pps in list from each username's string; assigns them to tuple
    # use least blocks and pps to sort later

    c = 0
    listofblockruns = []
    for i in listofusernames:
        listofblockruns.append((my_stats.unordered_block(i), my_stats.unordered_clock_to_seconds(i), c))
        c += 1

    return listofblockruns

def least_blocks_sorting_algorithm(listofblockruns):
    # sorting algorithm

    # uses bubble sorting
    # e checks if there has been any sorting for each time the entire list is run through
    # i is the number of iterations; is used for bubble sort
    currentblocks = 0
    nextblocks = 0
    e = 1
    iterations = 0
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

        iterations += 1
        if iterations % 10000 == 0:
            print(iterations)

    return listofblockruns

def stats_string_to_pc_sprint(listofusernames):
    # extract least block runs, index, and pps in list from each username's string; assigns them to tuple
    # use least blocks and pps to sort later

    # string format:
    # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

    c = 0
    listofpcruns = []
    for i in listofusernames:
        if ("No valid run" in i) == False:
            listofpcruns.append((my_stats.unordered_clock_to_seconds(i), c))
        c += 1

    return listofpcruns

def sprint_pc_sorting_algorithm(listofpcsprints):
    # sorting algorithm

    # uses bubble sorting
    # e checks if there has been any sorting for each time the entire list is run through
    # i is the number of iterations; is used for bubble sort
    currentsprint = 0
    nextsprint = 0
    e = 1
    iterations = 0
    while e != 0:

        # d iterates through the entire list of runs over and over to sort
        d = 0
        e = 0
        while len(listofpcsprints) - d - 1 > 0:
            currentsprint = listofpcsprints[d][0]
            nextsprint = listofpcsprints[d + 1][0]
            if nextsprint < currentsprint:
                listofpcsprints[d + 1], listofpcsprints[d] = listofpcsprints[d], listofpcsprints[d + 1]
                e += 1
            d += 1

        iterations += 1
        print(iterations)


    return listofpcsprints

def write_stats_to_file(listofblockruns, listofusernames):
    # final list of strings
    sortedlistofusernames = []
    for i in listofblockruns:
        sortedlistofusernames.append(listofusernames[i[len(i) - 1]])


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
    csvlistofusernames.append("Last updated:," + today.strftime("%B %d, %Y") + "\n")
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
