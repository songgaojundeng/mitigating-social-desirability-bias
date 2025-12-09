import os
import re
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Make sure it doesnt connect to huggingface (online)
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

# Path to the local model
model_id = os.environ.get("LLAMA_MODEL_ID", "/gpfs/work4/0/prjs1623/schapala/llama3.1-70b-hf")

datatype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True, local_files_only=True)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=datatype,
    device_map="auto",
    local_files_only=True,
)

model.eval()


def lc(t):
    return t.lower()


def uc(t):
    return t.upper()


def mc(t):
    tmp = t.lower()
    return tmp[0].upper() + t[1:]


def gen_variants(toks):
    results = []
    variants = [lc, uc, mc]
    for t in toks:
        for v in variants:
            results.append(" " + v(t))
    return results


def extract_probs(lp):
    lp_keys = list(lp.keys())
    ps = [lp[k] for k in lp_keys]
    vals = [(lp_keys[ind], ps[ind]) for ind in range(len(lp_keys))]
    vals = sorted(vals, key=lambda x: x[1], reverse=True)
    result = {}
    for v in vals:
        result[v[0]] = v[1]
    return result


def do_query(system_prompt, user_prompt, max_tokens=4, engine=model):
    """
    Single-query helper: formats as chat, runs generate(), returns raw text.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    # Format messages to Llama format
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    # Tokenize prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(engine.device)
    input_tokens = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    # Keep this so you dont store gradients and computional graphs, save memory
    with torch.no_grad():
        # Get model output
        outputs = engine.generate(
            input_ids=input_tokens,
            attention_mask=attention_mask,
            max_new_tokens=max_tokens,
            do_sample=False,  # Deterministic, no randomness
            pad_token_id=tokenizer.eos_token_id,
        )

    # Get newly generated tokens
    response_tokens = outputs[0][input_tokens.shape[1]:]
    text = tokenizer.decode(response_tokens, skip_special_tokens=True)
    text = text.strip()
    return text


#Modified LLM function to retrieve highest probability token
def classify_batch(system_prompts, user_prompts, num_options: int = 5, engine=None):
    """
    Deterministic classification over answer options using raw logits.

    - Always returns one of: "1", "2", ..., f"{num_options}".
    - Does NOT generate text, just looks at next-token logits.
    - Assumes the valid options are 1..num_options (max 5 in your case).
    """

    if engine is None:
        engine = model

    assert len(system_prompts) == len(user_prompts)
    batch_size = len(system_prompts)
    if batch_size == 0:
        return []

    # Safety: cap num_options at 5 because of your experiment design
    assert 1 <= num_options <= 5, "num_options must be between 1 and 5"

    # Ensure padding token exists
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        if hasattr(engine, "config"):
            engine.config.pad_token_id = tokenizer.pad_token_id

    # Build chat prompts
    prompts = [
        tokenizer.apply_chat_template(
            [
                {"role": "system", "content": sp},
                {"role": "user", "content": up},
            ],
            tokenize=False,
            add_generation_prompt=True,
        )
        for sp, up in zip(system_prompts, user_prompts)
    ]

    # Tokenize & pad
    inputs = tokenizer(
        prompts,
        return_tensors="pt",
        padding=True,
    ).to(engine.device)

    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    # Forward pass (no generate)
    with torch.inference_mode():
        outputs = engine(
            input_ids=input_ids,
            attention_mask=attention_mask,
        )
        logits = outputs.logits  # [B, T, vocab]

    # Index of last real token in each prompt
    last_token_indices = attention_mask.sum(dim=1) - 1  # [B]

    # Token IDs for " 1", " 2", ..., up to num_options
        # Token IDs for "1", "2", ..., up to num_options
    option_tokens = []
    option_labels = []
    for i in range(1, num_options + 1):
        s = str(i)  # no leading space
        ids = tokenizer.encode(s, add_special_tokens=False)
        if len(ids) != 1:
            raise ValueError(f"Option '{s}' tokenized into multiple tokens: {ids}")
        option_tokens.append(ids[0])
        option_labels.append(str(i))


    responses = []

    for b in range(batch_size):
        idx = last_token_indices[b].item()
        next_logits = logits[b, idx]  # [vocab]

        # Collect logits for each option token
        option_scores = [next_logits[tok_id].item() for tok_id in option_tokens]

        # Argmax over options
        best_idx = max(range(len(option_scores)), key=lambda i: option_scores[i])

        responses.append(option_labels[best_idx])

    return responses


