from sqlalchemy import Column, Integer, String, Boolean, UUID, VARCHAR
from db.session import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(VARCHAR(50), unique=True, index=True)
    password = Column(VARCHAR(255))
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, is_admin={self.is_admin})>"