"""Run Q6 homework (query_points). Use if Jupyter cell still shows client.search."""
import requests
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from fastembed import TextEmbedding

docs_url = "https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json"
documents_raw = requests.get(docs_url).json()
documents = []
for course in documents_raw:
    if course["course"] != "machine-learning-zoomcamp":
        continue
    for doc in course["documents"]:
        doc["course"] = course["course"]
        documents.append(doc)

embedding_model = TextEmbedding(model_name="BAAI/bge-small-en")
client = QdrantClient(":memory:")
collection_name = "ml_zoomcamp_faq"
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

points = []
for idx, doc in enumerate(documents):
    full_text = doc["question"] + " " + doc["text"]
    vector = list(embedding_model.embed([full_text]))[0]
    points.append(PointStruct(id=idx, vector=vector, payload=doc))

client.upsert(collection_name=collection_name, points=points)

query = "I just discovered the course. Can I still join it?"
query_vector = list(embedding_model.embed([query]))[0]

search_response = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=1,
)
highest_score = search_response.points[0].score
print(f"Highest similarity score for the first record: {highest_score}")
