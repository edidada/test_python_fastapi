from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from src import employee as employee_crud, schemas, database

router = APIRouter()


@router.post("/login", response_model=schemas.AuthResponse)
def login(
    login_data: schemas.EmployeeLogin,
    request: Request,
    db: Session = Depends(database.get_db)
):
    employee = employee_crud.get_employee_by_username(db, username=login_data.username)
    
    if not employee or employee.password != login_data.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    request.session["user_id"] = employee.id
    request.session["username"] = employee.username
    request.session["name"] = employee.name
    
    return schemas.AuthResponse(
        code=0,
        message="登录成功",
        data=schemas.EmployeeResponse.model_validate(employee)
    )


@router.post("/logout", response_model=schemas.GenericResponse)
def logout(request: Request):
    request.session.clear()
    return schemas.GenericResponse(code=0, message="登出成功")


@router.get("/verify", response_model=schemas.VerifyResponse)
def verify(request: Request):
    if "user_id" in request.session:
        return schemas.VerifyResponse(
            code=0,
            message="已登录",
            data={
                "user_id": request.session.get("user_id"),
                "username": request.session.get("username"),
                "name": request.session.get("name")
            }
        )
    else:
        raise HTTPException(status_code=401, detail="未登录")
