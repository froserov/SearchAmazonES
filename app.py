from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from urllib.parse import quote
import numpy as np

app = Flask(__name__)

# Conexión a Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "amazon_products"

## Busqueda de productos con template

@app.route("/search", methods=["GET"])
def search():
    search_box = request.args.get('search_box', '')
    main_category = request.args.get('main_category', '')

    # Solicitar búsqueda con template
    response = es.search_template(
        index=index_name,
        body={
            "id": "amazon_search_template",
            "params": {
                "search_box": search_box,
                "main_category": main_category
            }
        }
    )

    results = [
        {
            "name": hit["_source"]["name"],
            "ratings": hit["_source"].get("ratings", "N/A"),
            "no_of_ratings": hit["_source"].get("no_of_ratings", "N/A"),
            "discount_price_dolares": hit["_source"].get("discount_price_dolares", "N/A"),
            "actual_price_dolares": hit["_source"].get("actual_price_dolares", "N/A")
        }
        for hit in response["hits"]["hits"]
    ]

    return jsonify(results)

## Productos similares con embeddings

@app.route("/similar_products", methods=["GET"])
def similar_products():
    product_name = request.args.get('name')
    
    # Buscar el producto en Elasticsearch para obtener su embedding
    response = es.search(
        index=index_name,
        body={
            "query": {
                "match": {
                    "name": product_name
                }
            }
        }
    )
    
    if not response["hits"]["hits"]:
        return jsonify({"error": "Producto no encontrado"}), 404

    # Obtener el embedding del producto encontrado
    product_embedding = response["hits"]["hits"][0]["_source"]["embedding"]

    # Consultar Elasticsearch con la búsqueda por similitud de embeddings
    query_body = {
        "size": 5,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": product_embedding}
                }
            }
        }
    }

    similar_response = es.search(index=index_name, body=query_body)
    
    similar_products = [
        {
            "name": hit["_source"]["name"],
            "similarity_score": hit["_score"],
            "ratings": hit["_source"].get("ratings", "N/A"),
            "no_of_ratings": hit["_source"].get("no_of_ratings", "N/A"),
            "discount_price_dolares": hit["_source"].get("discount_price_dolares", "N/A"),
            "actual_price_dolares": hit["_source"].get("actual_price_dolares", "N/A")
        }
        for hit in similar_response["hits"]["hits"]
    ]

    return jsonify(similar_products)


if __name__ == "__main__":
    app.run(debug=True)

