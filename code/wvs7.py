from newcommon import *

ANES_FN = './WVS_Cross-National_Wave_7_filtered.csv' 

# For WVS7
fields_of_interest = {
    'Q290': {  # ANES V161310x — race/ethnicity
        "template": "sRacially, I am XXX.",
        "valmap": {
            1: 'white',
            2: 'black',
            3: 'South Asian',
            4: 'East Asian',
            5: 'Arabic or Central Asian',
            6: 'of another ethnic group'
        }
    },
    'Q200': {  # ANES V162174 — discuss politics with others
        "template": "XXX",
        "valmap": {
            1: 'I frequently discuss political matters with my friends.',
            2: 'I occasionally discuss political matters with my friends.',
            3: 'I never discuss political matters with my friends.'
        }
    },
    'Q240': {  # ANES V161126 — ideology (left–right self-placement, 1–10)
        "template": "On a left-right scale, I place myself XXX.",
        "valmap": {
            1: "on the far left",
            2: "on the left",
            3: "left of center",
            4: "slightly left of center",
            5: "at the center",
            6: "at the center",
            7: "slightly right of center",
            8: "right of center",
            9: "on the right",
            10: "on the far right"
        }
    },
    'Q171': {  # ANES V161244 — religious attendance
        "template": "I XXX.",
        "valmap": {
            1: "attend religious services more than once a week",
            2: "attend religious services once a week",
            3: "attend religious services once a month",
            4: "attend religious services only on special holy days",
            5: "attend religious services once a year",
            6: "attend religious services less than once a year",
            7: "never attend religious services"
        }
    },
    'Q262': {  # ANES V161267 — age
        "template": "I am XXX years old.",
        "valmap": {}
    },
    'Q260': {  # ANES V161342 — sex
        "template": "I am a XXX.",
        "valmap": {1: "man", 2: "woman"}
    },
    'Q199': {  # ANES V162256 — political interest
        "template": "I am XXX interested in politics.",
        "valmap": {1: "very", 2: "somewhat", 3: "not very", 4: "not at all"}
    }
}