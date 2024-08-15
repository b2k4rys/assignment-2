from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import random

from faker import Faker


def create_users(total):
    fake = Faker()
    Faker.seed(1)

    ids = list(range(total))
    random.seed(1)
    random.shuffle(ids)

    elements = [
        {
            "id": ids[i] + 1,
            "email": fake.free_email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "username": fake.user_name(),
        }
        for i in range(total)
    ]

    return elements



users = create_users(100)  # Здесь хранятся список пользователей
app = FastAPI()

templates = Jinja2Templates(directory="templates")
users_by_id = dict()

for i in users:
    users_by_id[i['id']] = i
print(users_by_id[18])

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# (сюда писать решение)

@app.get('/users/{id}', response_class=HTMLResponse)
async def get_user(request: Request, id: str):
    user = users_by_id[int(id)]
    return templates.TemplateResponse(name="users/user.html", context={"user": user, "request": request})

@app.get('/users', response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse(name='users/index.html', context={'users':users, 'request':request})

# (конец решения)
