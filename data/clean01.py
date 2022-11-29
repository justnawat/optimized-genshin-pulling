#! python3

import os
import sys
import pandas as pd


def generate_default_df():
    return pd.DataFrame({
        "Date": [],
        "Time": [],
        "Type": [],
        "Rarity": [],
        "Banner": []
    })


if len(sys.argv) != 2:
    print("Usage ./clean01.py <base/path/to/data/>")

base_path = sys.argv[1]
sub_dirs = filter(lambda s: s.isnumeric(), os.listdir(f"{base_path}/01/"))

translation = {
    "抽卡时间": "DateTime",
    "名称": "Name",
    "类别": "Type",
    "星级": "Rarity",
    "武器": "Weapon",
    "角色": "Character"
}

combined_df = generate_default_df()

for sub_dir in sub_dirs:
    def load_df(banner: int) -> pd.DataFrame:
        current_file_path = f"{base_path}/01/{sub_dir}/gacha{banner}.csv"
        if os.path.exists(current_file_path) and os.path.getsize(current_file_path) != 0:
            print(f"reading: {current_file_path}")
            data = pd\
                .read_csv(current_file_path)\
                .rename(columns=translation)
            data["Type"] = data["Type"].replace(translation)
            data = data.drop(["Name"], axis=1)
            data["Banner"] = banner

            return data
        return generate_default_df()

    permanent_df = load_df(200)
    character_banner_df = load_df(301)
    weapon_banner_df = load_df(302)

    combined_df = pd.concat(
        [combined_df, permanent_df, character_banner_df, weapon_banner_df])

combined_df\
    .reindex(columns=["Rarity", "DateTime", "Banner", "Type"])\
    .astype({"Banner": int, "Rarity": int})\
    .to_csv(f"{base_path}/data01.csv", index=False)
