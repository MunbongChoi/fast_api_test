from fastapi import APIRouter, Depends
from src.gpt.openai_client import get_gpt_response
from src.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/gpt",
    tags=["gpt"]
)

@router.post("/completion")
def complete_prompt(prompt: str, current_user=Depends(get_current_user)):
    gpt_output = get_gpt_response(prompt)
    return {
        "prompt": prompt,
        "gpt_output": gpt_output,
        "user": current_user.username
    }
