import username_init
import stats_gather
import stats_sorter
import math
import stats_interpreter
import concurrent.futures
import requests
import time

def mainfunction():

    # game:
    # 1 = sprint, 3 = cheese, 4 = survival, 5 = ultra

    # mode: (for sprint/cheese)
    # 1 = 40L/10L, 2 = 20L/18L, 3 = 100L, 4 = 1000L
    # any other gamemode should be 1

    game = "1"
    mode = "2"

    # gathers list of usernames; saves usernames for later if not already there in unorderedname.txt

    listofusernames = username_init.username_init(game, mode)

    # gets least block runs and respective stats from each player

    stats_gather.stats_gather(listofusernames, game, mode)

    # gather list of blocks from each stats for each player; outputs sorted stats to "orderedstats.txt"

    stats_sorter.stats_sorter(game)

if __name__ == '__main__':


    mainfunction()
    # thing = requests.get("https://gauchospace.ucsb.edu/courses/pluginfile.php/17994618/mod_resource/content/8/Powerpoint%20Five_Who%20is%20a%20Constituionalist_Post.pdf")
    # data = thing.text
    # filename = open("leaderboard.txt", "w")
    # filename.write(data + "\n")
    # filename.close()

