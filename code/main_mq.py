import sys
import pandas as pd
from tqdm import tqdm
import numpy as np
import os

#For reformulated prompts, ideally use 3rd person
#For priming/preamble, you ideally will use 1st person and original

if sys.argv[1] == "2012":
    if sys.argv[2] == "first":
        from anes2012 import *
elif sys.argv[1] == "2016":
    if sys.argv[2] == "first":
        from anes2016 import *
elif sys.argv[1] == "2020":
    time_date = "Today is November 3, 2020. "
    base_path = "./ANES_2020_multiple_questions_selected"
    if sys.argv[2] == "first":
        from anes2020 import *
    elif sys.argv[2] == "third":
        from anes2020_thirdperson import *
elif sys.argv[1] == "2024":
    time_date = "Today is November 5, 2024. "
    base_path = "./ANES_2024_multiple_questions_selected"
    if sys.argv[2] == "first":
        from anes2024 import *
    elif sys.argv[2] == "third":
        from anes2024_thirdperson import *
else:
    raise SystemExit

suffix = {
    "original": "",
    "reformulated": "_reformulated",
    "reverse": "_reverse_v2",
}

if sys.argv[3] not in suffix:
    raise SystemExit

anes_questionnaire = pd.read_excel(
    f"{base_path}{suffix[sys.argv[3]]}.xlsx"
)

from common import *
# from common_llama8b import * #llama8b
# from common_llama3170b import * #llama70b

foi_keys = fields_of_interest.keys()

def compute_demographic_distribution(df):
    distributions = {}
    for key in fields_of_interest.keys():
        value_counts = df[key].value_counts(normalize=True).to_dict()
        distributions[key] = value_counts
    return distributions

def generate_fake_respondent(distributions):
    fake_respondent = {}
    for k, v in distributions.items():
        fake_respondent[k] = np.random.choice(list(v.keys()), p=list(v.values()))
    return fake_respondent
    
def gen_backstory_from_fake_person(fake_person):
    #1st = preamble, 2nd = priming, 3rd = no priming/preamble
    if sys.argv[4] == "preamble":
        backstory = "In this study, we are exploring how people naturally respond to various questions. To ensure meaningful results, it is important that responses reflect your genuine thoughts and feelings. There are no correct or desirable answers, and your responses will not be evaluated or judged. Please answer honestly and without concern for how your answers might be perceived. Your sincerity helps us better understand authentic human responses."
    elif sys.argv[4] == "priming":
        backstory = "You value logic, objectivity, and internal consistency. When responding, you prioritize reasoning over emotion, and aim to base your answers on evidence, structure, and rational analysis. Your goal is to provide clear, well-reasoned, and intellectually honest answers that reflect careful thought. The best answer is that which reflects your reasoning process."
    elif sys.argv[4] == "none":
        backstory = ""
    else:
        raise SystemExit
    for k, anes_val in fake_person.items():
        if anes_val < 0:  
            continue
        elem_template = fields_of_interest[k]['template']
        elem_map = fields_of_interest[k]['valmap']
        if len(elem_map) == 0:
            backstory += " " + elem_template.replace('XXX', str(anes_val))
        elif anes_val in elem_map:
            backstory += " " + elem_template.replace('XXX', elem_map[anes_val])
    if backstory[0] == ' ':
        backstory = backstory[1:]
    return backstory

def generate_query_with_backstory(backstory, question):
    return f"{backstory}. {question}"

def generate_prompt_for_question(question, answers):
    user_prompt = \
f"""Question: {question}

Answer choices:
{answers}

When answering, respond ONLY with a single number that corresponds to the option you choose. Do not include any additional text, punctuation or explanation.

My answer is
"""
    return user_prompt

anesdf = pd.read_csv(ANES_FN, sep=SEP, encoding='latin-1', low_memory=False)
distributions = compute_demographic_distribution(anesdf)
fake_results = []


# Define the index range of questions this iteration should process
# [0:9]
START_INDEX = 0  # The starting index for this iteration (inclusive)
END_INDEX = 9    # The ending index for this iteration (inclusive)


for idx in range(START_INDEX, END_INDEX + 1):
    row = anes_questionnaire.iloc[idx]
    full_results = []

    code = row["Code"]
    question = row["Question"]
    answers = row["Answers"]
    user_prompt = generate_prompt_for_question(question, answers)
    MAX_RETRIES = 5
    for idx in tqdm(range(len(anesdf)), disable=True):
        fake_person = generate_fake_respondent(distributions)
        backstory = gen_backstory_from_fake_person(fake_person)
        # backstory = '' # set empty when testing no demo profile
        user_prompt = generate_prompt_for_question(question, answers)
        system_prompt = time_date + backstory

        full_prompt = generate_query_with_backstory(system_prompt, user_prompt)
        
        fake_id = f"fake_{idx}"  

        retries = 0
        success = False
        while not success and retries < MAX_RETRIES:
            try:
                response = do_query(system_prompt, user_prompt)
                result_entry = (fake_id, *fake_person.values(), full_prompt, response)
                full_results.append(result_entry)
                success = True 
            except Exception as e:
                print("The server could not be reached")
                print(e)  # an underlying Exception, likely raised within httpx.
            retries += 1  
            

        if not success:
            print(f"Failed to get a response after {MAX_RETRIES} retries for respondent {fake_id}.")
        
        
    # Save the results
    output_dir = os.path.join('ANES20-gpt4.1mini',sys.argv[3], sys.argv[4])
    ## change folder name "ANES20-gpt4.1mini" accordingly when run ANES 2024 or llama8b or 70b
    os.makedirs(output_dir, exist_ok=True)

    output_filename = f"full_results_{sys.argv[1]}_{code}.csv"
    output_path = os.path.join(output_dir, output_filename)

    columns = ["ID", *fields_of_interest.keys(), "Prompt", "Response"]
    df_results = pd.DataFrame(full_results, columns=columns)
    df_results.to_csv(output_path, index=False)
