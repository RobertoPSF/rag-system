from langchain_ollama import OllamaEmbeddings

emb = OllamaEmbeddings(
    model="llama3",
    base_url="http://host.docker.internal:11434"
)


def generate_embedding(text: str):
    return emb.embed_query(text)
