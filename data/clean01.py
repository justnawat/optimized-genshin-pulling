#! python3

import os
import sys
import pandas as pd
import json


def generate_default_df():
    return pd.DataFrame({
        "DateTime": [],
        "Type": [],
        "Rarity": [],
        "Banner": []
    })


if len(sys.argv) != 2:
    print("Usage ./clean01.py <base/path/to/data/>")

base_path = sys.argv[1]
sub_dirs = filter(lambda s: s.isnumeric(), os.listdir(f"{base_path}/01/"))

with open(f"{base_path}/translation.json", "r") as fp:
    translation = json.load(fp)


combined_df = generate_default_df()

for sub_dir in sub_dirs:
    def load_df(banner: int) -> pd.DataFrame:
        current_file_path = f"{base_path}/01/{sub_dir}/gacha{banner}.csv"
        if os.path.exists(current_file_path) and os.path.getsize(current_file_path) != 0:
            print(f"reading: {current_file_path}")
            data = pd\
                .read_csv(current_file_path)\
                .rename(columns=translation["col"])
            data["Type"] = data["Type"]\
                .replace(translation["type"])
            data = data.drop(["Name"], axis=1)
            data["Banner"] = banner

            return data
        return generate_default_df()

    permanent_df = load_df(200)
    character_banner_df = load_df(301)
    weapon_banner_df = load_df(302)

    combined_df = pd.concat(
        [combined_df, permanent_df, character_banner_df, weapon_banner_df])

combined_df.to_csv(f"{base_path}/data01.csv", index=False)
