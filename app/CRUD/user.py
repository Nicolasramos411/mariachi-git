from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schema, models


def get_users(page: int, count: int, db: Session):

    return db.query(models.User).offset(page * count).limit(count).all()


def create_user(db: Session, user: schema.User):

    try:
        # models.User(**user.dict()).validate()
        with db.begin(subtransactions=True):

            # Verify if user
            db_user = db.query(models.User).filter(
                models.User.phone == user.phone).first()

            db_user = models.User(
                name=user.name,
                phone=user.phone,
                house_id=user.house_id
            )
            db.add(db_user)
            db.flush()
        db.commit()
        db.refresh(db_user)
        return db_user

    except (ValueError, IntegrityError) as e:
        db.rollback()
        return error_message(str(e))


def get_user(db: Session, user_id: int):

    try:
        user_data = db.query(models.User).filter(
            models.User.id == user_id).first()
        if not user_data:
            return error_message('User not found')
        return user_data

    except Exception as e:
        return error_message(str(e))


def get_user_by_phone(db: Session, phone: int):

    try:
        user_data = db.query(models.User).filter(
            models.User.phone == phone).first()
        if not user_data:
            return error_message('User not found')
        return user_data

    except Exception as e:
        return error_message(str(e))


def get_users_by_house(db: Session, house_id: int):

    try:
        users_data = db.query(models.User).filter(
            models.User.house_id == house_id).all()
        if not users_data:
            return error_message('User not found')
        return users_data

    except Exception as e:
        return error_message(str(e))


def delete_user(db: Session, user_id: int):

    try:
        user_data = db.query(models.User).filter(
            models.User.id == user_id).first()
        if not user_data:
            return error_message('User not found')
        db.delete(user_data)
        db.commit()
        return user_data

    except Exception as e:
        return error_message(str(e))


def error_message(message, status_code=404):
    return {
        'error': message,
        'status': status_code
    }
