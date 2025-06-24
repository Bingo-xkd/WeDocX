import os
import traceback

from app.services.pdf_service import url_to_pdf_sync
from app.workers.tasks import create_pdf_task, send_email_task
from celery import chain
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
    接收用户提交的URL和目标邮箱，调用PDF转换服务（异步任务链）。
    """
    try:
        # 生成输出文件名
        filename = None
        pdf_output_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "output")
        )
        os.makedirs(pdf_output_dir, exist_ok=True)
        # 这里简单用url最后一段+时间戳
        from datetime import datetime

        now_str = datetime.now().strftime("%Y%m%d-%H-%M-%S")
        base_name = str(request.url).split("/")[-1][:10] or "file"
        pdf_filename = f"{now_str}-{base_name}.pdf"
        pdf_path = os.path.join(pdf_output_dir, pdf_filename)

        # 任务链：先生成PDF，再发邮件
        task_chain = chain(
            create_pdf_task.s(str(request.url), pdf_path),
            send_email_task.s(
                str(request.email),
                "网页转PDF",
                f"请查收由WeDocX生成的PDF文件：{pdf_filename}",
            ),
        )
        result = task_chain.apply_async()
        return {
            "status": "success",
            "task_id": str(result.id),
            "pdf_file": pdf_filename,
        }
    except Exception as e:
        print("API端点异常:", e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"任务提交失败: {e}")
