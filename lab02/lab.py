# lab.py 

import os
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------

def trick_me():
    df = pd.DataFrame(
        [["A", "X", 10],
         ["B", "Y", 20],
         ["C", "Z", 30],
         ["D", "W", 40],
         ["E", "V", 50]],
        columns=["Name", "Name", "Age"]
    )
    df.to_csv("tricky_1.csv", index=False)
    _ = pd.read_csv("tricky_1.csv") 
    return 3


def trick_bool():
    return [4, 10, 13]


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------

def population_stats(df: pd.DataFrame) -> pd.DataFrame:
    num_nonnull = df.notna().sum()
    prop_nonnull = num_nonnull / len(df)
    num_distinct = df.nunique(dropna=True)
    prop_distinct = num_distinct / num_nonnull

    return pd.DataFrame({
        "num_nonnull": num_nonnull,
        "prop_nonnull": prop_nonnull,
        "num_distinct": num_distinct,
        "prop_distinct": prop_distinct
    })


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------

def most_common(df: pd.DataFrame, N: int = 10) -> pd.DataFrame:
    result = pd.DataFrame(index=range(N))
    for col in df.columns:  
        counts = df[col].value_counts(dropna=False)
        vals = counts.index.tolist()
        freqs = counts.values.tolist()
        if len(vals) < N:
            vals = vals + [np.nan] * (N - len(vals))
            freqs = freqs + [np.nan] * (N - len(freqs))
        result[f"{col}_values"] = vals[:N]
        result[f"{col}_counts"] = freqs[:N]
    return result


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------

def super_hero_powers(powers: pd.DataFrame):
    powers_only = powers.drop(columns=["hero_names"])
    hero_with_most = powers.loc[powers_only.sum(axis=1).idxmax(), "hero_names"]

    flyers = powers[powers.get("Flight", False) == True]
    flyers_powers = flyers.drop(columns=["hero_names"])
    if "Flight" in flyers_powers.columns:
        flyers_powers = flyers_powers.drop(columns=["Flight"])
    most_common_flyer_power = flyers_powers.sum().idxmax()

    one_power_mask = powers_only.sum(axis=1) == 1
    single_power_heroes = powers.loc[one_power_mask].drop(columns=["hero_names"])
    most_common_single_power = single_power_heroes.sum().idxmax()

    return [hero_with_most, most_common_flyer_power, most_common_single_power]


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------

def clean_heroes(heroes: pd.DataFrame) -> pd.DataFrame:
    cleaned = heroes.replace(
        ["-", "", "None", "none", "N/A", "n/a", "Unknown", "unknown", "null", "Null"],
        np.nan
    )
    for col in ["Weight", "Height"]:
        numeric = pd.to_numeric(cleaned[col], errors="coerce")
        cleaned.loc[numeric <= 0, col] = np.nan
        cleaned[col] = numeric
    return cleaned


# ---------------------------------------------------------------------
# QUESTION 6 
# ---------------------------------------------------------------------

def super_hero_stats():
    heroes_fp = Path("data") / "superheroes.csv"
    df = pd.read_csv(heroes_fp)
    df = clean_heroes(df)

    NAME_COL = "name"
    if NAME_COL not in df.columns:
        NAME_COL = "Name"

    if "Height" in df.columns:
        df["Height"] = pd.to_numeric(df["Height"], errors="coerce")
    if "Weight" in df.columns:
        df["Weight"] = pd.to_numeric(df["Weight"], errors="coerce")

    q1_mask = (df.get("Race") == "Mutant") & (df.get("Hair color") == "No Hair")
    tallest_mutant_no_hair = (
        df.loc[q1_mask].sort_values("Height", ascending=False).iloc[0][NAME_COL]
    )

    known_pub = df["Publisher"].notna()
    by_pub = df[known_pub].groupby("Publisher", dropna=False)
    pub_counts = by_pub.size().rename("n")
    prop_human = by_pub["Race"].apply(lambda s: (s == "Human").mean()).rename("prop_human")
    pub_stats = pd.concat([pub_counts, prop_human], axis=1)
    pub_stats = pub_stats.loc[pub_stats["n"] > 5]
    top_human_pub = pub_stats.sort_values(["prop_human", "Publisher"],
                                          ascending=[False, True]).index[0]

    mask_gb = df["Alignment"].isin(["good", "bad"]) & df["Height"].notna()
    mean_heights = df.loc[mask_gb].groupby("Alignment")["Height"].mean()
    taller_side = "good" if mean_heights.get("good", -np.inf) > mean_heights.get("bad", -np.inf) else "bad"

    def prop_bad_for(publisher):
        sub = df[df["Publisher"] == publisher]
        return float((sub["Alignment"] == "bad").mean()) if len(sub) else 0.0
    worse_pub = "Marvel Comics" if prop_bad_for("Marvel Comics") > prop_bad_for("DC Comics") else "DC Comics"

    known = df["Publisher"].notna()
    other = df.loc[known & ~df["Publisher"].isin(["Marvel Comics", "DC Comics"]), "Publisher"]
    top_other_publisher = other.value_counts().idxmax()

    if "Weight" not in df.columns:
        df["Weight"] = np.nan
    h_mean, h_std = df["Height"].mean(skipna=True), df["Height"].std(skipna=True)
    w_mean, w_std = df["Weight"].mean(skipna=True), df["Weight"].std(skipna=True)
    outlier_mask = (df["Height"] > h_mean + h_std) & (df["Weight"] < w_mean - w_std)
    outlier_name = df.loc[outlier_mask, NAME_COL].iloc[0]

    return [
        tallest_mutant_no_hair,  
        top_human_pub,           
        taller_side,             
        worse_pub,              
        top_other_publisher,     
        outlier_name             
    ]


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------

def clean_universities(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["institution"] = df["institution"].str.replace("\n", ", ", regex=False)

    df["broad_impact"] = df["broad_impact"].astype(int)

    parts = df["national_rank"].str.split(",", n=1, expand=True)
    df["nation"] = parts[0].str.strip()
    df["national_rank_cleaned"] = parts[1].str.strip().astype(int)
    df = df.drop(columns=["national_rank"])

    df["nation"] = df["nation"].replace({
        "Czechia": "Czech Republic",
        "UK": "United Kingdom",
        "Russia": "Russian Federation",
        "USA": "United States",
        "U.S.A.": "United States",
    })

    df["is_r1_public"] = (
        (df["control"] == "Public") &
        df["control"].notna() & df["city"].notna() & df["state"].notna()
    )

    return df


def university_info(cleaned: pd.DataFrame):
    state_lowest = (
        cleaned.groupby("state")
        .filter(lambda g: len(g) >= 3)
        .groupby("state")["score"].mean()
        .idxmin()
    )

    top100 = cleaned[cleaned["world_rank"] <= 100]
    prop_faculty = float((top100["quality_of_faculty"] <= 100).mean())

    share_private = (
        cleaned.assign(is_r1_public=cleaned["is_r1_public"].fillna(False))
        .groupby("state")["is_r1_public"]
        .apply(lambda s: (s == False).mean())
    )
    num_private_states = int((share_private >= 0.5).sum())

    top_in_nation = cleaned[cleaned["national_rank_cleaned"] == 1]
    worst_of_best = top_in_nation.loc[top_in_nation["world_rank"].idxmax(), "institution"]

    return [state_lowest, prop_faculty, num_private_states, worst_of_best]
