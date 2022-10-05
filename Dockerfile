FROM python:3.9

RUN apt-get update && \
    apt-get install -y && \
    python -m pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8000


CMD ["uvicorn", "app.app:app", "--host=0.0.0.0", "--reload","--port=8000"]