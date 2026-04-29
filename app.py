from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from pipeline.orchestrator import PipelineInput, PipelineOrchestrator

app = FastAPI(title="Multi-Agent Test Factory", version="0.1.0")
orchestrator = PipelineOrchestrator()


class PipelineRequest(BaseModel):
    change_summary: str = Field(..., description="代码变更摘要")
    test_path: str = Field(default="sample_app/tests", description="pytest 目标路径")
    rerun_after_rca: bool = Field(default=True, description="RCA 后是否二次运行")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/pipeline/run")
def run_pipeline(req: PipelineRequest) -> dict:
    payload = PipelineInput(
        change_summary=req.change_summary,
        test_path=req.test_path,
        rerun_after_rca=req.rerun_after_rca,
    )
    return orchestrator.run(payload)
