from models.user import User


class UserController:
    def __init__(self, db):
        self.db = db
        
    def check_user_exists(self, username: str):
        """
        Check if a user exists in the database.

        Args:
            db: Database session.
            username (str): The username to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, username: str, password: str, email: str = None, is_admin: bool = False):
        """
        Create a new user in the database.

        Args:
            db: Database session.
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User: The created user object.
        """
        db_user = User(username=username, password=password, email=email, is_admin=is_admin)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, user_name: str):
        """
        Get a user by username.

        Args:
            db: Database session.
            user_name (str): The username of the user.

        Returns:
            User: The user object if found, None otherwise.
        """
        return self.db.query(User).filter(User.username == user_name).first()


    def delete_user(self, user_name: str):
        """
        Delete a user by username.

        Args:
            db: Database session.
            user_name (str): The username of the user to delete.

        Returns:
            bool: True if the user was deleted, False otherwise.
        """
        db_user = self.db.query(User).filter(User.username == user_name).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
    
    def update_password(self, user_name: str, new_password: str):
        """
        Update the password of a user.

        Args:
            db: Database session.
            user_name (str): The username of the user.
            new_password (str): The new password for the user.

        Returns:
            User: The updated user object if successful, None otherwise.
        """
        db_user = self.db.query(User).filter(User.username == user_name).first()
        if db_user:
            db_user.password = new_password
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        return None