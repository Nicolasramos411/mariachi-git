from fastapi import APIRouter, Depends, HTTPException

from ..CRUD import house as crud_house
from ..database import db
from ..schema import House
# from fastapi.responses import RedirectResponse

router = APIRouter()

# -----------------
# Begin CRUD houses


@router.get('/houses')
def get_houses(page: int = 0, count: int = 25, db=Depends(db)):
    info = crud_house.get_houses(page, count, db)
    if info:
        return info
    else:
        raise HTTPException(404, crud_house.error_message(
            'No houses'))
    
# Create house
@router.post('/house/new')
def create_house(house: House, db=Depends(db)):
    db_house = crud_house.create_house(db, house)
    return db_house

@router.get('/house/{house_id}')
def get_house(house_id: int, db=Depends(db)):
    db_house = crud_house.get_house(db, house_id)
    return db_house

@router.get('/house/name/{name}')
def get_house_by_name(name: str, db=Depends(db)):
    db_house = crud_house.get_house_by_name(db, name)
    return db_house






# End CRUD houses
# -----------------