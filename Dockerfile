# Use uma imagem base Python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie os arquivos do projeto para o diretório de trabalho
COPY . .

# Exponha a porta 5000 para que o aplicativo FastAPI seja acessível
EXPOSE 5000

# Execute o aplicativo FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]