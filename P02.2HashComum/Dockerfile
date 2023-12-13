FROM python:3.8-slim

WORKDIR /app

COPY chat3.py /app/
COPY requeriments.txt /app/

RUN pip install --no-cache-dir -r requeriments.txt

EXPOSE 12345

CMD ["python", "chat3.py"]
