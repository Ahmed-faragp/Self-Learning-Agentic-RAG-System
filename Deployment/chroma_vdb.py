import os
from langchain_core.documents import Document
import chromadb
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings
from datasets import load_dataset
import pandas as pd

embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    collection_name="my_collection",
    embedding_function=embedding_function,
    persist_directory="./chroma_db"
)





dataset = load_dataset("openai/openai_humaneval")
df = pd.DataFrame(dataset['test'])
documents = []
for index, row in df.iterrows():
    prompt = row['prompt']
    code = row['canonical_solution']
    text = prompt + "\n   CODE:\n" + code
    documents.append(
        Document(
            page_content=text,
            metadata={"id": str(index)}
        )
    )

if len(vectorstore.get()["ids"]) == 0:
    vectorstore.add_documents(documents)
    # vectorstore.persist()


def add_document_to_chroma(function_name, code, explanation):
    document = f"Function Name: {function_name}\nCode:\n{code}\nExplanation:\n{explanation}"
    doc = Document(
        page_content=document,
        metadata={"id": function_name}
    )
    vectorstore.add_documents([doc])
    vectorstore.persist()
def retrieve_with_confidence(query):
    results = vectorstore.similarity_search_with_score(query, k=3)
    best_doc, best_score = results[0]
    
    return best_doc.page_content, best_score
data = vectorstore.get()
print(len(data["ids"]))
query = """
 Input to this function is a string representing musical notes in a special ASCII format.
Your task is to parse this string and return list of integers corresponding to how many beats does each
not last."""

results, score = retrieve_with_confidence(query)

print("Retrieved documents:")
print(results)
print("Similarity score:", score)