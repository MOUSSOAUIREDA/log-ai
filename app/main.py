
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.summary_request import SummaryRequest
from app.models.chat_request import ChatRequest
from app.celery_app import celery_app
from celery.result import AsyncResult
from app.services.summary_service import summary
from app.services.chat_service import handle_question


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI()


# ============================================================
# CORS
# Permet à Vue.js (localhost:5173) de communiquer
# avec FastAPI (localhost:8001)
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# SUMMARY
# ============================================================

@app.post("/summary")
def summary_request(request: SummaryRequest):

    source_id = request.source_id
    requested_date = request.requested_date

    task = summary.delay(source_id, requested_date)

    return {
        "id": task.id,
        "message": "Task sent"
    }


# ============================================================
# TASK STATUS
# ============================================================

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):

    task = AsyncResult(
        task_id,
        app=celery_app
    )

    return {
        "task_id": task.id,
        "status": task.status,
        "result": str(task.result)
    }


# ============================================================
# CHAT
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    return handle_question(request.question)

