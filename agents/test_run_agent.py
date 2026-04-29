from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class TestRunResult:
    exit_code: int
    passed: int
    failed: int
    errors: int
    raw_output: str

    @property
    def success(self) -> bool:
        return self.exit_code == 0


class TestRunAgent:
    """执行 pytest 并提取结果。"""

    _RESULT_RE = re.compile(r"(\d+)\s+(passed|failed|error|errors)")

    def run_tests(self, test_path: str) -> TestRunResult:
        path = Path(test_path)
        cmd = [sys.executable, "-m", "pytest", str(path), "-q"]

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).resolve().parents[1],
            check=False,
        )

        output = (proc.stdout or "") + "\n" + (proc.stderr or "")

        passed = 0
        failed = 0
        errors = 0

        for count_str, label in self._RESULT_RE.findall(output):
            count = int(count_str)
            if label == "passed":
                passed += count
            elif label == "failed":
                failed += count
            elif label in {"error", "errors"}:
                errors += count

        return TestRunResult(
            exit_code=proc.returncode,
            passed=passed,
            failed=failed,
            errors=errors,
            raw_output=output.strip(),
        )
