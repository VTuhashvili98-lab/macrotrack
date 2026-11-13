import os

from sqlalchemy import URL, create_engine

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host="127.0.0.1",
    port=5432,
    database=os.environ["POSTGRES_DB"],
)

engine = create_engine(database_url)