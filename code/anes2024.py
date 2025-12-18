from common import *

######## No changes from 2020
SEP=','
OUTPUT_FN = "./full_results_2024.pkl"
OUTPUT_CSV = "./full_results_2024.csv"
ID_COL = "V200001"
VOTE_COL = "V202110x"  # 1-Biden, 2-Trump, 3-Jorgensen, 4-Hawkins
K1 = "trump"
K2 = "biden"
tok_sets = {
    "trump": gen_variants([ "donald", "trump", "republican", "conservative"]),
    "biden": gen_variants([ "joe", "joseph", "biden", "democrat", "democratic", "liberal"])
}

query = "In the 2020 presidential election, Donald Trump is the Republican candidate, "
query += "and Joe Biden is the Democratic candidate, and I voted for"
######## No changes from 2020

ANES_FN = './2024 ANES_test.csv'


fields_of_interest = {
    'V241501x': {
        "template": "Racially, I am XXX.",
        "valmap": {1: 'white', 2: 'black', 3: 'asian', 4: 'native American', 5: 'hispanic'}
    },
    # 'V202022': {
    #     "template": "The respondent XXX.",
    #     "valmap": {
    #         1: 'likes to discuss politics with their family and friends',
    #         2: 'never discusses politics with their family or friends'
    #     }
    # }, # the relevant question is V242025 but asking 'How many days in the past week did you talk about politics with family or friends?' and with different answer options, so removed
    'V241709': {
        "template": "Ideologically, I am XXX.",
        "valmap": {
            1: "extremely liberal",
            2: "liberal",
            3: "slightly liberal",
            4: "moderate",
            5: "slightly conservative",
            6: "conservative",
            7: "extremely conservative"
        }
    },
    'V241707': {
        "template": "Politically, I am XXX.",
        "valmap": {
            1: "a strong democrat",
            2: "a weak Democrat",
            3: "an independent who leans Democratic",
            4: "an independent",
            5: "an independent who leans Republican",
            6: "a weak Republican",
            7: "a strong Republican"
        }
    },
    'V241439': {
        "template": "I XXX.",
        "valmap": {1: "attend church", 2: "do not attend church"}
    },
    'V241457': {
        "template": "I am XXX years old.",
        "valmap": {}
    },
    'V241550': {
        "template": "I am a XXX.",
        "valmap": {1: "man", 2: "woman"}
    },
    'V242400': {
        "template": "I am XXX interested in politics.",
        "valmap": {1: "very", 2: "somewhat", 3: "not very", 4: "not at all"}
    }
}
