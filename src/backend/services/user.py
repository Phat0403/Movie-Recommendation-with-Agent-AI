from sqlalchemy.orm import Session
from models.favorite import Favorite
from db.crud_comment import CommentController
from db.crud_user import UserController
from models.user import User


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.comment_controller = CommentController(db)
        self.user_controller = UserController(db)

    def add_favorite_movie(self, username: str, movie_id: str) -> bool:
        """
        Add a movie to the user's favorite list.
        
        Args:
            username (str): The ID of the user.
            movie_id (str): The ID of the movie to be added.
        
        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        print(f"Adding favorite movie: {movie_id} for user: {username}")
        db_favorite = Favorite(username=username, movie_id=movie_id)
        existing_favorite = self.db.query(Favorite).filter(
            Favorite.username == username,
            Favorite.movie_id == movie_id
        ).first()
        if existing_favorite:
            raise ValueError("Movie is already in favorites")
        try:
            self.db.add(db_favorite)
            self.db.commit()
            self.db.refresh(db_favorite)
        except Exception as e:
            print(f"Error adding favorite movie: {e}")
            self.db.rollback()
            return False
        return True
    
    def remove_favorite_movie(self, username: str, movie_id: str) -> bool:
        """
        Remove a movie from the user's favorite list.
        
        Args:
            username (str): The ID of the user.
            movie_id (str): The ID of the movie to be removed.
        
        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        db_favorite = self.db.query(Favorite).filter(
            Favorite.username == username,
            Favorite.movie_id == movie_id
        ).first()

        if not db_favorite:
            raise ValueError("Favorite movie not found")

        try:
            self.db.delete(db_favorite)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()  
            raise ValueError(f"Error removing favorite movie: {e}")
    
    def get_favorite_movies(self, username: str) -> list[str]:
        """
        Retrieve the list of favorite movies for a user.
        
        Args:
            username (str): The ID of the user.
        
        Returns:
            list[str]: A list of movie IDs that are marked as favorites by the user.
        """
        try:
            favorites = self.db.query(Favorite).filter(Favorite.username == username).all()
            return [fav.movie_id for fav in favorites]
        except Exception as e:
            print(f"Error retrieving favorite movies: {e}")
            return []
    
    def get_user_info(self, username: str) -> dict:
        """
        Retrieve user information by user ID.
        
        Args:
            username (str): The ID of the user.
        
        Returns:
            dict: A dictionary containing user information, or an empty dictionary if not found.
        """
        user = self.user_controller.get(User,username=username)
        favorite_movies = self.get_favorite_movies(username)
        comment_list = self.comment_controller.get_comments_by_username(username)
        user_info = {
            "username": username,
            "email": user.email if user else None,
            "favorite_movies": favorite_movies,
            "comments": [{comment.movie_id: comment.comment} for comment in comment_list]
        }
        return user_info

    
if __name__ == "__main__":
    from db.clients import get_db
    db = next(get_db())
    user_service = UserService(db)
    # Example usage
    print(user_service.add_favorite_movie("test_user", "tt1234567"))
    print(user_service.get_favorite_movies("test_user"))
    print(user_service.remove_favorite_movie("test_user", "tt1234567"))
    print(user_service.get_user_info("test_user"))
    print(user_service.recommend_movies("test_user"))