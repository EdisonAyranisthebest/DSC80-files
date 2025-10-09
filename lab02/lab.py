# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def trick_me():
    
    tricky_1 = pd.DataFrame([
        ["A", "X", 10],
        ["B", "Y", 20],
        ["C", "Z", 30],
        ["D", "W", 40],
        ["E", "V", 50],
    ], columns=["Name", "Name", "Age"])
    
    # Save and reload
    tricky_1.to_csv("tricky_1.csv", index=False)
    tricky_2 = pd.read_csv("tricky_1.csv")
    
    return 3


def trick_bool():
    return [4, 12, 4]



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def population_stats(df):
    num_nonnull = df.notna().sum()
    prop_nonnull = num_nonnull / len(df)
    num_distinct = df.nunique(dropna=True)
    prop_distinct = num_distinct / num_nonnull

    stats = pd.DataFrame({
        "num_nonnull": num_nonnull,
        "prop_nonnull": prop_nonnull,
        "num_distinct": num_distinct,
        "prop_distinct": prop_distinct
    })

    return stats


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_common(df, N=10):
    result = pd.DataFrame(index=range(N))  
    
    for col in df.columns:
        counts = df[col].value_counts()     
        values = counts.index.to_list()     
        freqs = counts.values.tolist()      

        while len(values) < N:
            values.append(np.nan)
            freqs.append(np.nan)
        
        result[f"{col}_values"] = values[:N]
        result[f"{col}_counts"] = freqs[:N]
    
    return result


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def super_hero_powers(powers):
    powers_only = powers.drop(columns=["hero_names"])
    hero_with_most = powers.loc[powers_only.sum(axis=1).idxmax(), "hero_names"]

    flyers = powers[powers["Flight"] == True]
    flyers_powers = flyers.drop(columns=["hero_names", "Flight"])
    most_common_flyer_power = flyers_powers.sum().idxmax()

    one_power = powers_only.sum(axis=1) == 1
    single_power_heroes = powers[one_power].drop(columns=["hero_names"])
    most_common_single_power = single_power_heroes.sum().idxmax()

    return [hero_with_most, most_common_flyer_power, most_common_single_power]


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------

def clean_heroes(heroes):
    cleaned = heroes.replace(
        ["-", "", "None", "none", "N/A", "n/a", "Unknown", "unknown", "null", "Null"], 
        np.nan
    )
    cleaned.loc[cleaned['Weight'] <= 0, 'Weight'] = np.nan
    return cleaned

# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def super_hero_stats():
    return [
        "NAME_OF_TALLEST_MUTANT_NO_HAIR",       
        "PUBLISHER_WITH_HIGHEST_HUMAN_PROP",   
        "good" or "bad",                       
        "Marvel Comics" or "DC Comics",        
        "PUBLISHER_NOT_MARVEL_OR_DC",          
        "NAME_OF_OUTLIER_HERO"                 
    ]


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def clean_universities(df):
    df = df.copy()

    # Clean institution names
    df['institution'] = df['institution'].str.replace('\n', ', ', regex=False)

    # broad_impact → int
    df['broad_impact'] = df['broad_impact'].astype(int)

    # Split national_rank -> nation, national_rank_cleaned
    parts = df['national_rank'].str.split(',', n=1, expand=True)
    df['nation'] = parts[0].str.strip()
    df['national_rank_cleaned'] = parts[1].str.strip().astype(int)
    df = df.drop(columns=['national_rank'])

    # Normalize country aliases (the dataset-specific 3 + USA variants)
    df['nation'] = df['nation'].replace({
        'Czechia': 'Czech Republic',
        'UK': 'United Kingdom',
        'Russia': 'Russian Federation',
        'USA': 'United States',
        'U.S.A.': 'United States',
    })

    # R1 public: public + has non-null control, city, state
    df['is_r1_public'] = (
        (df['control'] == 'Public') &
        df['control'].notna() & df['city'].notna() & df['state'].notna()
    )

    return df


def university_info(cleaned):
    state_lowest = (
        cleaned.groupby('state')
        .filter(lambda g: len(g) >= 3)
        .groupby('state')['score'].mean()
        .idxmin()
    )

    top100 = cleaned[cleaned['world_rank'] <= 100]
    prop_faculty = float((top100['quality_of_faculty'] <= 100).mean())  # cast here

    share_private = (
        cleaned.assign(is_r1_public=cleaned['is_r1_public'].fillna(False))
        .groupby('state')['is_r1_public']
        .apply(lambda s: (s == False).mean())
    )
    num_private_states = int((share_private >= 0.5).sum())

    best_in_nation = cleaned[cleaned['national_rank_cleaned'] == 1]
    worst_of_best = best_in_nation.loc[best_in_nation['world_rank'].idxmax(), 'institution']

    return [state_lowest, prop_faculty, num_private_states, worst_of_best]

    # 5) R1 public: public + has non-null control, city, state
    df['is_r1_public'] = (
        (df['control'] == 'Public') &
        df['control'].notna() & df['city'].notna() & df['state'].notna()
    )

    return df


