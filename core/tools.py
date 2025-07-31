from dotenv import load_dotenv
import os
import json
from langchain_qdrant import QdrantVectorStore
from langchain.tools import tool
from qdrant_client.http import models
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
import csv
import json
# Load environment variables
load_dotenv()

# Qdrant API Key and collection settings
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
QDRANT_URL = os.getenv('QDRANT_URL')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')


@tool
def search_documents(json_input):
    """
    Busca entre los documentos información turística sobre diferentes ciudades.
    Example of input JSON:
    {
      "query": "Asunto sobre el que buscar información en los documentos",
      "city": "Ciudad sobre la que buscar información" Ej: "Sevilla"
    }
    """
    import json
    import streamlit as st
    from langchain_openai import OpenAIEmbeddings
    from qdrant_client import QdrantClient
    from langchain_qdrant import QdrantVectorStore
    from qdrant_client.http import models

    parsed_json = json.loads(json_input)
    query = parsed_json.get("query", None)
    city = parsed_json.get("city", None)

    # Parámetros desde session_state (con valores por defecto en caso de error)
    top_k = st.session_state.get("top_k", 5)
    threshold = st.session_state.get("similarity_threshold", 0.5)

    # Inicializa embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # Conecta a Qdrant
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

    # Asegura que el índice existe para filtrar por ciudad
    qdrant_client.create_payload_index(
        collection_name="Mi primer RAG",
        field_name="metadata.city",
        field_schema=models.PayloadSchemaType.KEYWORD
    )

    # Inicializa vector store
    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )

    # Filtro por ciudad
    search_filter = models.Filter(
        should=[
            models.FieldCondition(
                key="metadata.city",
                match={"value": city}
            ),
        ]
    )

    # Realiza búsqueda por similitud
    result = vector_store.similarity_search(
        query=query,
        filter=search_filter,
        k=top_k,
        score_threshold=threshold  # este requiere versión moderna de Qdrant
    )

    print(result)
    return result


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

@tool
def generate_csv(json_input: str) -> str:
    """
    Guarda registros en un fichero CSV fijo en 'documentos_generados/output.csv'.
    Ejemplo de input JSON:
    {
        "file_name": "Name of the file without extension"
        "headers": ["col1", "col2", "col3"],
        "rows": [
            ["valor11", "valor12", "valor13"],
            ["valor21", "valor22", "valor23"]
        ]
    }
    """
    # Parsear el JSON de entrada

    params = json.loads(json_input)
    file_name = params.get("file_name")
    headers = params.get("headers")
    rows = params.get("rows")

    # Validaciones básicas
    if not headers or not isinstance(headers, list):
        return json.dumps({"error": "No se proporcionaron 'headers' válidos."}, ensure_ascii=False)
    if not rows or not isinstance(rows, list):
        return json.dumps({"error": "No se proporcionaron 'rows' válidos."}, ensure_ascii=False)

    # Ruta fija para el CSV
    file_path = f"generated_files/{file_name}.csv"

    # Asegurarnos de que la carpeta existe
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Escritura del CSV
    try:
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(rows)
    except Exception as e:
        return json.dumps({"error": f"Falló al escribir el CSV: {e}"}, ensure_ascii=False)

    return json.dumps(
        {"status": "success", "file_path": file_path},
        ensure_ascii=False,
        indent=4
    )


from langchain_community.tools.tavily_search import TavilySearchResults
os.environ["TAVILY_API_KEY"] = "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"

tavily = TavilySearchResults()

@tool
def search_internet(json_input):
  """
  Buscar en internet información detallada
  Example of input JSON:
  {
    "query": "Asunto sobre el que buscar información en internet",
    "max_results": 5
  }
  """
  parsed_json = json.loads(json_input)

  query = parsed_json.get("query", None)
  max_results = parsed_json.get("max_results", None)

  if not query:
    return "No se ha proporcionado ninguna query para hacer la búsqueda."

  if not max_results:
    max_results = 5

  results = tavily.run({
      "query": query,
      "max_results": max_results
  })

  return results
