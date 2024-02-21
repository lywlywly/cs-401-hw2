import datetime
import json
import os
import pickle

import pandas as pd
from fpgrowth_py import fpgrowth

import urllib.request
import ssl


dataset_url = os.environ.get(
    "DATASET_URL",
    "https://homepages.dcc.ufmg.br/~cunha/hosted/cloudcomp-2023s2-datasets/2023_spotify_ds1.csv",
)
data_dir = os.environ.get("DATA_DIR", "/data")
filename = dataset_url.split("/")[-1]


def download_file(url, destination_directory):
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        filename = url.split("/")[-1]
        save_location = os.path.join(destination_directory, filename)
        with urllib.request.urlopen(url, context=ssl_context) as response, open(
            save_location, "wb"
        ) as out_file:
            out_file.write(response.read())
        print("Download success")
    except Exception as e:
        print(f"Error downloading: {e}")


def download_dataset():
    os.makedirs("/data/spotify", exist_ok=True)
    save_directory = "/data/spotify"
    download_file(dataset_url, save_directory)


def prepare_data():
    download_dataset()
    df = pd.read_csv(os.path.join(data_dir, f"spotify/{filename}"))
    new_df = df[["pid", "track_name"]]
    grouped = new_df.groupby("pid")["track_name"].apply(list).tolist()

    return grouped


def run():
    grouped = prepare_data()
    print("Running fpgrowth...")
    _, rules = fpgrowth(grouped, minSupRatio=0.08, minConf=0.5)
    # rules_dict = {tuple(r[0]): r[1] for r in rules}
    rules_dict: dict[tuple[str], set[str]] = {}
    for item in rules:
        it = list(item[0])
        it.sort()
        key = tuple(it)
        values = set(item[1])
        if key in rules_dict:
            rules_dict[key].update(values)
        else:
            rules_dict[key] = values

    os.makedirs("/data/ml", exist_ok=True)

    with open(os.path.join(data_dir, "ml/rule.pickle"), "wb") as file:
        pickle.dump(rules_dict, file)

    with open(os.path.join(data_dir, "ml/rule.info"), "w") as file:
        current_date = datetime.datetime.now()
        info = {"date": str(current_date)}
        json.dump(info, file)


def main():
    run()


main() if __name__ == "__main__" else None
