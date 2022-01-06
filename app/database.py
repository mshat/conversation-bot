from peewee import PostgresqlDatabase

from dotenv import dotenv_values
config = dotenv_values("heroku.env")
db = PostgresqlDatabase(database=config["DB_NAME"], user=config["DB_USER"], password=config["DB_PASSWORD"],
                        host=config["DB_HOST"])
