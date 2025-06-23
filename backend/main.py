import os

from app.services.pdf_service import url_to_pdf_sync
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, HttpUrl

app = FastAPI(
    title="WeDocX API",
    description="API for WeDocX to process URLs into PDFs.",
    version="0.1.0",
)


class ProcessUrlRequest(BaseModel):
    url: HttpUrl
    email: EmailStr


@app.get("/")
async def read_root():
    """
    Root endpoint to check API status.
    """
    return {"status": "ok", "message": "Welcome to WeDocX API!"}


@app.post("/api/v1/process-url")
async def process_url(request: ProcessUrlRequest):
    """
    接收用户提交的URL和目标邮箱，调用PDF转换服务。
    """
    try:
        pdf_path = url_to_pdf_sync(request.url)
        filename = os.path.basename(pdf_path)
        return {"status": "success", "pdf_file": filename, "pdf_path": pdf_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF转换失败: {e}")
