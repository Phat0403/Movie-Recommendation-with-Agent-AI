
from sqlalchemy.orm import Session

from models.comment import Comment
from db.crud import BaseController

class CommentController(BaseController):
    def __init__(self, db: Session):
        self.db = db
    
    def get_comments_by_movie_id(self, movie_id: str):
        """
        Get all comments for a specific movie.
        
        Args:
            movie_id (str): The ID of the movie.
        
        Returns:
            List[Comment]: A list of comments for the specified movie.
        """
        return self.db.query(Comment).filter(Comment.movie_id == movie_id).all()
    
    def get_comments_by_username(self, username: str):
        """
        Get all comments made by a specific user.
        
        Args:
            username (str): The username of the user.
        
        Returns:
            List[Comment]: A list of comments made by the specified user.
        """
        return self.db.query(Comment).filter(Comment.username == username).all()
    
    