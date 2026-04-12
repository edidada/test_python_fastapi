from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
import uuid
from src import models, schemas


def get_category(db: Session, category_id: str) -> Optional[models.Category]:
    return db.query(models.Category).filter(
        and_(
            models.Category.id == category_id,
            models.Category.is_deleted == 0
        )
    ).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    return db.query(models.Category).filter(
        models.Category.is_deleted == 0
    ).offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    category_id = str(uuid.uuid4())
    db_category = models.Category(
        id=category_id,
        name=category.name,
        type=category.type,
        sort=category.sort,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_update: schemas.CategoryUpdate) -> Optional[models.Category]:
    db_category = get_category(db, category_update.id)
    if not db_category:
        return None
    
    update_data = category_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: str) -> bool:
    db_category = get_category(db, category_id)
    if not db_category:
        return False
    
    db_category.is_deleted = 1
    db.commit()
    return True
