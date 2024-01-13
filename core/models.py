from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# base.py에서 생성한 Base import
from base import Base

# Base를 상속 받아 SQLAlchemy model 생성
class User(Base):
    # 해당 모델이 사용할 table 이름 지정
    __tablename__ = "users"

    # Model의 attribute(column) 생성 -> "="를 사용하여 속성을 정의
    email = Column(String, primary_key=True, index=True)
    username= Column(String, index=True)