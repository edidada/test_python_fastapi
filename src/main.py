from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from src.config import get_settings
from src.database import engine, SessionLocal
from src import models
from src.routers import auth, blog, category, dish
from src.employee import create_employee

settings = get_settings()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="session_id",
    max_age=86400
)


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        from src.models import Employee
        existing = db.query(Employee).filter(Employee.username == "admin").first()
        if not existing:
            create_employee(db, name="管理员", username="admin", password="admin123")
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "code": 0,
        "message": "Blog REST API Server",
        "data": {
            "version": settings.APP_VERSION,
            "endpoints": [
                "/login", "/logout", "/verify",
                "/blog/list", "/blog/add", "/blog/edit", "/blog/delete", "/blog/page",
                "/category/list", "/category/add", "/category/edit", "/category/delete",
                "/dish/list", "/dish/add", "/dish/edit", "/dish/delete"
            ]
        }
    }


app.include_router(auth.router, tags=["auth"])
app.include_router(blog.router, prefix="/blog", tags=["blog"])
app.include_router(category.router, prefix="/category", tags=["category"])
app.include_router(dish.router, prefix="/dish", tags=["dish"])


def main():
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )


if __name__ == "__main__":
    main()
