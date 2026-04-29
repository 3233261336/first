from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .test_run_agent import TestRunResult


@dataclass
class RcaReport:
    likely_causes: List[str]
    fix_suggestions: List[str]
    confidence: float


class RcaFixAgent:
    """根据测试输出做根因分析（MVP 规则版，可替换为 LLM）。"""

    def analyze_failures(self, result: TestRunResult) -> RcaReport:
        output = result.raw_output.lower()
        causes: List[str] = []
        fixes: List[str] = []
        confidence = 0.55

        if "zerodivisionerror" in output:
            causes.append("除零场景未被业务逻辑保护")
            fixes.append("在 divide 方法中对 b==0 做显式校验并抛出 ValueError")
            confidence = 0.85

        if "assert" in output:
            causes.append("断言与当前实现行为不一致")
            fixes.append("核对预期值与函数约定，修正实现或测试断言")
            confidence = max(confidence, 0.65)

        if not causes:
            causes.append("可能是边界输入处理不完整或测试数据覆盖不足")
            fixes.append("补充边界测试并检查异常分支")

        return RcaReport(
            likely_causes=causes,
            fix_suggestions=fixes,
            confidence=round(confidence, 2),
        )
