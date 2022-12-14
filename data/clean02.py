#! python3

import os
import sys
import pandas as pd
import random as rd


SAMPLE_SIZE = 200 if len(sys.argv) != 3 else -1 if sys.argv[2] == "all" else int(sys.argv[2])


def generate_default_df():
    return pd.DataFrame({
        "Date": [],
        "Time": [],
        "Type": [],
        "Rarity": [],
        "Banner": []
    })


if len(sys.argv) != 2:
    print("Usage ./clean02.py <base/path/to/data/>")

base_path = sys.argv[1]
all_subdirs = os.listdir(f"{base_path}/02/")
sub_dirs = rd.sample(all_subdirs, SAMPLE_SIZE if SAMPLE_SIZE != -1 else len(all_subdirs))

translation = {
    "name": "Name",
    "gacha_type": "Banner",
    "item_type": "Type",
    "rank_type": "Rarity",
    "gacha_id": "Pull ID",
    "gacha_time": "DateTime",
    0: "Character",
    1: "Weapon"
}


combined_df = generate_default_df()

for i, sub_dir in enumerate(sub_dirs):
    print(i, end=' ')

    def load_df() -> pd.DataFrame:
        current_file_path = f"{base_path}/02/{sub_dir}"
        if os.path.getsize(current_file_path) != 0:
            print(f"reading: {current_file_path}")
            data = pd\
                .read_csv(current_file_path)\
                .rename(columns=translation)
            data["Type"] = data["Type"].replace(translation)
            data = data.drop(["Name", "Pull ID"], axis=1)
            data = data[data.Banner != 100]

            return data
        return generate_default_df()

    new_df = load_df()
    combined_df = pd.concat([combined_df, new_df])

combined_df\
    .reindex(columns=["Rarity", "DateTime", "Banner", "Type"])\
    .astype({"Banner": int, "Rarity": int})\
    .to_csv(f"{base_path}/data02.csv", index=False)
