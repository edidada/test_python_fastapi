from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src import category_crud, schemas, database

router = APIRouter()


@router.get("/list", response_model=schemas.CategoryListResponse)
def category_list(db: Session = Depends(database.get_db)):
    categories = category_crud.get_categories(db)
    return schemas.CategoryListResponse(
        code=0,
        message="获取成功",
        data=[schemas.CategoryResponse.model_validate(c) for c in categories]
    )


@router.post("/add", response_model=schemas.GenericResponse, status_code=201)
def category_add(category: schemas.CategoryCreate, db: Session = Depends(database.get_db)):
    db_category = category_crud.create_category(db=db, category=category)
    return schemas.GenericResponse(
        code=0,
        message="添加成功",
        data={"id": db_category.id, "name": db_category.name}
    )


@router.post("/edit", response_model=schemas.GenericResponse)
def category_edit(category_update: schemas.CategoryUpdate, db: Session = Depends(database.get_db)):
    db_category = category_crud.update_category(db=db, category_update=category_update)
    if not db_category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    return schemas.GenericResponse(
        code=0,
        message="编辑成功",
        data={"id": db_category.id, "name": db_category.name}
    )


@router.post("/delete", response_model=schemas.GenericResponse)
def category_delete(category_id: dict, db: Session = Depends(database.get_db)):
    cid = category_id.get("id")
    if not cid:
        raise HTTPException(status_code=400, detail="分类ID不能为空")
    
    success = category_crud.delete_category(db=db, category_id=cid)
    if not success:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    return schemas.GenericResponse(code=0, message="删除成功")
