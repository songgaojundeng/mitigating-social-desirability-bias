from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    timeout=20.0,

)

models = client.models.list()

for m in models.data:
    print(m.id)