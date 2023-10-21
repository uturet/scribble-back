from sqlalchemy.orm import relationship, Mapped
from typing import List
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Text, Table
from pydantic import ConfigDict
from app.db import Base


teams = Table(
    "teams",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("post_id", ForeignKey("posts.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    password = Column(String(80))
    image = Column(String(100))
    own_posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")
    team_posts: Mapped[List["Post"]] = relationship(
        secondary=teams, back_populates="users"
    )

    def __repr__(self) -> str:
        return f"User(username={self.username}, is_admin={self.is_admin})"

# data = [{canvas: text, description: text}]


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    img = Column(String(80), nullable=False)
    owner = relationship("User", back_populates="own_posts")
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, server_default=func.now())
    comments = relationship("Comment", back_populates="post")
    users: Mapped[List["User"]] = relationship(
        secondary=teams, back_populates="team_posts"
    )

    def __repr__(self) -> str:
        return f"Post(data={self.data[:min(50, len(self.data))]})"


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    post = relationship("Post", back_populates="comments")
    post_id = Column(Integer, ForeignKey('posts.id'))
    owner = relationship("User", back_populates="comments")
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"Comment(content={self.content[:min(50, len(self.content))]})"


