from typing import Optional
from pydantic import BaseModel, PositiveInt

class Member(BaseModel):
    name:str
    email:str
    phone_number:PositiveInt
    password:str
   
    
class ShowMember(BaseModel):
    member_id:int
    name:str
    email:str
    phone_number:PositiveInt
    password:str
  
    class Config():
        orm_mode = True
        
        
class Book(BaseModel):
   
    Accessnumber:int
    Username:str
    Title:str
    Author:str
    Subject:str
    KeyWord:str
    bookcategory:str
    
    
class ShowBook(BaseModel):
   
    Accessnumber:int
    Username:str
    Title:str
    Author:str
    Subject:str
    KeyWord:str
    bookcategory:str
        
class Login(BaseModel):
    username:str
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    email:Optional[str]=None    