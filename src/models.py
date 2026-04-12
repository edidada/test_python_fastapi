from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database import Base


class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class User(Base):
    __tablename__ = "users"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    sex = Column(String(10))
    id_number = Column(String(50))
    avatar = Column(String(255))
    is_deleted = Column(Integer, default=0)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())


class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(20))
    sex = Column(String(10))
    id_number = Column(String(50))
    status = Column(Integer, default=1)
    is_deleted = Column(Integer, default=0)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(Integer, default=1)
    sort = Column(Integer, default=0)
    description = Column(String(255))
    is_deleted = Column(Integer, default=0)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())


class Dish(Base):
    __tablename__ = "dishes"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category_id = Column(String(50))
    price = Column(Float, default=0.0)
    image = Column(String(255))
    description = Column(Text)
    status = Column(Integer, default=1)
    sort = Column(Integer, default=0)
    is_deleted = Column(Integer, default=0)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())
