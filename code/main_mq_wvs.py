import sys
import pandas as pd
from tqdm import tqdm
import numpy as np


#For reformulated prompts, you ideally will use 3rd person

if sys.argv[1] == "first":
    from wvs7 import *
elif sys.argv[1] == "third":
    from wvs7_thirdperson import *
else:
    raise SystemExit()

from common import *

time_date = "The year is 2022. "
base_path = "./WVS_Wave7_multiple_questions_selected"
suffix = {
    "original": "",
    "reformulated": "_reformulated",
}
    
if sys.argv[2] not in suffix:
    raise SystemExit()

wvs_questionnaire = pd.read_excel(
    f"{base_path}{suffix[sys.argv[2]]}.xlsx"
)

foi_keys = fields_of_interest.keys()


def compute_demographic_distribution(df):
    distributions = {}
    for key in fields_of_interest.keys():
        s = df[key]
        distributions[key] = s.value_counts(normalize=True).to_dict()
    return distributions


def generate_fake_respondent(distributions):
    fake_respondent = {}
    for k, v in distributions.items():
        fake_respondent[k] = np.random.choice(list(v.keys()), p=list(v.values()))
    return fake_respondent


def gen_backstory_from_fake_person(fake_person):
    if sys.argv[3] == "preamble":
        backstory = "In this study, we are exploring how people naturally respond to various questions. To ensure meaningful results, it is important that responses reflect your genuine thoughts and feelings. There are no correct or desirable answers, and your responses will not be evaluated or judged. Please answer honestly and without concern for how your answers might be perceived. Your sincerity helps us better understand authentic human responses."
    elif sys.argv[3] == "priming":
        backstory = "You value logic, objectivity, and internal consistency. When responding, you prioritize reasoning over emotion, and aim to base your answers on evidence, structure, and rational analysis. Your goal is to provide clear, well-reasoned, and intellectually honest answers that reflect careful thought. The best answer is that which reflects your reasoning process."
    elif sys.argv[3] == "none":
        backstory = ""
    else:
        raise SystemExit()

    for k, wvs_val in fake_person.items():
        if wvs_val < 0:
            continue

        elem_template = fields_of_interest[k]["template"]
        elem_map = fields_of_interest[k]["valmap"]

        if len(elem_map) == 0:
            backstory += " " + elem_template.replace("XXX", str(wvs_val))
        elif wvs_val in elem_map:
            backstory += " " + elem_template.replace("XXX", elem_map[wvs_val])

    if backstory and backstory[0] == " ":
        backstory = backstory[1:]

    return backstory


def generate_query_with_backstory(backstory, question):
    return f"{backstory}. {question}"


def generate_prompt_for_question(question, answers):
    return f"""Question: {question}

Answer choices:
{answers}

When answering, respond ONLY with a single number that corresponds to the option you choose. Do not include any additional text, punctuation or explanation.

My answer is
"""


wvsdf = pd.read_csv(WVS_FN, sep=",", encoding="latin-1", low_memory=False)
distributions = compute_demographic_distribution(wvsdf)

START_INDEX = 0
END_INDEX = len(wvs_questionnaire) - 1
MAX_RETRIES = 5


for q_idx in range(START_INDEX, END_INDEX + 1):
    row = wvs_questionnaire.iloc[q_idx]
    full_results = []

    code = row["Code"]
    question = row["Question"]
    answers = row["Answers"]

    user_prompt = generate_prompt_for_question(question, answers)

    for i in tqdm(range(len(wvsdf)), disable=True):
        fake_person = generate_fake_respondent(distributions)
        backstory = gen_backstory_from_fake_person(fake_person)

        system_prompt = time_date + backstory
        full_prompt = generate_query_with_backstory(system_prompt, user_prompt)

        fake_id = f"fake_{i}"

        retries = 0
        success = False

        while not success and retries < MAX_RETRIES:
            try:
                response = do_query(system_prompt, user_prompt)

                result_entry = (
                    fake_id,
                    *fake_person.values(),
                    full_prompt,
                    response,
                )
                full_results.append(result_entry)
                success = True

            except Exception as e:
                print("The server could not be reached")
                print(e)

            retries += 1

        if not success:
            print(f"Failed to get a response after {MAX_RETRIES} retries for respondent {fake_id}.")

    output_filename = f"full_results_wvs7_{sys.argv[2]}_{code}.csv"
    columns = ["ID", *fields_of_interest.keys(), "Prompt", "Response"]

    df_results = pd.DataFrame(full_results, columns=columns)
    df_results.to_csv(output_filename, index=False)