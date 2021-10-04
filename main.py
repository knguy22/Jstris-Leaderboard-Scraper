import username_init
import stats_gather
import stats_sorter

if __name__ == '__main__':
    # gathers list of usernames; saves usernames for later if not already there in unorderedname.txt

    listofusernames = username_init.username_init()

    # gets least block runs and respective stats from each player

    stats_gather.stats_gather(listofusernames)

    # gather list of blocks from each stats part

    stats_sorter.stats_sorter()

    # To do
    # Add gamemode support
    # support not having minutes in time
    # look into spreadsheets?
    # Multithread requests
