from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schema, models


def get_houses(page: int, count: int, db: Session):

    return db.query(models.House).offset(page * count).limit(count).all()


def create_house(db: Session, house: schema.House):

    try:
        # models.House(**house.dict()).validate()
        with db.begin(subtransactions=True):

            # Verify if house
            db_house = db.query(models.House).filter(
                models.House.name == house.name).first()

            db_house = models.House(**house.dict())
            db.add(db_house)
            db.flush()
        db.commit()
        db.refresh(db_house)
        return db_house

    except (ValueError, IntegrityError) as e:
        db.rollback()
        return error_message(str(e))


def get_house(db: Session, house_id: int):

    try:
        house_data = db.query(models.House).filter(
            models.House.id == house_id).first()
        if not house_data:
            return error_message('House not found')
        return house_data

    except Exception as e:
        return error_message(str(e))


def get_house_by_name(db: Session, name: str):

    try:
        house_data = db.query(models.House).filter(
            models.House.name == name).first()
        if not house_data:
            return error_message('House not found')
        return house_data

    except Exception as e:
        return error_message(str(e))


def error_message(message: str):
    return {
        'error': message
    }
