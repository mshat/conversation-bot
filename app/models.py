from peewee import Model, Check
from peewee import CharField, PrimaryKeyField, FloatField
from settings import DB


models = []


class User(Model):
    id = PrimaryKeyField(null=False)
    GENDER_CHOICES = ("MAN", "WOMAN", "OTHER")
    gender = CharField(
        max_length=max([len(choice) for choice in GENDER_CHOICES]),
        constraints=[Check(f"gender in {GENDER_CHOICES}")])
    photo_path = CharField(null=True)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    bio = CharField(null=True)

    class Meta:
        db_table = 'users'
        database = DB


models.append(User)
