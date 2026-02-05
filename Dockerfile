# Usa uma versão leve do Python
FROM python:3.9-slim

# Define a pasta de trabalho
WORKDIR /app

# Copia TODOS os arquivos (incluindo o requirements.txt)
COPY . .

# COMANDO QUE ESTAVA FALTANDO: Instala as bibliotecas
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o script
CMD ["python", "main.py"]