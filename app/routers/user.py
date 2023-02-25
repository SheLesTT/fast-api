
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal, get_db
from .. import models, schemas, utiles
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine, SessionLocal, get_db


router = APIRouter(
    prefix='/user',
    tags = ["User"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):


    user.password = utiles.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user.__dict__

@router.get('/{id}', response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does't exist")
    return user.__dict__
