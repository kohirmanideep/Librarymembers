from sqlalchemy import Column,Integer,String,VARCHAR, BigInteger
from database import Base

class Member(Base):
    __tablename__="members"
    
    member_id = Column(Integer,primary_key=True,index=True)
    name = Column(VARCHAR(300))
    email=Column(VARCHAR(300),unique=True)
    phone_number = Column(BigInteger())
    password = Column(VARCHAR(300))
    
    

    