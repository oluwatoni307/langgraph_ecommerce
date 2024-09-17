import requests
from langchain_chroma import Chroma
import xml.etree.ElementTree as ET
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
from langchain_core.documents import Document
from config import label_chain, label_prompt_template
import json


import re



import os

api_key = os.getenv('api_key')



# File to store the integer
file_name = "product6.jsonl"


# Function to create or initialize the integer in the file
def create_integer(value=0):
    with open(file_name, "w") as file:
        file.write(str(value))


# Function to retrieve the integer from the file
def retrieve_integer():
    try:
        with open(file_name, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return None  # Return None if file doesn't exist
    except ValueError:
        return None  # Return None if file content is invalid


# Function to update the integer in the file
def update(new_value):
    with open(file_name, "a") as file:
        file.write(new_value + "\n")


amount = retrieve_integer()


import os

# api_key = os.getenv('api_key')


embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)

vector_store = Chroma(
    collection_name="Product",
    embedding_function=embeddings,
    persist_directory="./",  # Where to save data locally, remove if not neccesary
)

# # toni = [{"name":"toni","age":20, "sex":"male"}, {"name":"toyosi","age":21, "sex":"female"}, {"name":"toki","age":26, "sex":"male"}]

# # docs = []
# # for i in toni:
# #     doc = Document(
# #         page_content=str(i),
# #         metadata = {'source':'xml'}
# #     )
# #     docs.append(doc)
# # uuid = [str(uuid4() for i in range(len(docs)))]

# # vector_store.add_documents(documents=docs)
# # results = vector_store.similarity_search("how old ", k=2)


# # print(results)


# # Fetch the XML feed
# url = "https://feeds.mergado.com/doplnkyprokaravany-cz-google-nakupy-3263f92298aa865c4b1bedea88352427.xml"
# response = requests.get(url)
# xml_content = response.content

# # Parse the XML content
# root = ET.fromstring(xml_content)

# # Find the channel element
# channel = root.find("channel")
# channel_data = []

# # Print the structure of the first 10 items within the channel
# if channel is not None:
#     items = channel.findall("item")
#     for i, item in enumerate(items[5461:]):  # Limit to first 10 items
#         lis = []
#         product = ''
#         for child in item:
            
#             cleaned_text = re.sub(r"{http://base\.google\.com/ns/1\.0}", "", child.tag)
#             if (
#                 cleaned_text == "product_type"
#                 or cleaned_text == "google_product_category"
#             ):
#                 continue
#             if cleaned_text == "price":
#                 number = re.findall(r"\d+", child.text)[
#                     0
#                 ]  # Find the first sequence of digits
#                 # Convert the extracted number to an integer
#                 number_as_int = int(number)
#                 product += f"{cleaned_text} = {number_as_int},"
#                 continue
            
#             product += f"{cleaned_text} = {child.text},"
            
            
            



#         channel_data.append(product
#                             )

#     print(channel_data)
#     new_amount = len(channel_data)
#     # update_integer(new_amount)

# else:
#     print("No channel found in the RSS feed")





# if channel_data:
#     docs = []
#     for i in channel_data:
#         doc = Document(
#             page_content=str(i),
#             metadata = {'source':'xml'}
#         )
#         docs.append(doc)
#     vector_store.add_documents(documents=docs)
results = vector_store.similarity_search("awning", filter={"source": "xml"})
print(results)


# for item in channel_data:
#     input = str(item)
#     answer = label_chain.invoke({'input':input})
#     # product_type =
