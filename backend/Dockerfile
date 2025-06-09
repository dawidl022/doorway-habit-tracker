FROM python:3.13-slim

WORKDIR /app

RUN apt update && apt install -y gcc libpq-dev

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
