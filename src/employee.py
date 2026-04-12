from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
import uuid
from src import models


def get_employee_by_username(db: Session, username: str) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(
        and_(
            models.Employee.username == username,
            models.Employee.status == 1,
            models.Employee.is_deleted == 0
        )
    ).first()


def create_employee(db: Session, name: str, username: str, password: str) -> models.Employee:
    employee_id = str(uuid.uuid4())
    db_employee = models.Employee(
        id=employee_id,
        name=name,
        username=username,
        password=password
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
