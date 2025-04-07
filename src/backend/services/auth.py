from core.auth import create_access_token, get_password_hash, verify_password
from db.crud_user import UserController

def register_normal_user(user_controller: UserController, username: str, password: str):
    """
    Register a new user in the database.

    Args:
        db: Database session.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        User: The created user object.
    """
    if user_controller.check_user_exists(username):
        return "User already exists"

    hashed_password = get_password_hash(password)
    user = user_controller.create_normal_user(username, hashed_password)

    return user

def register_admin_user(user_controller: UserController, username: str, password: str):
    """
    Register a new admin user in the database.

    Args:
        db: Database session.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        User: The created admin user object.
    """
    if user_controller.check_user_exists(username):
        return "User already exists"

    hashed_password = get_password_hash(password)
    user = user_controller.create_admin_user(username, hashed_password)
    return user

def login_user(user_controller: UserController, username: str, password: str):
    """
    Login a user and return an access token.

    Args:
        db: Database session.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        str: Access token if login is successful, otherwise an error message.
    """
    db_user = user_controller.check_user_exists(username)
    if db_user is None:
        return "User does not exist"

    if not verify_password(password, db_user.password):
        return "Incorrect password"

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    from db.session import get_db,engine
    db = next(get_db())
    user_controller = UserController(db)
    # Example usage
    # Register a normal user
    from models.user import User
    User.metadata.create_all(bind=engine)
    res = register_normal_user(user_controller, "abc12345", "testpassword")
    print(res)
    # jwt = login_user(user_controller, "testuser", "testpassword")
    # print(jwt)