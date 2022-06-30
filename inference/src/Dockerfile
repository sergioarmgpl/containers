FROM python:3.10.5-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python3 create_model.py

CMD ["sh", "-c", "python index.py"]

