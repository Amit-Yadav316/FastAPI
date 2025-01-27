from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    name= Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    blogs = relationship("Blog", back_populates="user")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(String, nullable=False)
    title = Column(String, nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="blogs")




