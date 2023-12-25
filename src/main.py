import username_init
import stats_gather
import stats_csv

# game:
# 1 = sprint, 3 = cheese, 4 = survival, 5 = ultra
game = "1"

# mode: (for sprint/cheese)
# 1 = 40L/10L, 2 = 20L/18L, 3 = 100L, 4 = 1000L
# any other gamemode should be 1
mode = "1"

# where all players that are to be scraped are stored
usernamesFile = "output/usernames.txt"

# each player is given a separate JSON file in this directory
storageDir = "output/sprint40stats"

# final csv containing all games
fileDest = "output/sprint40.csv"


def scrape_jstris_leaderboard():
    # gathers list of usernames; saves usernames for later if not already there in usernames.txt
    listofusernames = username_init.get_usernames(game, mode, usernamesFile)

    # gets all games from each player
    stats_gather.gather_all_games(storageDir, listofusernames, game, mode)

    # sorts all stats and outputs sorted stats to "orderedstats.txt"
    stats_csv.concat_to_csv(fileDest, storageDir)

if __name__ == '__main__':
    scrape_jstris_leaderboard()
