from dotenv import load_dotenv
import os
import json
from langchain_qdrant import QdrantVectorStore
from langchain.tools import tool
from qdrant_client.http import models
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
# Load environment variables
load_dotenv()

# Qdrant API Key and collection settings
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
QDRANT_URL = os.getenv('QDRANT_URL')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
@tool
def search_vdb(json_input) -> str:
    """
    Retrieves very useful information about different cities in Andalucia

    Example of input JSON:
    {
        "query": "topic you want to get information about",
        "city": "city you want to get information about"
    }

    Example of output:
    {
    }
    """
    parsed_json = json.loads(json_input)

    topic = parsed_json.get("query", None)
    city=parsed_json.get("city", None)



    qdrant_client = QdrantClient(
      url = os.environ["QDRANT_URL"],
      api_key = os.environ["QDRANT_API_KEY"]
    )


    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name= "mi_primer_rag",
    embedding=embeddings,
    )



    # Perform similarity search on the precision collection
    parsed_json = json.loads(json_input)

    location = parsed_json.get("query", None)

    results = vector_store.similarity_search(
    query=topic,
    k =3,  # Número de resultados a devolver
    )
    retrieved_docs = []
    for document in results:
        # print(document)
        retrieved_docs.append(document.page_content)
    return json.dumps(retrieved_docs)

@tool
def search_JSON(json_input) -> str:
    """
    Return all the festive days in a city.
    Example of input JSON:
    {
        "city": "city you want to get festive days about"
    }
    """
    # Parse input JSON
    parsed_json = json.loads(json_input)
    city = parsed_json.get("city", None)

    if not city:
        return json.dumps({"error": "City not provided."}, ensure_ascii=False)

    # Path to the JSON file containing festive days
    json_location = "files/festivos_andalucia.json"

    with open(json_location, "r", encoding="utf-8") as file:
        festive_data = json.load(file)

    # Fetch festive days for the given city
    festive_days = festive_data.get(city, None)

    if festive_days:
        return json.dumps({"city": city, "festive_days": festive_days}, ensure_ascii=False, indent=4)
    else:
        return json.dumps({"error": f"No data found for city: {city}"}, ensure_ascii=False)

