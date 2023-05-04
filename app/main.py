from fastapi import FastAPI, Depends, HTTPException, Query
from .Routes import (
    user_routes,
    house_routes
)
from .database import engine, db
from . import models
from fastapi.responses import RedirectResponse
from .schema import (
    User,
    House,
    RegisterUser,
    AddPoints
)

from .CRUD import (
    user as crud_user,
    house as crud_house
)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_routes.router)


@app.get('/')
def redirect_to_docs():
    print("bien bien")
    return RedirectResponse(url='/docs')


@app.get("/verify_user")
def verify_user(db=Depends(db), phone: int = Query(..., description="Número de teléfono a checkear")):
    user = crud_user.get_user_by_phone(db, phone)
    if user is None or "error" in user:
        return "No existe"
    else:
        if user.name == "NN":
            return "No Nombre"
        else:
            return "Registrado"

# Recibo la información del usuario y la guardo en la base de datos si la empresa existe, si el usuario no existe


@app.post("/register_user")
###
# {
#     "name": "Nicolas",
#     "phone": 5456432237,
#     "house_name": "Casa de Nico"
# }
###
def register_user(register_user: RegisterUser, db=Depends(db)):

    house = crud_house.get_house_by_name(db, register_user.house_name)
    if house is None:
        return "No existe la casa"

    elif type(house) == dict and "error" in house:
        return "No existe la casa"

    else:
        register_user.house_id = house.id
        user = crud_user.get_user_by_phone(db, register_user.phone)
        if user is None:
            user = crud_user.create_user(db, register_user)
            return user
        else:
            if type(user) == dict and "error" in user:
                user = crud_user.create_user(db, register_user)
                return user

            print(user)
            return "Ya existe el usuario"


@app.post("/add_points")
###
# {
#     "phone": 5456432237,
#     "points": 10
# }
###
def add_points(add_points: AddPoints, db=Depends(db)):
    user = crud_user.get_user_by_phone(db, add_points.phone)
    if user is None:
        return "No existe el usuario"
    else:
        user.points += add_points.points
        db.commit()
        return user


@app.post("/delete_user/{user_id}")
def delete_user(user_id: int, db=Depends(db)):
    user = crud_user.get_user(db, user_id)
    if user is None:
        return "No existe el usuario"
    else:
        db.delete(user)
        db.commit()
        return "Usuario eliminado"


@app.post("/house/new")
def new_house(house: House, db=Depends(db)):
    house = crud_house.create_house(db, house)
    return house


@app.get("/house/{house_id}")
def get_house(house_id: int, db=Depends(db)):
    house = crud_house.get_house(db, house_id)
    return house


@app.get("/houses")
def get_houses(page: int = 0, count: int = 25, db=Depends(db)):
    houses = crud_house.get_houses(page, count, db)
    return houses


@app.post("/house/delete/{house_id}")
def delete_house(house_id: int, db=Depends(db)):
    house = crud_house.get_house(db, house_id)
    if house is None:
        return "No existe la casa"
    else:
        db.delete(house)
        db.commit()
        return "Casa eliminada"
