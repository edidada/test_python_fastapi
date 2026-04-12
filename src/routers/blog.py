from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src import article, schemas, database

router = APIRouter()


@router.get("/list", response_model=schemas.ArticleListResponse)
def blog_list(db: Session = Depends(database.get_db)):
    articles = article.get_articles(db)
    return schemas.ArticleListResponse(
        code=0,
        message="获取成功",
        data=[schemas.ArticleResponse.model_validate(a) for a in articles]
    )


@router.get("/page", response_model=schemas.ArticlePageResult)
def blog_page(page: int = 1, page_size: int = 10, db: Session = Depends(database.get_db)):
    skip = (page - 1) * page_size
    total = article.get_articles_count(db)
    articles = article.get_articles(db, skip=skip, limit=page_size)
    
    return schemas.ArticlePageResult(
        code=0,
        message="获取成功",
        data=schemas.ArticlePageResponse(
            total=total,
            page=page,
            page_size=page_size,
            items=[schemas.ArticleResponse.model_validate(a) for a in articles]
        )
    )


@router.post("/add", response_model=schemas.GenericResponse, status_code=201)
def blog_add(article: schemas.ArticleCreate, db: Session = Depends(database.get_db)):
    db_article = article.create_article(db=db, article=article)
    return schemas.GenericResponse(
        code=0,
        message="添加成功",
        data={
            "id": db_article.id,
            "title": db_article.title,
            "content": db_article.content
        }
    )


@router.post("/edit", response_model=schemas.GenericResponse)
def blog_edit(article_update: schemas.ArticleUpdate, db: Session = Depends(database.get_db)):
    db_article = article.update_article(db=db, article_update=article_update)
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    return schemas.GenericResponse(
        code=0,
        message="编辑成功",
        data={
            "id": db_article.id,
            "title": db_article.title,
            "content": db_article.content
        }
    )


@router.post("/delete", response_model=schemas.GenericResponse)
def blog_delete(article_id: dict, db: Session = Depends(database.get_db)):
    aid = article_id.get("id")
    if not aid:
        raise HTTPException(status_code=400, detail="文章ID不能为空")
    
    success = article.delete_article(db=db, article_id=aid)
    if not success:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    return schemas.GenericResponse(code=0, message="删除成功")
