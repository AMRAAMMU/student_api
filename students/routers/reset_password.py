# reset_password.py
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import EmailStr
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(
    prefix="/Password_Reset",
    tags=['Password_Reset']
)

@router.post('/')
def password_reset(email: EmailStr, db: Session = Depends(database.get_db)):
    student = db.query(models.User).filter(models.User.email == email).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credential")

    # Check if there is an existing token for the user
    existing_token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.email == email).first()

    if existing_token:
        # Display the existing token without creating a new one
        return {"access_token": existing_token.token, "token_type": "bearer"}
    else:
        # Create a new token and insert it into the database
        access_token = token.create_access_token(data={"sub": student.email})
        reset_token = models.PasswordResetToken(email=email, token=access_token)
        db.add(reset_token)
        db.commit()
        db.refresh(reset_token)
        return {"access_token": access_token, "token_type": "bearer"}

@router.put('/', status_code=status.HTTP_202_ACCEPTED)
def update(token: str, email: str, request: schemas.ps, db: Session = Depends(database.get_db)):
    up = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token).first()
    st = db.query(models.User).filter(models.User.email == email).first()
    if not up:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with the token is not available")
    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and confirm password do not match"
        )
    hashed_password = Hash.bcrypt(request.password)
    
    if st:
        st.password = hashed_password
        st.confirm_password = hashed_password
        # db.delete(up)  # Remove the used token from the database
        db.commit()
        return {"message": "Password updated successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
