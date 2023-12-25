import csv
import json
import os

def concat_to_csv(dest, dataDir):
    data_list = []
    header = {}

    for file in os.listdir(dataDir):
        assert file.endswith(".json")

        # Load new file
        file_path = os.path.join(dataDir, file)
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
            data_list.append(json_data)

        # Initialize header
        if not header:
            header = list(data_list[0][0].keys())

        # Create the destination csv if necessary
        if not os.path.isfile(dest):
            with open(dest, 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=header)
                writer.writeheader()

        # Concatenate into csv from cache
        # This is done because the total amount of games may not fit in memory, so we write to files in chunks
        if len(data_list) >= 100:

            # Append the data list
            for player in data_list:
                with open(dest, 'a', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=header)
                    writer.writerows(player)

            # Clear the data list for the next batch
            data_list = []

    # After processing all JSON files, write any remaining data to the CSV file
    for player in data_list:
        with open(dest, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writerows(player)

if __name__ == "__main__":
    concat_to_csv("output/test.csv", "output/playerstats")
