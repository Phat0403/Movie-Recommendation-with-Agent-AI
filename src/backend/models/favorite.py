from sqlalchemy import Column, Integer, VARCHAR
from db.session import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(VARCHAR(50), nullable=False, index=True)
    movie_id = Column(VARCHAR(20), nullable=False)

    def __repr__(self):
        return f"<Favorite(id={self.id}, username={self.username}, movie_id={self.movie_id})>"
    def __str__(self):
        return f"Favorite(id={self.id}, username={self.username}, movie_id={self.movie_id})"
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "movie_id": self.movie_id
        }