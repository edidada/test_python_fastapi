from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    content: Optional[str] = None


class ArticleResponse(ArticleBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    code: int = 0
    message: str = "获取成功"
    data: List[ArticleResponse]


class ArticlePageResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ArticleResponse]


class ArticlePageResult(BaseModel):
    code: int = 0
    message: str = "获取成功"
    data: ArticlePageResponse


class EmployeeLogin(BaseModel):
    username: str
    password: str


class EmployeeResponse(BaseModel):
    id: str
    username: str
    name: str
    
    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    code: int = 0
    message: str
    data: Optional[EmployeeResponse] = None


class VerifyResponse(BaseModel):
    code: int = 0
    message: str
    data: Optional[dict] = None


class CategoryBase(BaseModel):
    name: str
    type: Optional[int] = 1
    sort: Optional[int] = 0
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    id: str
    name: Optional[str] = None
    type: Optional[int] = None
    sort: Optional[int] = None
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: str
    is_deleted: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    code: int = 0
    message: str = "获取成功"
    data: List[CategoryResponse]


class DishBase(BaseModel):
    name: str
    category_id: Optional[str] = None
    price: Optional[float] = 0.0
    image: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = 1
    sort: Optional[int] = 0


class DishCreate(DishBase):
    pass


class DishUpdate(BaseModel):
    id: str
    name: Optional[str] = None
    category_id: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    sort: Optional[int] = None


class DishResponse(DishBase):
    id: str
    is_deleted: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DishListResponse(BaseModel):
    code: int = 0
    message: str = "获取成功"
    data: List[DishResponse]


class GenericResponse(BaseModel):
    code: int = 0
    message: str
    data: Optional[dict] = None
