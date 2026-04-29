from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict

from agents.rca_fix_agent import RcaFixAgent
from agents.test_gen_agent import TestGenAgent
from agents.test_run_agent import TestRunAgent


@dataclass
class PipelineInput:
    change_summary: str
    test_path: str = "sample_app/tests"
    rerun_after_rca: bool = True


class PipelineOrchestrator:
    def __init__(self) -> None:
        self.test_gen_agent = TestGenAgent()
        self.test_run_agent = TestRunAgent()
        self.rca_fix_agent = RcaFixAgent()

    def run(self, payload: PipelineInput) -> Dict[str, Any]:
        plan = self.test_gen_agent.generate_plan(payload.change_summary)
        first_run = self.test_run_agent.run_tests(payload.test_path)

        output: Dict[str, Any] = {
            "test_plan": asdict(plan),
            "first_run": {
                "success": first_run.success,
                "passed": first_run.passed,
                "failed": first_run.failed,
                "errors": first_run.errors,
                "exit_code": first_run.exit_code,
            },
            "rca_report": None,
            "second_run": None,
            "note": "MVP 默认只给修复建议，不自动改代码。",
        }

        if first_run.success:
            output["note"] = "测试首次通过，无需 RCA。"
            return output

        rca = self.rca_fix_agent.analyze_failures(first_run)
        output["rca_report"] = asdict(rca)

        if payload.rerun_after_rca:
            second_run = self.test_run_agent.run_tests(payload.test_path)
            output["second_run"] = {
                "success": second_run.success,
                "passed": second_run.passed,
                "failed": second_run.failed,
                "errors": second_run.errors,
                "exit_code": second_run.exit_code,
            }

        return output
