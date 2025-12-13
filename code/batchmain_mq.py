import sys
import pandas as pd
from tqdm import tqdm
import numpy as np

# Brings in tokenizer/model helpers, including do_query_batch
from batchcommon import *

# ANES-specific imports (2020 case for now)
if sys.argv[1] == "2020":
    from anes2020_thirdperson import *

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
    backstory = ""
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


# ---------------------------------------------------------------------
# Load data and precompute distributions
# ---------------------------------------------------------------------
anesdf = pd.read_csv(ANES_FN, sep=SEP, encoding="latin-1", low_memory=False)
anes_2020_questionnaire = pd.read_excel(
    "./ANES_2020_multiple_questions_selected_reformulated.xlsx"
)
distributions = compute_demographic_distribution(anesdf)

time_date = "Today is November 3, 2020. "

# Define the index range of questions this iteration should process
# Example: [0:9]
START_INDEX = 0  # inclusive
END_INDEX = 9    # inclusive

# Batch size for model calls – tune this based on GPU memory
BATCH_SIZE = 4

# ---------------------------------------------------------------------
# Main loop over questions
# ---------------------------------------------------------------------
for q_idx in range(START_INDEX, END_INDEX + 1):
    row = anes_2020_questionnaire.iloc[q_idx]
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
        # do_query_batch now decodes like do_query and returns digits (or "")

        batch_responses = do_query_batch_old_debug(
            batch_system_prompts,
            batch_user_prompts,
            fake_ids=batch_fake_ids,
            max_tokens=10,
            print_full_prompt=True,  # set False if output is too spammy
        )

        # Collect results for this batch
        for fake_id, fake_person, full_prompt, resp in zip(
            batch_fake_ids, batch_fake_people, batch_full_prompts, batch_responses
        ):
            result_entry = (fake_id, *fake_person.values(), full_prompt, resp)
            full_results.append(result_entry)

    # Save the results for this question
    output_filename = f"full_results_2020_{code}.csv"
    columns = ["ID", *fields_of_interest.keys(), "Prompt", "Response"]
    df_results = pd.DataFrame(full_results, columns=columns)
    df_results.to_csv(output_filename, index=False)
