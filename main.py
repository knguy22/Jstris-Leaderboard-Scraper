import username_init
import stats_gather
import stats_sorter
import stats_interpreter
import requests
import time

def indiv_main_function():

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

    stats_gather.indiv_player_stats_gather(listofusernames, game, mode)

    # gather list of blocks from each stats for each player; outputs sorted stats to "orderedstats.txt"

    stats_sorter.stats_sorter(game)

def all_game_function():

    game = "3"
    mode = "3"


    # gathers list of usernames; saves usernames for later if not already there in unorderedname.txt

    listofusernames = username_init.username_init(game, mode)

    # gets all games from each player

    stats_gather.all_games_stats_gather(listofusernames, game, mode)

    # sorts all stats and outputs sorted stats to "orderedstats.txt"

    stats_sorter.stats_sorter(game)


def num_sub_blocks_all_games(username, blocks):
    url = "https://jstris.jezevec10.com/cheese?display=5&user={}&lines=100L".format(username)
    stats_gather.username_leaderboard_file(url)
    my_stats = stats_gather.page_all_replay_stats(username=username, game='3', mode='3')
    num_runs = 0
    for stats in my_stats:
        if stats[1] < blocks:
            print(stats)
            num_runs += 1
    return num_runs

def num_ppb_front_page(username, ppb):
    url = "https://jstris.jezevec10.com/ultra?display=5&user={}".format(username)
    stats_gather.username_leaderboard_file(url)
    my_stats = stats_gather.ultra_page_200_replays_stats()
    num_runs = 0
    for stats in my_stats:
        if stats[2] > ppb:
            print(stats)
            num_runs += 1
    return num_runs



if __name__ == '__main__':

    # print(num_sub_blocks_front_page('qinghan', 220))
    all_game_function()

    # mainfunction()

    # stats_gather.username_leaderboard_file("https://harddrop.com/forums/index.php?showtopic=1000")
    # print(stats_gather.username_ultra_ppb("kevinhe828", "5"))
    # print(num_sub_blocks_front_page("qwerty", 260))