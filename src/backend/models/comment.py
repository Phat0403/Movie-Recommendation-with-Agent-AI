from db.session import Base
from sqlalchemy import Column, Integer, VARCHAR, DateTime

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    movie_id = Column(VARCHAR(20), nullable=False)
    username = Column(VARCHAR(50), nullable=False)
    comment = Column(VARCHAR(255), nullable=False)
    comment_time = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Comment(id={self.id}, movie_id={self.movie_id}, username={self.username}, comment={self.comment}, comment_time={self.comment_time})>"
    
    def __str__(self):
        return f"Comment(id={self.id}, movie_id={self.movie_id}, username={self.username}, comment={self.comment}, comment_time={self.comment_time})"
    
    def as_dict(self):
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "username": self.username,
            "comment": self.comment,
            "comment_time": self.comment_time.isoformat() if self.comment_time else None
        }
