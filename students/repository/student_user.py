#students_user.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import User
from ..hashing import Hash

def get_all_user(db: Session):
    users = db.query(User).all()
    return users

def create_user(request, db: Session):
    new_student_user = User(name=request.name, email=request.email, password=Hash.bcrypt(request.password),
                            age=request.age, department=request.department)
    db.add(new_student_user)
    db.commit()
    db.refresh(new_student_user)
    return new_student_user

def show(id: int, db: Session):
    get_result = db.query(User).filter(User.id == id).first()
    if not get_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')
    return get_result

 