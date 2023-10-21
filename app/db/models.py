from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, ForeignKey, Text, Table

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    password = Column(String(80))
    is_admin = Column(Boolean, default=False)
    posts = relationship("Post", back_populates="owner")

    def __repr__(self) -> str:
        return f"User(username={self.username}, is_admin={self.is_admin})"

# data = [{}]

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    owner = relationship("User", back_populates="posts")
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, server_default=func.now())
    comments = relationship("Comment", back_populates="post")

    def __repr__(self) -> str:
        return f"Post(data={self.data[:min(50, len(self.data))]})"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    post = relationship("Post", back_populates="comments")
    post_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"Comment(content={self.content[:min(50, len(self.content))]})"


association_table = Table(
    "teams",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("post_id", ForeignKey("posts.id")),
)