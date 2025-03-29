---
noteId: "8e7bbe200bf611f08d4343051b4a46a4"
tags: []

---
## **Detalle de solucion de caso**

**3.1 Crear el Índice en ElasticSearch**

- El nb 1 contiene el proceso de conexión a E.S y el mapping del indice "amazon products". En este indice se incluye la propiedad standard_analyzer para el nombre de los productos, ademas se inclye a las categorias y subcategorias como keywords, para poderlos usar como filtros posteriormente. 

- Es importante mencionar que tambien se incluye a las columnas **procesadas** discount_price_dolares y actual_price_dolares, obtenidas en el nb 1, que transforman los precios originales expresados en Ruppias a dólares.

**3.2 Ingesta de Data: Implementar código en Python para leer archivo CSV y cargue el catálogo de productos en ElasticSearch.**

- El nb 1 contiene el proceso de Ingesta de datos en ES. Como primer paso, se realizó un preprocesamiento básico de los datos, en donde se trabajo en la conversión de los precios a dólares y la eliminación de productos que están duplicados en la base, considerando como clave primaria la combinación de los campos ["name", "main_category", "sub_category", "ratings","no_of_ratings","discount_price","actual_price"].Como resultado de la eliminación de duplicados se excluyen a cerca de 60 mil productos de la base del proceso de ingesta.

- Para el proceso de ingesta se usar la funcion **indexar_datos** en la que se utiliza sub agrupaciones o chunks para prevenir posibles errores en el proceso debido a la gran canridad de documentos que se ingestan. 

- Antes de comenzar la ingesta se incluyen conversiones a los formatos necesarios para asegurarnos de que todos los documentos en este y proximos procesos se inserten correctamente, ademas se incluyen en la funcion mensajes para verificar el progreso en la ingesta de documentos y un log de errores en **errores_indexacion.json**.


**3.3 Template Mustache para Búsquedas**

-El nb 2 incluye el seteo del template **amazon_search_template** que incluye la funcionalidad de un search_box utilizando el campo de nombre del producto "name" y un filtrado por termino usando el campo de categoria de producto **main_category**

**3.4 Priorizacion de resultados**

- El nb 2 incluye la mejora de priorización de resultados en el template. Para ello se utiliza a los campos de rating promedio **"ratings"** y cantidad de ratings que tiene el producto **"no_of_ratings"**, usando boost y priorizando los productos con ratings mayores a 4 con doble prioridad y con más de 100 ratings (con 1.5 veces más probabilidad).

**3.5 Desarrollo de una API en Flask**

- **Crear una API en Python usando Flask que exponga al menos dos endpoints:**

- La API de flask está disponible para su ejecución en **app.py**. El desarrollo a detal 
le del componente /search se encuentra en el nb 2, mientras que el desarrollo a detalle del componente de **/similar_products** que usa embeddings se encuentra en el nb3

- **/search: Para realizar búsquedas utilizando el template Mustache y el índice de ElasticSearch.**
- endpoint search: se usa la plantilla creada anteriormente con sus funcionalidades de busqueda de nombre y filtrado de categoria. En el nb2 se puede encontrar el proceso de desarrollo del endpoint asi como un ejemplo para testeo de su funcionalidad dentro de **app.py**

- **/similar_products: Para realizar consultas de productos similares.**
- endpoint similar_products: Este endpoint recibe un nombre de producto y utiliza un índice de Elasticsearch con embeddings previamente almacenados.El proceso de calculo y almacenamiento de los embeddings, asi como su indexación a ES esta disponible en el nb 3.
Al consultar, se calcula la similitud entre el embedding del producto consultado y los almacenados mediante la métrica de similitud de coseno para retornar los productos más similares en base a sus características semánticas.

**3.6 Implementación de Embeddings**

- **Gereracion de embeddings**: Para la seccion de generación de embeddings se realizó un trabajo extensivo, ya que, en primer lugar, se probó la funcionalidad del modelo **all-mpnet-base-v2**, que tuvo un tiempo de ejecución muy alto, ya que entre sus caracteristicas está generar embeddings de dimensionalidad mayor a 700, siendo bastate pesado para su procesamiento y posterior indexación. Debido a estos problemas, y a la carga pesada que esto representó en local, se probó con un modelo más ligero como es **sentence-transformers/all-MiniLM-L6-v2**

- **Almacenamiento y consulta**
Los embeddings generados de la base procesada se almacenan en  formato **"dense_vector""**. Ademas, se guarda un respaldo con los embeddings de toda la base en formato parquet.
En cuanto al proceso de consulta, **se define como metrica de similitud al coseno**, la implementación de la función de busqueda por similitud y ranqueo del top 5 por similitud se pueden encontrar en el nb3.

**4 Consideraciones Adicionales**

- **Validación y Manejo de Errores**
Se incluyen validaciones de las funciones de busqueda en los nbs, asi como celdas que sirven para validar la calidad de los datos y de sus estructuras antes de procesos como el indexing a E.S.

Los procesos de indexing de los nb almacenan un log de errores en un archivo json para su revisión y la optimización del proceso.

- **Testing**

Se incluye en los nbs 2 y 3 celdas para poder probar la funcionalidad de las funciones de busqueda

**5 Valor agregado**

- Se incluye la estructura basica para despliegue usando docker
- Se incluye funcion para reduccion de dimensiones que se puede usar para embeddings más complejos