from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
import schemas, models,authentication,hashing
import database
from typing import List
from oaut2 import get_current_user

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(authentication.router)




@app.post("/blog",tags=["Blog"])
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db),current_user:schemas.User=Depends(get_current_user)):
    new_blog = models.Blog(body=request.body, title=request.title, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog", response_model=List[schemas.ShowBlog],tags=["Blog"])
def all_blog(db: Session = Depends(database.get_db),current_user:schemas.User=Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}", response_model=schemas.ShowBlog,tags=["Blog"])
def indi_blog(id: int, db: Session = Depends(database.get_db),current_user:schemas.User=Depends(get_current_user)):
    blog = db.query(models.Blog).options(joinedload(models.Blog.user)).filter(id==models.Blog.id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.delete("/blog/{id}",tags=["Blog"])
def del_blog(id: int, db: Session = Depends(database.get_db),current_user:schemas.User=Depends(get_current_user)):
    blog_d = db.query(models.Blog).filter(id==models.Blog.id).first()
    if not blog_d:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog_d)
    db.commit()
    return {"Blog deleted successfully"}

@app.put("/blog/{id}",tags=["Blog"])
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(database.get_db),current_user:schemas.User=Depends(get_current_user)):
    blog = db.query(models.Blog).filter(id==models.Blog.id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.body = request.body
    blog.title = request.title
    db.commit()
    db.refresh(blog)
    return blog

@app.post("/user",tags=["User"])
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(name=request.name, email=request.email, password=hashing.hashed(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}", response_model=schemas.ShowUser,tags=["User"])
def indi_user(id: int, db: Session = Depends(database.get_db),current_user:schemas.User=Depends(get_current_user)):
    user = db.query(models.User).options(joinedload(models.User.blogs)).filter(id==models.User.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




