from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


# models (SQLAlchemy)
class Post(Base):
    __tablename__ = "posts"

    # columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(80), nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, nullable=False, server_default="True")
    rating = Column(Integer, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
