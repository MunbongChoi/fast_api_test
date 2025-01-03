from fastapi import FastAPI, Depends
from src.auth.routers import router as auth_router
from src.gpt.routers import router as gpt_router
from src.file.routers import router as file_router
from src.chat.routers import router as chat_router
from src.commands.analysis import run_analysis_command
from src.commands.visualization import run_visualization_command
from src.db.models import Base
from src.db.database import engine
from src.auth.dependencies import get_current_user
from prometheus_fastapi_instrumentator import Instrumentator

# DB 테이블이 없으면 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MyService",
    description="""
    - 사용자 인터페이스: 웹에서 CSV/SHAPE 업로드, ChatGPT 대화형 UI, compas-v 시각화 대시보드 연동
    - 백엔드 계층: 파일 스토리지, 분석/처리 레이어, LLM API 연동
    - 인증/보안: OAuth2, HTTPS(SSL), 파일 접근 제어
    - 옵션: Redis/Memcached 캐시, Grafana/Prometheus 모니터링, Elastic Stack 로깅
    """,
    version="0.2.0",
)

# 라우터 등록
app.include_router(auth_router)
app.include_router(gpt_router)
app.include_router(file_router)
app.include_router(chat_router)

# Prometheus 모니터링 초기화
Instrumentator().instrument(app).expose(app, include_in_schema=False)

# (선택) 예: 분석명령, 시각화명령을 직접 API로 노출
@app.post("/analysis")
def analysis_command(params: dict, current_user=Depends(get_current_user)):
    result = run_analysis_command(params)
    return {"analysis_result": result, "user": current_user.username}

@app.post("/visualization")
def visualization_command(params: dict, current_user=Depends(get_current_user)):
    result = run_visualization_command(params)
    return {"visualization_result": result, "user": current_user.username}
