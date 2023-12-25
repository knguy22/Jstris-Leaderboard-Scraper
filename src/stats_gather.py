import os
import json

from jstrisuser import UserIndivGames

# stats_gather takes that list of usernames and for each username
# finds desired replay from each user with the replay's corresponding stats and link
# all of these things are stored in "unorderedstats.txt"

# sorts for all games in general (supports least blocks so far)
def gather_all_games(storage_dir, list_of_usernames, game, mode):
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)

    finished_players = 1
    files = os.listdir(storage_dir)
    for file in files:
        list_of_usernames.remove(file[:-5]) # remove .json
        finished_players += 1

    for i, username in enumerate(list_of_usernames):
        print(i + finished_players, username) 
        currentstats = UserIndivGames(username, game, mode)
        assert len(currentstats.all_replays) > 0

        with open(f"{storage_dir}/{username}.json", 'w') as f:
            float_new_username_stats = replace_decimals(currentstats.all_replays)
            f.write(json.dumps(float_new_username_stats))



def replace_decimals(obj):
    """
    Replaces objects with Decimal class with floats (this undoes ijson turning all floats into Decimal)
    :param obj: nested dictionary/list
    :return: obj:
    """

    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_decimals(obj[k])
        return obj
    # Replaces decimal type without replacing ints or strs
    try:
        if obj is None or type(obj) in (int, str):
            raise ValueError
        return float(obj)
    except ValueError:
        return obj
