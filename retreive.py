from typing import Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from retrival import get_relevant_documents
from db_helper import ProductDatabase
from pydantic import BaseModel, Field
from langchain_core.tools import tool


import os

api_key = os.getenv('api_key')

# Initialize Chat Model and Embeddings
model = ChatOpenAI(model='gpt-4o-mini', temperature=0, api_key=api_key)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)


# Custom retriever using the vector store

# Database helper object for SQL queries
db = ProductDatabase()

# Pydantic model for input validation (if needed for structured inputs)
class Retrieval_input(BaseModel):
    filter: Optional[dict] = Field(description='Meta tags to filter vector results')
    k: Optional[int] = Field(description='Number of products to retrieve')
    use_and: Optional[bool] = Field(description='Use AND/OR in filtering meta tags')
    query: Optional[str] = Field(description='the query for the database')

# Retrieval Tool
@tool(args_schema=Retrieval_input)
def retrieve( k: int =5, use_and: bool =True, query: str = '', filter: dict = None):
    """
    Retrieve relevant documents based on query, filter, and combination logic.

    Args:
        filter (dict): A dictionary of meta tags used to filter the vector results.
        k (int): The number of documents to retrieve.
        use_and (bool): Boolean flag to determine how the filter conditions are applied:
            - If True, documents must match **all** conditions (AND logic).
            - If False, documents can match **any** condition (OR logic).
        query (str, optional): A query string to search within the filtered documents. Defaults to an empty string.

    Returns:
        list: A list of relevant documents retrieved based on the query and filter criteria.
    """
    docs = get_relevant_documents(query, filter, use_and, k)
    return docs

class SqlQuery(BaseModel):
    query: str = Field(description="SQL query string")
    params: Optional[dict] = Field(description="Optional query parameters")

# SQL Query Tool
@tool(args_schema=SqlQuery)
def sql_retrieve(query: str, params: dict):
    """
    Execute a custom SQL query with optional parameters.

    Args:
        query (str): The SQL query string to execute.
        params (dict): A dictionary of parameters to pass to the SQL query.

    Returns:
        list: A list of rows returned from the query.
    """
    response = db.execute_custom_query(query, params)
    return response




tools = [retrieve]


from langgraph.prebuilt import create_react_agent
# We can add "chat memory" to the graph with LangGraph's checkpointer
# to retain the chat context between interactions


prompt ="""

AI Assistant for Doplňky pro karavany (Czech Caravan Accessories E-commerce)

Role: Friendly caravan expert providing product info and advice.
Tone: Informal, conversational, enthusiastic.

Tool: Vector database of product details
- Parameters: query (string), k (integer, number of vectors to retrieve)

Query Process:
1. Translate non-Czech queries; always respond in user's language.
2. Formulate effective query:
   - Identify product category/categories
   - Add relevant terms to enhance search
3. Determine appropriate k value:
   - Standard queries: k=3
   - Comparisons: k=5 per product
   - Category-wide or price-based queries: k=6-10
4. Retrieve k most relevant product vectors
5. Present product info (omit if unavailable):
    Image: <img src="[image_link]" alt="[title]">
    Product Link: Odkaz na produkt: <a href="[link]">[title]</a>
    Price: Cena: [price] Kč
    Availability: Dostupnost: [availability]
    MPN: MPN: [mpn]


Handle Query Types:
- Product inquiries: Detail based on retrieved data
- Comparisons: Focus on key differences
- Recommendations: Suggest based on query and retrieved products
- Price queries (cheapest/most expensive): Use larger k, compare retrieved products

Key Principles:
- Ensure accuracy based solely on retrieved vectors
- Omit unavailable info; never provide false data
- Ask for clarification if query is ambiguous
- For complex queries, break down reasoning steps
- Adopt "Karel" persona; use general anecdotes without specific claims

Continuously analyze and improve responses
"""


graph = create_react_agent(model, tools= tools, state_modifier=prompt)























































































def retriever(input, past_question):
    prompt= {
        "Conversation": past_question,
        "User_question": input
        
    }
    print('hello')
    
    inputs = {"messages": [("user", str(prompt))]}
    answer = graph.invoke(inputs) 
    message = answer["messages"][-1].content
    return message
 
 
 
# conv = {'user':'hi'}
# quest= 'hi'
# answer = retriever(quest, conv)
# print (answer)