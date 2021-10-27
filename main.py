import username_init
import stats_gather
import stats_sorter
import stats_interpreter

def mainfunction():

    # game:
    # 1 = sprint, 3 = cheese, 4 = survival, 5 = ultra

    # mode: (for sprint/cheese)
    # 1 = 40L/10L, 2 = 20L/18L, 3 = 100L, 4 = 1000L
    # any other gamemode should be 1

    game = "3"
    mode = "3"

    # gathers list of usernames; saves usernames for later if not already there in unorderedname.txt

    listofusernames = username_init.username_init(game, mode)

    # gets least block runs and respective stats from each player

    stats_gather.stats_gather(listofusernames, game, mode)

    # gather list of blocks from each stats for each player; outputs sorted stats to "orderedstats.txt"

    stats_sorter.stats_sorter(game)

if __name__ == '__main__':


    # mainfunction()

    # stats_gather.username_leaderboard_file("https://jstris.jezevec10.com/ultra?display=5&user=fortissim2")
    print(stats_gather.username_ultra_ppb("zepheniah", "5"))
