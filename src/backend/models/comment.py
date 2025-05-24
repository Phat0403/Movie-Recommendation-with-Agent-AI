from db.session import Base
from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, DateTime

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    movie_id = Column(VARCHAR(20), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment = Column(VARCHAR(255), nullable=False)
    comment_time = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Comment(id={self.id}, movie_id={self.movie_id}, user_id={self.user_id}, content={self.content})>"