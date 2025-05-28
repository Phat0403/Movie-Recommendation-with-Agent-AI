from db.crud_comment import CommentController
from models.comment import Comment

from datetime import datetime
from sqlalchemy.orm import Session

import logging

class CommentService:
    def __init__(self, db: Session):
        self.db = db
        self.comment_controller = CommentController(db)

    def create(self, movie_id: str, username: str, comment_text: str) -> Comment:
        """
        Create a new comment for a movie.
        
        Args:
            movie_id (str): The ID of the movie.
            username (str): The username of the user making the comment.
            comment_text (str): The content of the comment.
        
        Returns:
            Comment: The created comment instance.
        """

        try:
            new_comment = Comment(
                movie_id=movie_id,
                username=username,
                comment=comment_text,
                comment_time=datetime.now()
            )
            self.comment_controller.create(new_comment)
        except Exception as e:
            logging.error(f"Error creating comment for movie {movie_id} by user {username}: {e}")
            return None
        return new_comment
    
    def get(self, comment_id: int) -> Comment:
        """
        Retrieve a comment by its ID.
        
        Args:
            comment_id (int): The ID of the comment.
        
        Returns:
            Comment: The comment instance if found, otherwise None.
        """
        
        try:
            comment = self.comment_controller.get(Comment, id=comment_id)
        except Exception as e:
            logging.error(f"Error retrieving comment {comment_id}: {e}")
            return None
        return comment

    def get_comments_by_movie_id(self, movie_id: str) -> list[Comment]:
        """
        Retrieve all comments for a specific movie.
        
        Args:
            movie_id (str): The ID of the movie.
        
        Returns:
            list[Comment]: A list of comments associated with the specified movie.
        """
        try:
            comments = self.comment_controller.get_comments_by_movie_id(movie_id)
        except Exception as e:
            logging.error(f"Error retrieving comments for movie {movie_id}: {e}")
            return None
        return {"status": 200, "message": "Comments retrieved successfully", "comments": comments}

    def get_comments_by_username(self, username: str) -> list[Comment]:
        """
        Retrieve all comments made by a specific user.
        
        Args:
            username (str): The username of the user.
        
        Returns:
            list[Comment]: A list of comments made by the specified user.
        """
        
        try:
            comments = self.comment_controller.get_comments_by_username(username)
        except Exception as e:
            logging.error(f"Error retrieving comments for user {username}: {e}")
            return None
        if not comments:
            return {"status": 200, "message": "No comments found for this user", "comments": []}
        return {"status": 200, "message": "Comments retrieved successfully", "comments": comments}
    
    def update(self, comment_id: int, new_comment: str) -> Comment:
        """
        Update an existing comment.
        
        Args:
            comment_id (int): The ID of the comment to update.
            new_text (str): The new content for the comment.
        
        Returns:
            Comment: The updated comment instance, or None if not found.
        """
        
        try:
            existing_comment = self.comment_controller.get(Comment, id=comment_id)
            if not existing_comment:
                raise ValueError(f"Comment with ID {comment_id} not found")
            self.comment_controller.update(existing_comment, comment=new_comment, comment_time=datetime.now())
        except Exception as e:
            logging.error(f"Error updating comment {comment_id}: {e}")
            raise ValueError(f"Failed to update comment: {e}")
        return existing_comment
    
    def delete(self, comment_id: int) -> bool:
        """
        Delete a comment by its ID.
        
        Args:
            comment_id (int): The ID of the comment to delete.
        
        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        
        try:
            existing_comment = self.comment_controller.get(Comment, id=comment_id)
            if not existing_comment:
                return {"status": 404, "message": "Comment with ID {comment_id} not found"}
            self.comment_controller.delete(existing_comment, id=comment_id)
        except Exception as e:
            logging.error(f"Error deleting comment {comment_id}: {e}")
            return {"status": 400, "message": "Failed to delete comment"}
        return {"status": 200, "message": "Comment deleted successfully"}
    
if __name__ == "__main__":
    from db.clients import get_db
    db = next(get_db())
    comment_service = CommentService(db)
    # Example usage
    # comment_service.create(movie_id="tt1234567", username="testuser", comment_text="Bad movie!")
    response = comment_service.delete(10)
    print(response)
    # comment = Comment(
    #     movie_id="tt1234567",
    #     username="testuser",
    #     comment="Great movie!",
    #     comment_time=datetime.now()
    # )
    # comment_service.comment_controller.create(comment)