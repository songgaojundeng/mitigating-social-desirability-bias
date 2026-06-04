import sys
import pandas as pd
from tqdm import tqdm
import numpy as np

#For priming/preamble, you ideally will use 1st person and original

#Determine year and point of view of respondent's backstory
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

#Which version of the questionnaire to use
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

# Brings in tokenizer/model helpers, including do_query_batch
from batchcommon import *

foi_keys = fields_of_interest.keys()


def compute_demographic_distribution(df: pd.DataFrame):
    """Compute empirical distributions for each field of interest."""
    distributions = {}
    for key in fields_of_interest.keys():
        value_counts = df[key].value_counts(normalize=True).to_dict()
        distributions[key] = value_counts
    return distributions


def generate_fake_respondent(distributions):
    """Sample a fake respondent according to the empirical distributions."""
    fake_respondent = {}
    for k, v in distributions.items():
        fake_respondent[k] = np.random.choice(list(v.keys()), p=list(v.values()))
    return fake_respondent


def gen_backstory_from_fake_person(fake_person):
    """Turn a fake respondent into a natural-language backstory."""
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
        elem_template = fields_of_interest[k]["template"]
        elem_map = fields_of_interest[k]["valmap"]
        if len(elem_map) == 0:
            backstory += " " + elem_template.replace("XXX", str(anes_val))
        elif anes_val in elem_map:
            backstory += " " + elem_template.replace("XXX", elem_map[anes_val])
    if backstory and backstory[0] == " ":
        backstory = backstory[1:]
    return backstory


def generate_query_with_backstory(backstory, question_block):
    """
    In the original code this combines the 'system' string and the
    user prompt (which already contains question + answers).
    """
    return f"{backstory}. {question_block}"


def generate_prompt_for_question(question, answers):
    user_prompt = f"""Question: {question}

Answer choices:
{answers}

When answering, respond ONLY with a single number that corresponds to the option you choose. Do not include any additional text, punctuation or explanation.

My answer is
"""
    return user_prompt

anesdf = pd.read_csv(ANES_FN, sep=SEP, encoding="latin-1", low_memory=False)
distributions = compute_demographic_distribution(anesdf)

# Define the index range of questions this iteration should process
# Example: [0:9]
START_INDEX = 0  # inclusive
END_INDEX = 9    # inclusive

# Batch size for model calls – tune this based on GPU memory
BATCH_SIZE = 4

for q_idx in range(START_INDEX, END_INDEX + 1):
    row = anes_questionnaire.iloc[q_idx]
    full_results = []

    code = row["Code"]
    question = row["Question"]
    answers = row["Answers"]

    # User prompt only depends on the question, not on the respondent
    base_user_prompt = generate_prompt_for_question(question, answers)

    N = len(anesdf)

    # Iterate over respondents in batches
    for start_idx in tqdm(range(0, N, BATCH_SIZE), disable=True):
        end_idx = min(start_idx + BATCH_SIZE, N)

        batch_fake_people = []
        batch_system_prompts = []
        batch_user_prompts = []
        batch_full_prompts = []
        batch_fake_ids = []

        # Build a batch of fake respondents + prompts
        for i in range(start_idx, end_idx):
            fake_person = generate_fake_respondent(distributions)
            backstory = gen_backstory_from_fake_person(fake_person)

            system_prompt = time_date + backstory
            user_prompt = base_user_prompt
            full_prompt = generate_query_with_backstory(system_prompt, user_prompt)
            fake_id = f"fake_{i}"

            batch_fake_people.append(fake_person)
            batch_system_prompts.append(system_prompt)
            batch_user_prompts.append(user_prompt)
            batch_full_prompts.append(full_prompt)
            batch_fake_ids.append(fake_id)

        # One batched model call instead of many single calls
        batch_responses = classify_batch(
            batch_system_prompts,
            batch_user_prompts,
            num_options=5,
        )


        # Collect results for this batch
        for fake_id, fake_person, full_prompt, resp in zip(
            batch_fake_ids, batch_fake_people, batch_full_prompts, batch_responses
        ):
            result_entry = (fake_id, *fake_person.values(), full_prompt, resp)
            full_results.append(result_entry)

    # Save the results for this question
    output_filename = f"full_results_{sys.argv[1]}_{code}.csv"
    columns = ["ID", *fields_of_interest.keys(), "Prompt", "Response"]
    df_results = pd.DataFrame(full_results, columns=columns)
    df_results.to_csv(output_filename, index=False)
