from fastapi import APIRouter, Depends
from src.auth.dependencies import get_current_user
from sqlalchemy.orm import Session
from src.db.database import get_db

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post("/message")
def send_message(message: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    DB에 대화 로그 저장, GPT 호출, 기타 로직 가능
    """
    # 예) 대화 로그 저장
    # db_chat = ChatModel(user_id=current_user.id, message=message)
    # db.add(db_chat)
    # db.commit()
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "message": message,
        "reply": "이곳에 GPT나 기타 로직의 응답"
    }
