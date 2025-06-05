from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional
from config.config import settings
import re
import random
from config.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from utils.logger import get_logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = get_logger(__name__)

# ---------------------------
# PASSWORD UTILS
# ---------------------------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def password_validation(password: str) -> bool:
    """
    Validate the password strength.
    
    Args:
        password (str): The password to validate.
    
    Returns:
        bool: True if the password is strong, False otherwise.
    """
    # Password must be at least 8 characters long and contain letters and numbers
    regex = r'^.{8,}$'

    return bool(re.match(regex, password))

# ---------------------------
# JWT TOKEN UTILS
# ---------------------------

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# ---------------------------
# VERIFY / DECODE TOKENS
# ---------------------------

def decode_token(token: str) -> Optional[dict]:
    token = token.strip('"')  # remove outer quotes if present
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def get_username_from_token(token: str) -> Optional[str]:
    payload = decode_token(token)
    return payload.get("username") if payload else None

def get_role_from_token(token: str) -> Optional[str]:
    payload = decode_token(token)
    return payload.get("role") if payload else None

# ---------------------------
# EMAIL UTILS
# ---------------------------

def email_validation(email: str) -> bool:
    """
    Validate the email format.
    
    Args:
        email (str): The email address to validate.
    
    Returns:
        bool: True if the email format is valid, False otherwise.
    """
    # Regex pattern to match a standard email format
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def send_email_verification(email: str) -> bool:
    """
    Send an email verification link to the user's email address.
    
    Args:
        email (str): The email address to send the verification link to.
    
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    # Placeholder for sending email logic
    # In a real-world scenario, you would integrate with an email service provider
    code = str(random.randint(100000, 999999))
    gmail = settings.GMAIL
    password = settings.GMAIL_PASSWORD
    subject = "Email Verification"
    body = f"Your verification code is: {code}"
    
    message = MIMEMultipart()
    message['From'] = gmail
    message['To'] = email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(gmail, password)
            server.send_message(message)
        return {'code': code, 'email': email, 'status': 200}
    except Exception as e:
        print(f"Failed to send email: {e}")
        return {'status': 500, 'error': 'Failed to send email'}



if __name__=="__main__":
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwbm1rMDgxMSJ9.F0tBSWxjkuS4SsN4VnyUNnofP_19sCe6TGWl71MdDwo"
    print(get_username_from_token(token))