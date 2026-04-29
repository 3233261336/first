from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class TestPlan:
    objective: str
    scenarios: List[str]
    generated_cases: List[str]


class TestGenAgent:
    """根据变更摘要生成测试计划（MVP 规则版，可替换为 LLM）。"""

    def generate_plan(self, change_summary: str) -> TestPlan:
        summary = (change_summary or "").strip()
        if not summary:
            summary = "常规回归测试"

        scenarios: List[str] = [
            "正常路径验证",
            "边界值与异常输入",
            "历史缺陷回归",
        ]

        generated_cases: List[str] = [
            f"基于变更摘要生成的冒烟用例: {summary}",
            "参数为零、空值、负值时的行为",
            "错误输入时是否抛出明确异常",
        ]

        return TestPlan(
            objective=f"验证变更的正确性与稳定性: {summary}",
            scenarios=scenarios,
            generated_cases=generated_cases,
        )
