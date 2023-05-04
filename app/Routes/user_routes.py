from fastapi import APIRouter, Depends, HTTPException

from ..CRUD import user as crud_user
from ..database import db
from ..schema import User
# from fastapi.responses import RedirectResponse

router = APIRouter()

# -----------------
# Begin CRUD users


@router.get('/users')
def get_users(page: int = 0, count: int = 25, db=Depends(db)):
    info = crud_user.get_users(page, count, db)
    if info:
        return info
    else:
        raise HTTPException(404, crud_user.error_message(
            'No users'))

# Create user

# Create post using query params


@router.post('/user/new')
def create_user(user: User, db=Depends(db)):
    db_user = crud_user.create_user(db, user)
    return db_user

@router.get('/user/{user_id}')
def get_user(user_id: int, db=Depends(db)):
    db_user = crud_user.get_user(db, user_id)
    return db_user

@router.get('/user/phone/{phone}')
def get_user_by_phone(phone: int, db=Depends(db)):
    db_user = crud_user.get_user_by_phone(db, phone)
    return db_user

@router.get('/user/house/{house_id}')
def get_users_by_house(house_id: int, db=Depends(db)):
    db_user = crud_user.get_users_by_house(db, house_id)
    return db_user

# End CRUD users
# -----------------