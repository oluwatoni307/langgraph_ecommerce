
import os

api_key = os.getenv('api_key')

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", api_key=api_key, temperature=0.5)


from pydantic import BaseModel, Field


class Product_augData(BaseModel):
    product_type: str = Field(description="type of product")
    category: list = Field(description="category")
    recommendation_tags: list = Field(
        description="tags to query for recommendation querying"
    )


structured_llm = llm.with_structured_output(Product_augData)


answer = structured_llm.invoke("tell me about any product")
print(type(answer.recommendation_tags))


label_prompt_template = """
AI product analyst for e-commerce categorization & recommendations

INPUT: List of product data dicts

TASK: Generate for each product:
1. Product Type: General, comparable (e.g. "office_chair")
2. Product Category: Primary & secondary (if applicable)
3. Recommendation Tags: 5-10 covering features, audience, usage, style, characteristics

OUTPUT FORMAT:
{
  "product_type": "string_with_underscores",
  "product_category": {
    "primary": "string_with_underscores",
    "secondary": "string_with_underscores" // if applicable
  },
  "recommendation_tags": ["tag1", "tag2", "tag3_with_underscores", ...]
}

INSTRUCTIONS:
- Use underscores, not spaces (except brand names in tags)
- Keep product_type general; use specifics in tags
- Base on provided data only
- Use "unknown" if info missing, "n/a" if not applicable
- Consistent naming, industry-standard terms when possible
- Create & explain new categories for unique products
- Prioritize tags by relevance
- Preserve brand name capitalization in tags

EXAMPLE INPUT:
{
  "name": "Ergonomic Mesh Office Chair",
  "description": "High-back design with lumbar support, adjustable armrests, and breathable mesh material. Suitable for long hours of computer work.",
  "price": 199.99,
  "brand": "ComfortPlus"
}

EXAMPLE OUTPUT:
{
  "product_type": "office_chair",
  "product_category": {
    "primary": "office_furniture",
    "secondary": "ergonomic_workstation_equipment"
  },
  "recommendation_tags": [
    "ergonomic",
    "mesh",
    "high_back",
    "lumbar_support",
    "adjustable_armrests",
    "computer_work",
    "long_sitting_hours",
    "breathable",
    "professional",
    "ComfortPlus_brand"
  ]
}

"""

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

label_prompt = PromptTemplate(
    template=label_prompt_template,
    input_variables=['input']
)

label_chain = label_prompt|structured_llm



