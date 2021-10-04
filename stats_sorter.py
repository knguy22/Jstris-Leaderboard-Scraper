import io

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

    listofblockruns = sorting_algorithm(listofblockruns)

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
