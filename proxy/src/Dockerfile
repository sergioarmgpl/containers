FROM python:3.9.13-bullseye
WORKDIR /app

COPY requirements.txt .

RUN apt-get update -y
RUN apt-get install libatlas-base-dev -y
RUN pip install --index-url=https://www.piwheels.org/simple --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python index.py"]