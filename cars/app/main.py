from fastapi import FastAPI, Response, HTTPException
import random
from faker import Faker
from faker_vehicle import VehicleProvider


def create_cars(cars_total):
    fake = Faker()
    fake.add_provider(VehicleProvider)

    car_ids = list(range(cars_total))
    random.seed(0)
    random.shuffle(car_ids)

    cars = [
        {
            "id": car_ids[i] + 1,
            "name": fake.vehicle_make_model(),
            "year": fake.machine_year(),
        }
        for i in range(cars_total)
    ]

    return cars




cars = create_cars(100)  # Здесь хранятся список машин
app = FastAPI()

car_list = cars
car_by_id = dict()

for i in car_list:
    car_by_id[i['id']] = i



@app.get("/")
def index():
    return Response("<a href='/cars'>Cars</a>")


# (сюда писать решение)

@app.get('/cars')
def cars(page: int = 1, limit: int = 10):
    return car_list[page*limit-10:page*limit]

@app.get('/cars/{id}')
def cars(id: str):
    if int(id) in car_by_id.keys():
        return car_by_id[int(id)]
    else:
        raise HTTPException(status_code=404, detail="Item not found")


# (конец решения)
