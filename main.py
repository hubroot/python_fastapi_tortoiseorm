from fastapi import FastAPI, HTTPException
from tortoise import Tortoise
from models import Person, Account
from tortoise.contrib.fastapi import register_tortoise
import random
import string
import requests
from datetime import date

app = FastAPI()

def fetchData(url) : 
    response = requests.get(url)
    json = response.json()
    return json.get('data')

def fetchNames(nameType) :
    return fetchData('https://www.randomlists.com/data/names-'+nameType+'.json')

def pickRandom(list) :
    return random.choice(list)

def generateName() :
    response = fetchNames(pickRandom(['male', 'female']))
    return pickRandom(response)

def randomString() :
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(16))

@app.get("/")
async def index():
    for i in range(50):
        name = generateName()
        person = await Person.create(name=name, dob=date.today())
        account = await Account.create(person_id=person.id, email=randomString()+'@gmail.com', password=randomString())
    
    await Person.all().prefetch_related('account')
    await Person.all().delete()
    await Account.all().delete()

    return "Hello World!"

register_tortoise(
    app,
    db_url='mysql://root:root@localhost:3306/benchmark',
    modules={"models": ["models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)