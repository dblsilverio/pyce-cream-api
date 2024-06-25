FROM python:3.12-slim-bookworm
LABEL authors="diogo.silverio"

WORKDIR /app/

COPY . /app/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "8000"]