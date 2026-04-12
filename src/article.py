from sqlalchemy.orm import Session
from typing import List, Optional
from src import models, schemas


def get_article(db: Session, article_id: int) -> Optional[models.Article]:
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_articles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Article]:
    return db.query(models.Article).offset(skip).limit(limit).all()


def get_articles_count(db: Session) -> int:
    return db.query(models.Article).count()


def create_article(db: Session, article: schemas.ArticleCreate) -> models.Article:
    db_article = models.Article(title=article.title, content=article.content)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(db: Session, article_update: schemas.ArticleUpdate) -> Optional[models.Article]:
    db_article = get_article(db, article_update.id)
    if not db_article:
        return None
    
    if article_update.title is not None:
        db_article.title = article_update.title
    if article_update.content is not None:
        db_article.content = article_update.content
    
    db.commit()
    db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int) -> bool:
    db_article = get_article(db, article_id)
    if not db_article:
        return False
    
    db.delete(db_article)
    db.commit()
    return True
