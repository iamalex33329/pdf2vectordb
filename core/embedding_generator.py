from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def generate_embeddings(texts):
    embeddings = []
    for text in texts:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        embeddings.append(response.data[0].embedding)
    return embeddings
