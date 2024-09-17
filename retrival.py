from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma


import os

api_key = os.getenv('api_key')
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)

# Setup Chroma vector store for storing product embeddings
vector_store = Chroma(
    collection_name="Product",
    embedding_function=embeddings,
    persist_directory="./",  # Optional: Remove if persistence is not needed
)

  
def get_relevant_documents( query: str, filters: dict = None, use_and: bool = True, k: int = 5):
        # Create the search_kwargs dictionary
        search_kwargs = {
            "k": k,  # You can adjust this value as needed
        }

        # Check if filters are provided
        if filters:
            search_kwargs["filter"] = _build_filter(filters, use_and)

        # Create the retriever
        retriever = vector_store.as_retriever(search_kwargs=search_kwargs)
        
        # Retrieve and return relevant documents
        return retriever.invoke(query)

def _build_filter(self, filters: dict, use_and: bool):
        filter_list = []
        for key, value in filters.items():
            filter_list.append({key: {"$eq": value}})

        if use_and:
            return {"$and": filter_list}
        else:
            return {"$or": filter_list}
        
answer = get_relevant_documents('')
print(answer)