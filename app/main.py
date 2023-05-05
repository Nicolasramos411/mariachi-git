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

from random import randint, choice


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


@app.post("/desition/handler")
def desition():
    options = ["imagen", "audio", "texto"]
    # Mata piscola sea 1 con probabilidad de un 10%
    random_value = randint(1, 10)
    mata_piscola = 0
    if random_value == 1:
        mata_piscola = 1

    # Selecciona una opcion al azar
    random_value = randint(0, 2)
    random_option = options[random_value]

    images_links = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4I5RiCahoreZ_ctm7siY0TsYDihdxL-bwyQ&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbzADEWWb2sKxD4V4n2AIRzsm_FT6aSxSUQ1itNedyTLeR-4DUdTwfDb3cqhn7vH0m0gQ&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6FN4PBxoMFKd74bbjJblL6ozLDulw_E4ROA&usqp=CAU",
        "https://i.scdn.co/image/ab67616d0000b273a76c5855e6a5e9587072a064",
        "data:image/jpeg;base64,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",
        "data:image/jpeg;base64,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",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-p7FZXvH0hw77BCzlbiiNFheWFEkR8VGBOg&usqp=CAU",
        "https://images2.memedroid.com/images/UPLOADED15/4fe770b2dd1d8.jpeg"
    ]

    texts = [
        "Orale cabrón dale un trago a la piscola",
        "Viva mexico cabrones",
        "Viva chile mierda!, perdón, Mexico",
        "Mata la piscola"
    ]

    audio_links = [
        "https://mariachi-s3.s3.amazonaws.com/y2mate.com+-+Celebraci%C3%B3n+Mariachi+efecto+de+sonido.mp3",
        "https://mariachi-s3.s3.amazonaws.com/y2mate.com+-+Audio+Orale+Ps+ya+es+martes+aaaaaaaaahhhhhhhh.mp3",
        "https://mariachi-s3.s3.amazonaws.com/y2mate.com+-+El+grito+mexicano+viva+mexico.mp3",
        "https://mariachi-s3.s3.amazonaws.com/y2mate.com+-+grito+mexicano.mp3"
    ]

    info = ""
    if random_option == "imagen":
        info = choice(images_links)
    elif random_option == "texto":
        info = choice(texts)
    elif random_option == "audio":
        info = choice(audio_links)

    return {
        "mata_piscola": mata_piscola,
        "option": random_option,
        "status": "OK",
        "info": info
    }
