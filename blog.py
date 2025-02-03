from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
import schemas, models,hashing
import database
from typing import List
from oaut2 import get_current_user

router=APIRouter(tags=["Blog"])

@router.post("/blog")
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db),current_user:schemas.User=Depends(get_current_user)):
    new_blog = models.Blog(body=request.body, title=request.title, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/blog", response_model=List[schemas.ShowBlog])
def all_blog(db: Session = Depends(database.get_db),current_user:schemas.User=Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get("/blog/{id}", response_model=schemas.ShowBlog)
def indi_blog(id: int, db: Session = Depends(database.get_db),current_user:schemas.User=Depends(get_current_user)):
    blog = db.query(models.Blog).options(joinedload(models.Blog.user)).filter(id==models.Blog.id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.delete("/blog/{id}")
def del_blog(id: int, db: Session = Depends(database.get_db),current_user:schemas.User=Depends(get_current_user)):
    blog_d = db.query(models.Blog).filter(id==models.Blog.id).first()
    if not blog_d:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog_d)
    db.commit()
    return {"Blog deleted successfully"}

@router.put("/blog/{id}")
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(database.get_db),current_user:schemas.User=Depends(get_current_user)):
    blog = db.query(models.Blog).filter(id==models.Blog.id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.body = request.body
    blog.title = request.title
    db.commit()
    db.refresh(blog)
    return blog
