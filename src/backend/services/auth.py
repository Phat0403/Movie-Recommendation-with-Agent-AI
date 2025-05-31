from core.auth import create_access_token, get_password_hash, verify_password, email_validation, password_validation, send_email_verification, get_username_from_token, decode_token
from db.crud_user import UserController
from db.redis_client import RedisClient
from db.clients import get_db
from models.user import User

import logging

class AuthService:
    def __init__(self, user_controller: UserController):
        self.user_controller = user_controller

    def get_current_user(self, token: str):
        if token is None or token == "":
            return {"error": "Token is required", "status": 400}
        username = get_username_from_token(token)
        if username is None:
            return {"error": "Invalid token", "status": 401}
        db_user = self.user_controller.get(User, username=username)
        if db_user is None:
            return {"error": "User not found", "status": 404}
        return db_user
    
    async def send_register_otp_email(self, username: str, password: str, email: str = None, redis_client: RedisClient = None):
        """
        Initialize the registration process for a new user.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.

        Returns:
            dict: A dictionary containing the status and message.
        """
        if self.user_controller.check_user_exists(username):
            return {"error": "User already exists", "status": 400}
        if username is None or username == "":
            return {"error": "Username is required", "status": 400}
        if email is None or email == "":
            return {"error": "Email is required", "status": 400}
        if password is None or password == "":
            return {"error": "Password is required", "status": 400}
        if not password_validation(password):
            return {"error": "Password must be at least 8 characters long and contain letters and numbers", "status": 400}
        if not email_validation(email):
            return {"error": "Invalid email format", "status": 400}
        response = send_email_verification(email)
        otp_code = response.get("code")
        if response.get("status") != 200:
            logging.error(f"Failed to send verification email: {response.get('message')}")
            return {"error": "Failed to send verification email", "status": response.get("status", 500)}
        if otp_code is None:
            return {"error": "Failed to send verification email", "status": 500}
        if redis_client is None:
            return {"error": "Redis client is required", "status": 400}
        # Store the OTP code in Redis with a 10-minute expiration
        logging.warning(f"Storing registration code for {username} in Redis")
        await redis_client.set(f"registration_code:{username}", otp_code, expire=600)
        await redis_client.set(f"registration_code:{username}_password", password, expire=600)
        await redis_client.set(f"registration_code:{username}_email", email, expire=600)

        return {"message": "Registration initialized successfully", "status": 200}
    
    async def register(self, otp: str, username: str = None, redis_client: RedisClient = None):
        """
        Register a new user in the database.

        Args:
            db: Database session.
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User: The created user object.
        """
        if redis_client is None:
            return {"error": "Redis client is required", "status": 400}
        redis_code = await redis_client.get(f"registration_code:{username}")
        if redis_code is None:
            return {"error": "Invalid or expired registration code", "status": 400}
        if redis_code != otp:
            return {"error": "Invalid registration code", "status": 400}
        # Retrieve the password and email from Redis
        password = await redis_client.get(f"registration_code:{username}_password")
        email = await redis_client.get(f"registration_code:{username}_email")
        await redis_client.delete(f"registration_code:{username}")
        await redis_client.delete(f"registration_code:{username}_password")
        await redis_client.delete(f"registration_code:{username}_email")

        
        hashed_password = get_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email, is_admin=False)
        try:
            self.user_controller.create(new_user)
        except Exception as e:
            logging.error(f"Failed to register user: {e}")
            return {"error": "Failed to register user", "status": 500}

        return {"message": "User registered successfully", "status": 201}
    async def resend_registration_otp(self, username: str, redis_client: RedisClient):
        """
        Resend the registration OTP to the user's email.

        Args:
            username (str): The username of the user.
            redis_client (RedisClient): The Redis client instance.

        Returns:
            dict: A dictionary containing the status and message.
        """
        if redis_client is None:
            return {"error": "Redis client is required", "status": 400}
        
        email = await redis_client.get(f"registration_code:{username}_email")
        if email is None:
            return {"error": "User have not initiated registration", "status": 400}
        
        response = send_email_verification(email)
        otp_code = response["code"]
        if response["status"] != 200:
            logging.error(f"Failed to resend verification email: {response.get('message')}")
            return {"error": "Failed to send verification email", "status": response.get("status", 500)}
        
        if otp_code is None:
            return {"error": "Failed to send verification email", "status": 500}
        
        await redis_client.set(f"registration_code:{username}", otp_code, expire=600)
        await redis_client.set(f"registration_code:{username}_email", email, expire=600)
        password = await redis_client.get(f"registration_code:{username}_password")
        await redis_client.set(f"registration_code:{username}_password", password, expire=600)

        return {"message": "Registration OTP resent successfully", "status": 200}
    def login(self, username: str, password: str):
        """
        Login a user and return an access token.

        Args:
            db: Database session.
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            str: Access token if login is successful, otherwise an error message.
        """
        
        db_user = self.user_controller.check_user_exists(username)
        if not db_user:
            return {"error": "User does not exist", "status": 404}
        
        user = self.user_controller.get(User, username=username)
        
        if not verify_password(password, user.password):
            return {"error": "Incorrect password", "status": 401}

        access_token = create_access_token(data={"username": username, "admin": user.is_admin})
        return {"access_token": access_token, "token_type": "bearer", "status": 200}

    def change_password(self, username: str, old_password: str, new_password: str):
        """
        Change the password of a user.

        Args:
            db: Database session.
            username (str): The username of the user.
            old_password (str): The old password of the user.
            new_password (str): The new password of the user.

        Returns:
            str: Success message if password change is successful, otherwise an error message.
        """
        db_user = self.user_controller.check_user_exists(username)
        if db_user is None:
            return {"error": "User does not exist", "status": 404}

        if not verify_password(old_password, db_user.password):
            return {"error": "Incorrect old password", "status": 401}

        if old_password == new_password:
            return {"error": "New password cannot be the same as old password", "status": 400}
        
        if not password_validation(new_password):
            return {"error": "New password must be at least 8 characters long and contain letters and numbers", "status": 400}
        
        hashed_new_password = get_password_hash(new_password)
        
        old_password_user = self.user_controller.get(User, username=username)
        new_password_user = self.user_controller.update(
            old_password_user,
            password=hashed_new_password
        )
        if new_password_user is None:
            return {"error": "Failed to change password", "status": 500}
        return {"message": "Password changed successfully", "status": 200}
    
    async def send_password_reset_email(self, redis_client: RedisClient, username: str):
        """
        Send a password reset email to the user.

        Args:
            db: Database session.
            email (str): The email of the user.

        Returns:
            str: Success message if email is sent, otherwise an error message.
        """
        user_existed = self.user_controller.check_user_exists(username)
        if user_existed:
            db_user = self.user_controller.get(User, username=username)
        else:
            return {"error": "User does not exist", "status": 404}
        
        email = db_user.email
        response = send_email_verification(email)
        
        if response["status"] != 200:
            return {"error": "Failed to send email", "status": response["status"]}
        
        code = response["code"]
        await redis_client.set(f"recovery_code:{db_user.username}", code, expire=600)
        
        return {"message": "Password reset email sent successfully", "status": 200}
    
    async def verify_password_reset_code(self, redis_client: RedisClient, username: str, code: str):
        """
        Verify the password reset code.

        Args:
            db: Database session.
            username (str): The username of the user.
            code (str): The password reset code.

        Returns:
            str: Success message if code is valid, otherwise an error message.
        """
        if username is None or username == "":
            return {"error": "Username is required", "status": 400}
        if code is None or code == "":
            return {"error": "Code is required", "status": 400}
        
        redis_code = await redis_client.get(f"recovery_code:{username}")
        
        if redis_code is None:
            return {"error": "Invalid or expired code", "status": 400}
        
        if redis_code != code:
            return {"error": "Invalid code", "status": 400}
        
        return {"message": "Code verified successfully", "status": 200}
    
    def reset_password(self, username: str, new_password: str):
        """
        Reset the password of the user.

        Args:
            db: Database session.
            username (str): The username of the user.
            new_password (str): The new password of the user.

        Returns:
            str: Success message if password reset is successful, otherwise an error message.
        """
        db_user = self.user_controller.check_user_exists(username)
        if db_user is None:
            return {"error": "User does not exist", "status": 404}

        if not password_validation(new_password):
            return {"error": "New password must be at least 8 characters long and contain letters and numbers", "status": 400}
        
        hashed_new_password = get_password_hash(new_password)
        old_password_user = self.user_controller.get(User, username=username)
        new_password_user = self.user_controller.update(
            old_password_user,
            password=hashed_new_password
        )
        if new_password_user is None:
            return {"error": "Failed to reset password", "status": 500}
        
        return {"message": "Password reset successfully", "status": 200}

async def test_send_password(db, username: str):
    """
    Send a password reset email to the user.

    Args:
        email (str): The email of the user.

    Returns:
        str: Success message if email is sent, otherwise an error message.
    """
    redis_client = RedisClient()
    user_controller = UserController(db)
    auth_service = AuthService(user_controller)
    response = await auth_service.send_password_reset_email(redis_client, username)
    return response

async def test_verify_password_reset_code(db, username: str, code: str):
    """
    Verify the password reset code.

    Args:
        username (str): The username of the user.
        code (str): The password reset code.

    Returns:
        str: Success message if code is valid, otherwise an error message.
    """
    redis_client = RedisClient()
    user_controller = UserController(db)
    auth_service = AuthService(user_controller)
    response = await auth_service.verify_password_reset_code(redis_client, username, code)
    return response


if __name__ == "__main__":
    # from db.session import get_db,engine
    db = next(get_db())
    import asyncio
    res = asyncio.run(test_verify_password_reset_code(db,"abc12345","655380"))
    print(res)
    # user_controller = UserController(db)
    # auth_service = AuthService(user_controller)
    # Example usage
    # Register a normal user
    # from models.user import User
    # User.metadata.create_all(bind=engine)
    # res = auth_service.register_user("abc12345", "PNmk@0811", "pnmk0811@gmail.com")
    # print(res)
    # jwt = login_user(self.user_controller, "testuser", "testpassword")
    # print(jwt)
    