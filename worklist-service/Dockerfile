FROM python:3.11-slim

WORKDIR /app

# Instala dependências
RUN pip install --no-cache-dir flask pydicom

# Copia o serviço
COPY worklist-service.py .

# Cria diretório de worklists
RUN mkdir -p /worklists

# Expõe a porta
EXPOSE 8002

# Comando para iniciar
CMD ["python", "worklist-service.py"]