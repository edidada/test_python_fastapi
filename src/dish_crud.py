from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
import uuid
from src import models, schemas


def get_dish(db: Session, dish_id: str) -> Optional[models.Dish]:
    return db.query(models.Dish).filter(
        and_(
            models.Dish.id == dish_id,
            models.Dish.is_deleted == 0
        )
    ).first()


def get_dishes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Dish]:
    return db.query(models.Dish).filter(
        models.Dish.is_deleted == 0
    ).offset(skip).limit(limit).all()


def create_dish(db: Session, dish: schemas.DishCreate) -> models.Dish:
    dish_id = str(uuid.uuid4())
    db_dish = models.Dish(
        id=dish_id,
        name=dish.name,
        category_id=dish.category_id,
        price=dish.price,
        image=dish.image,
        description=dish.description,
        status=dish.status,
        sort=dish.sort
    )
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def update_dish(db: Session, dish_update: schemas.DishUpdate) -> Optional[models.Dish]:
    db_dish = get_dish(db, dish_update.id)
    if not db_dish:
        return None
    
    update_data = dish_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_dish, key, value)
    
    db.commit()
    db.refresh(db_dish)
    return db_dish


def delete_dish(db: Session, dish_id: str) -> bool:
    db_dish = get_dish(db, dish_id)
    if not db_dish:
        return False
    
    db_dish.is_deleted = 1
    db.commit()
    return True
