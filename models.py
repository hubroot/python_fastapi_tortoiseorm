from tortoise.models import Model
from tortoise import fields

class Person(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    dob = fields.DateField()
    class Meta:
        table="person"

class Account(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    created_at = fields.DatetimeField()
    person = fields.OneToOneField('models.Person', related_name='account')
    class Meta:
        table="account"
