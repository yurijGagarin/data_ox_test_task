FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY alembic /app/alembic/
COPY parser /app/parser/
COPY alembic.ini /app/

CMD alembic upgrade head && python -m parser.main
