from peewee import PostgresqlDatabase
from dotenv import dotenv_values

CONFIG = dotenv_values("heroku.env")

DB = PostgresqlDatabase(database=CONFIG["DB_NAME"], user=CONFIG["DB_USER"], password=CONFIG["DB_PASSWORD"],
                        host=CONFIG["DB_HOST"])
