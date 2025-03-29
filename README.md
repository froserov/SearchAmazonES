---
noteId: "6cbfa0500bd611f0994f85234ebad6ce"
tags: []

---

## **Search & Recommendation System with Elasticsearch and Embeddings**

🔍 **Descripción**
Este proyecto implementa un sistema de búsqueda y recomendación utilizando Elasticsearch y embeddings generados 
con modelos preentrenados de Sentence Transformers. 
Este caso de estudio busca demostrar habilidades en la creación de índices, consultas avanzadas, implementación de plantillas Mustache 
y desarrollo de APIs usando Flask.

### 📁 **Estructura del Proyecto**

├── data/

│   ├── raw/

**Se debe usar para depositar la base de datos Amazon-Products.csv**

│   ├── processed/

**Para almacenar archivos procesados (embeddings, DataFrames limpios, etc).**

├── notebooks/

│   ├── 1)ingestion_and_indexing.ipynb

**Carga de datos, preprocesamiento, creación de índice "amazon_products" e ingesta.**

│   ├── 2)api_development.ipynb            

**Desarrollo mustache template y de la API Flask con búsquedas avanzadas.**

│   ├── 3)embedding_processing.ipynb        

**Generación de embeddings y almacenamiento en Elasticsearch**.

├── app.py                      

**Código principal de la API Flask.**

├── requirements.txt            

**Librerías requeridas para la ejecución del proyecto.**

├── README.md    

**Archivo README del proyecto.**

├── DETALLE_PREGUNTAS.md        

**Resume como se respondió a cada pregunta del caso**

├── .gitignore                  

**Archivos y carpetas a excluir del repositorio.**



### 📌 **Tecnologías Usadas**

**Python:** Lenguaje principal del proyecto.

**Elasticsearch:** Motor de búsqueda para indexar y consultar datos.

**Flask:** Framework para construir la API.

**Sentence Transformers:** Modelo preentrenado para generar embeddings de texto.

**Pandas & NumPy:** Manipulación y procesamiento de datos.

**Docker (próximamente)**: Despliegue y aseguramiento de compatibilidad del proyecto.


### 📌 **Instalación y Configuración**

**Clonar el repositorio:**
- git clone https://github.com/tu_usuario/SearchAmazonES.git

**Crear un ambiente virtual (opcional pero recomendado):**
- python -m venv venv
- source venv/bin/activate  # En Linux/Mac
- .\venv\Scripts\activate   # En Windows

**Instalar dependencias:**
- pip install -r requirements.txt

**Iniciar Elasticsearch (si no está corriendo aún)**. 
- docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.17.10


### 📌 **Uso sugerido**

**1)Abrir y leer md Detalle Preguntas**

**2)Descargar base Amazon-Products y ubicarla en carpeta raw, descargar (preferiblemente) base con embeddings para no tener que generarlos**

Opcion 1: Repo Kaggle:https://www.kaggle.com/datasets/lokeshparab/amazon-products-dataset?select=All+Electronics.csv

Opción 2: Drive 

**3) Revisar/Ejecutar Preprocesamiento e Ingesta (Notebook 1)**
- Carga y procesa df.
- Transforma precios de Rupias a Dólares y los convierte a formato numérico.
- Remueve duplicados según criterios específicos.
- Indexa los datos en Elasticsearch con un mapping definido.

**4)Revisar/Ejecutar Mustache Template & Search (Notebook 2)**
- Construcción de la plantilla mustache:
- Crea la funcion **/search:** usando la plantilla que permite realizar búsquedas en Elasticsearch utilizando filtros por categorías y palabras clave.

**5)Revisar/Ejecutar Generación de Embeddings (Notebook 3)**
- Generar embeddings a partir del nombre del producto.
- Almacena los embeddings en el índice de Elasticsearch para futuras búsquedas semánticas.
- Crea y prueba función **similar_products**

**6)Ejecutar app.py**
Utiliza las funciones **/search:**  y **similar_products** desarollados en los nbs 2 y 3 respectivamente.
Se puede ejecutar en bash con python app.py



