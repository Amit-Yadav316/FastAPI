from fastapi import FastAPI
import models,user,blog,reset
import database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(user.router)
app.include_router(blog.router)
app.include_router(reset.router)




