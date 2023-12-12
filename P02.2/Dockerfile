FROM python:3.8-slim

# Definir diretório de trabalho no container
WORKDIR /app

# Copie os arquivos necessários para o container
COPY chat.py /app/
COPY requeriments.txt /app/

# Instale as dependências
RUN pip install --no-cache-dir -r requeriments.txt

# Expor a porta usada pelo seu aplicativo (ajuste conforme necessário)
EXPOSE 12345

# Comando para executar quando o container for iniciado
CMD ["python", "chat.py"]
