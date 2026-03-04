    FROM python:3.11-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    RUN mkdir -p cache data && \
        RUN mkdir -p cache data

    EXPOSE 5000

    CMD ["python", "app.py"]