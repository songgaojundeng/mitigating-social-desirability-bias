from common import *

WVS_FN = "./WVS_Wave_7_NLD.csv"

# For WVS7
fields_of_interest = {
    'Q275': {  # ANES — no direct analog; education added for cross-country comparability (ISCED 2011)
        "template": "My highest level of education is XXX.",
        "valmap": {
            0: 'early childhood education or no formal education',
            1: 'primary education',
            2: 'lower secondary education',
            3: 'upper secondary education',
            4: 'post-secondary non-tertiary education',
            5: 'short-cycle tertiary education',
            6: 'a bachelor\'s degree or equivalent',
            7: 'a master\'s degree or equivalent',
            8: 'a doctoral degree or equivalent',
        }
    },
    'Q288R': {  # WVS recoded household income (low/middle/high); preferred over raw 10-step Q288
        "template": "My household income is XXX.",
        "valmap": {
            1: 'low',
            2: 'middle',
            3: 'high',
        }
    },
    'Q290': {  # ANES V161310x — race/ethnicity
        "template": "My ethnic background is XXX.",
        "valmap": {
            528001: 'white',
            528002: 'black',
            528003: 'South Asian',
            528004: 'East Asian',
            528005: 'Arabic or Central Asian',
            528999: 'of another ethnic group'
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


fields_of_interest_third = {
    'Q275': {  # ANES — no direct analog; education added for cross-country comparability (ISCED 2011)
        "template": "The respondent's highest level of education is XXX.",
        "valmap": {
            0: 'early childhood education or no formal education',
            1: 'primary education',
            2: 'lower secondary education',
            3: 'upper secondary education',
            4: 'post-secondary non-tertiary education',
            5: 'short-cycle tertiary education',
            6: 'a bachelor\'s degree or equivalent',
            7: 'a master\'s degree or equivalent',
            8: 'a doctoral degree or equivalent',
        }
    },
    'Q288R': {  # WVS recoded household income (low/middle/high); preferred over raw 10-step Q288
        "template": "The respondent's household income is XXX.",
        "valmap": {
            1: 'low',
            2: 'middle',
            3: 'high',
        }
    },
    'Q290': {  # ANES V161310x — race/ethnicity
        "template": "The respondent's ethnic background is XXX.",
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
            1: 'The respondent frequently discusses political matters with their friends.',
            2: 'The respondent occasionally discusses political matters with their friends.',
            3: 'The respondent never discusses political matters with their friends.'
        }
    },
    'Q240': {  # ANES V161126 — ideology (left–right self-placement, 1–10)
        "template": "On a left-right scale, the respondent places themselves XXX.",
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
        "template": "The respondent XXX.",
        "valmap": {
            1: "attends religious services more than once a week",
            2: "attends religious services once a week",
            3: "attends religious services once a month",
            4: "attends religious services only on special holy days",
            5: "attends religious services once a year",
            6: "attends religious services less than once a year",
            7: "never attends religious services"
        }
    },
    'Q262': {  # ANES V161267 — age
        "template": "The respondent is XXX years old.",
        "valmap": {}
    },
    'Q260': {  # ANES V161342 — sex
        "template": "The respondent is a XXX.",
        "valmap": {1: "man", 2: "woman"}
    },
    'Q199': {  # ANES V162256 — political interest
        "template": "The respondent is XXX interested in politics.",
        "valmap": {1: "very", 2: "somewhat", 3: "not very", 4: "not at all"}
    }
}