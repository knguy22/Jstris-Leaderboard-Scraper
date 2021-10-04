import username_init
import stats_gather
import stats_sorter


if __name__ == '__main__':

    # gathers list of usernames; saves usernames for later if not already there in unorderedname.txt

    listofusernames = username_init.username_init()

    # gets least block runs and respective stats from each player

    stats_gather.stats_gather(listofusernames)

    # gather list of blocks from each stats for each player; outputs sorted stats to "orderedstats.txt"

    stats_sorter.stats_sorter()


    # To do
    # Add gamemode support
    # use a more efficient sorting algorithm
    # support not having minutes in time
    # switch from sorting with pps to sorting with time
    # csv support
    # Multithread requests
