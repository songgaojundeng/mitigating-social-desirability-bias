from openai import OpenAI
import numpy as np
from dotenv import load_dotenv

model = "gpt-5-mini"

load_dotenv()
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    timeout=20.0,
)

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

def do_query(system_prompt, user_prompt, engine=model):
    response = client.responses.create(
        model=engine,
        reasoning={"effort": "medium"},
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.output_text

