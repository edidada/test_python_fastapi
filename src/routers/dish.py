from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src import dish_crud, schemas, database

router = APIRouter()


@router.get("/list", response_model=schemas.DishListResponse)
def dish_list(db: Session = Depends(database.get_db)):
    dishes = dish_crud.get_dishes(db)
    return schemas.DishListResponse(
        code=0,
        message="获取成功",
        data=[schemas.DishResponse.model_validate(d) for d in dishes]
    )


@router.post("/add", response_model=schemas.GenericResponse, status_code=201)
def dish_add(dish: schemas.DishCreate, db: Session = Depends(database.get_db)):
    db_dish = dish_crud.create_dish(db=db, dish=dish)
    return schemas.GenericResponse(
        code=0,
        message="添加成功",
        data={"id": db_dish.id, "name": db_dish.name}
    )


@router.post("/edit", response_model=schemas.GenericResponse)
def dish_edit(dish_update: schemas.DishUpdate, db: Session = Depends(database.get_db)):
    db_dish = dish_crud.update_dish(db=db, dish_update=dish_update)
    if not db_dish:
        raise HTTPException(status_code=404, detail="菜品不存在")
    
    return schemas.GenericResponse(
        code=0,
        message="编辑成功",
        data={"id": db_dish.id, "name": db_dish.name}
    )


@router.post("/delete", response_model=schemas.GenericResponse)
def dish_delete(dish_id: dict, db: Session = Depends(database.get_db)):
    did = dish_id.get("id")
    if not did:
        raise HTTPException(status_code=400, detail="菜品ID不能为空")
    
    success = dish_crud.delete_dish(db=db, dish_id=did)
    if not success:
        raise HTTPException(status_code=404, detail="菜品不存在")
    
    return schemas.GenericResponse(code=0, message="删除成功")
