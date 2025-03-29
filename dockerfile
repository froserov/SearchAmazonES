# Dockerfile

#  1. Imagen base de Python
FROM python:3.9

#  2. Establecer el directorio de trabajo
WORKDIR /app

#  3. Copiar todos los archivos al contenedor
COPY . /app

#  4. Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

#  5. Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#  6. Exponer el puerto donde correrá Flask
EXPOSE 5000

#  7. Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
