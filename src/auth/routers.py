from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.auth.dependencies import authenticate_user, create_access_token
from src.db.models import User
from src.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    # 단순 예시로, 중복 체크 후 생성
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered", "user_id": new_user.id}

@router.get("/oauth/{provider}")
def oauth_login(provider: str):
    # provider별 인증 URL로 리다이렉트하는 로직
    return {"msg": f"Redirecting to {provider} OAuth"}
