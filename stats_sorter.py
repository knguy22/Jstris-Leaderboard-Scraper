import io
from datetime import date
from stats_interpreter import my_stats
import operator

# sorts unorderedstats.txt to desired specifications
# the ordered usernames are put into "orderedstats.txt"
def stats_sorter(game):

    # open the list of unordered least block runs; now have listofusernames

    listofusernames = []
    listofusernames = open_unordered_stats('unorderedstats.txt')



    # sorts by cheese least blocks; by time if blocks are the same
    if game == "3":
        listofruns = stats_string_to_runs(listofusernames)
        listofruns = sorted(listofruns, key=operator.itemgetter(2,1))

    # sorts by pc sprint finish
    elif game == "1":
        listofruns = stats_string_to_runs(listofusernames)
        listofruns = sorted(listofruns, key=operator.itemgetter(1))

    # prepares list of stats from unorderedstatstxt using sorted listofblockruns and writes unorderedstats into
    # orderedstats.txt

    write_stats_to_file(listofruns, listofusernames, usecsv= True)

def open_unordered_stats(filename):
    with io.open(filename, encoding='utf-8') as f:
        stringofusernames = f.readlines()

    listofusernames = []
    for i in stringofusernames:
        listofusernames.append(i.rstrip())

    return listofusernames


def stats_string_to_runs(listofusernames):
    # extracts the tuple of stats definied in stats_interpreter.py
    # use least blocks and pps to sort later

    listofblockruns = []
    for i in listofusernames:
        if i != "No valid run;":
            listofblockruns.append(my_stats.statsstring_to_tuple(i))

    return listofblockruns


def write_stats_to_file(listofblockruns, listofusernames, usecsv):
    # final list of strings
    sortedlistofusernames = []
    for i in listofblockruns:
        sortedlistofusernames.append(my_stats.tuple_to_statsstring(i))


    # convert to csv

    sortedlistofusernames = statsformattocsv(sortedlistofusernames, usecsv)

    # write text to final document
    with open("orderedstats.csv", "w", encoding='utf-8') as f:
        f.writelines(sortedlistofusernames)

def statsformattocsv(sortedlistofusernames, usecsv):
    # input
    # Vince_HD  Time: 1:43.365  Blocks: 240  PPS: 2.32  Finesse: 9  Date: 2020-03-12 08:27:26  Link: https://jstris.jezevec10.com/replay/12611720

    # output
    # 9747.,Shenanigans,44:30.45,2155,0.81,4692,2020-05-24 00:16:44,https://jstris.jezevec10.com/replay/15847946
    csvlistofusernames = []
    currentcsvusername = ""

    today = date.today()


    c = 1
    if usecsv == False:
        csvlistofusernames.append("Last updated: " + today.strftime("%B %d, %Y") + "\n")
        csvlistofusernames.append("\n")
        for i in sortedlistofusernames:
            csvlistofusernames.append(str(c) + ". " + i)
            c += 1
    else:
        csvlistofusernames.append("Last updated:," + today.strftime("%B %d, %Y") + "\n")
        csvlistofusernames.append("Ranking,Username,Time,Blocks,PPS,Finesse,Date,Link\n")
        csvlistofusernames.append("\n")
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
            csvlistofusernames.append((currentcsvusername))
    return csvlistofusernames
