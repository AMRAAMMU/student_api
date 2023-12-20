#student.py
from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, schemas, oauth2
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..repository import student_user

router = APIRouter(
    prefix="/Users",
    tags=['Users']
)
@router.get('/Get all Users')
def get_all(db: Session = Depends(database.get_db),
             current_user: schemas.User_student = Depends(oauth2.get_current_user)):
    return student_user.get_all_user(db)

@router.post('/User', status_code=status.HTTP_201_CREATED)
def create(request: schemas.User_student, db: Session = Depends(database.get_db),
            current_user: schemas.User_student = Depends(oauth2.get_current_user)):
    return student_user.create_user(request, db)

@router.get('/user/{id}', response_model=schemas.show_user, status_code=200)
def show_student_user(id: int, db: Session = Depends(database.get_db),
                       current_user: schemas.User_student = Depends(oauth2.get_current_user)):
    return student_user.show(id, db)
