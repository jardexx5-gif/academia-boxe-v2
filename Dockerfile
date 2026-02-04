# Usa uma versão leve do Python
FROM python:3.9-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia o seu script de cobrança para dentro da pasta /app
COPY main.py .

# Comando para rodar o script
CMD ["python", "main.py"]