from fastapi import FastAPI,Depends
from numpy import append
import schemas,models
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from database import engine
from typing import List
from fastapi import status,HTTPException
from hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm
import Token,oauth2
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from jose import JWTError,jwt
from typing import Optional
import schemas
import Token

models.Base.metadata.create_all(engine)

app=FastAPI()

origins = [
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:3000/"
    "http://127.0.0.1:3000/",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:3000/Register",
    "http://localhost:3000/Register",
    "http://localhost:8000",
    "http://localhost:8000/members",
    "http://127.0.0.1:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post('/members',response_model=schemas.ShowMember,tags = ['members'])
def create_member(request:schemas.Member,db:Session=Depends(get_db)):
    new_member=models.Member(name=request.name,email=request.email,phone_number=request.phone_number,password=Hash.bcrypt(request.password))
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    db.close()
    return new_member



@app.post('/login',tags=['members'])
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    member=db.query(models.Member).filter(models.Member.email==form_data.username).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    if not Hash.verify(member.password,form_data.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    access_token = Token.create_access_token(data={"sub":member.email})
    return {"access_token":access_token,"token_type":"bearer"}

@app.post("/decoder", tags=['decoder'])
def verify_token(token:str, db:Session=Depends(get_db)):
        payload = jwt.decode(token, Token.SECRET_KEY, algorithms=[Token.ALGORITHM])
        email: str = payload.get("sub")  
        if email is None:
            raise HTTPException(status_code=404,detail="token not decoded")
        token_data = schemas.TokenData(email=email)
        return db.query(models.Member).filter(models.Member.email==email).first()
    
@app.get('/get/member/{member_id}',response_model=schemas.ShowMember,tags=['members'])
def get_member(member_id,db:Session=Depends(get_db),current_user:schemas.Member = Depends(oauth2.get_current_user)):
    member=db.query(models.Member).filter(models.Member.member_id).first()
    return member

@app.get('/member/',response_model=List[schemas.ShowMember],tags=['members'])
def get_member(db:Session=Depends(get_db),current_user:schemas.Member = Depends(oauth2.get_current_user)):
    member=db.query(models.Member).all()
    return member

@app.put('/members/{member_id}',status_code=status.HTTP_404_NOT_FOUND,tags = ['members'])
def create_member(member_id,request:schemas.Member,db:Session=Depends(get_db),current_user:schemas.Member = Depends(oauth2.get_current_user)):
    db.query(models.Member).filter(models.Member.member_id==member_id).update(request.dict)
    db.commit()
    return 'updated'

@app.delete('/members/{member_id}',status_code=status.HTTP_404_NOT_FOUND,tags = ['members'])
def create_member(member_id,db:Session=Depends(get_db),current_user:schemas.Member = Depends(oauth2.get_current_user)):
    db.query(models.Member).filter(models.Member.member_id==member_id).delete(synchronize_session=False)
    db.commit()
    return 'DONE'

    
    
    
    
    
    



   

    
