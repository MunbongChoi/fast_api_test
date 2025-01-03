from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from src.file.storage import save_file, get_file
from src.auth.dependencies import get_current_user
import os

router = APIRouter(
    prefix="/file",
    tags=["file"]
)

@router.post("/upload")
def upload_file(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    """
    CSV, SHAPE 등 다양한 형식 업로드 가능.
    업로드된 파일에 대해 접근 제어(권한) 로직을 추가할 수 있음.
    """
    content = file.file.read()

    # MIME 타입 체크, 확장자 검사 등 가능
    # ex) if file.content_type not in ["text/csv", "application/octet-stream", ...]:
    #         raise HTTPException(status_code=400, detail="Invalid file type")

    saved_path, filename = save_file(content, file.filename)
    return {
        "message": "File uploaded",
        "filename": filename,
        "saved_path": saved_path,
        "uploaded_by": current_user.username
    }

@router.get("/download")
def download_file(filename: str, current_user=Depends(get_current_user)):
    """
    실제 운영 환경에서는 파일 권한/소유자 체크 등이 필요할 수 있음.
    """
    file_path = f"uploaded_files/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    file_content = get_file(file_path)
    # 단순히 파일 내용을 JSON으로 반환 (실제는 StreamingResponse 등으로)
    return {
        "filename": filename,
        "content": file_content
    }
