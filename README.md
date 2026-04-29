# Multi-Agent Test Factory (MVP)

一个可运行的最小实现：
- `TestGenAgent`：基于代码变更描述生成测试计划
- `TestRunAgent`：执行 `pytest` 并解析结果
- `RcaFixAgent`：对失败信息做根因分析并给出修复建议
- `PipelineOrchestrator`：串联“生成 -> 执行 -> 诊断 -> 二次验证”闭环

## 1. 环境要求

- Python 3.11+
- Windows / macOS / Linux

## 2. 安装依赖

```bash
pip install -r requirements.txt
```

## 3. 启动 API

```bash
uvicorn app:app --reload
```

启动后访问：
- 健康检查：`GET http://127.0.0.1:8000/health`
- 触发流水线：`POST http://127.0.0.1:8000/pipeline/run`

## 4. 触发示例

```bash
curl -X POST http://127.0.0.1:8000/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{
    "change_summary": "新增 Calculator.divide()，需要补充除零和负数边界测试",
    "test_path": "sample_app/tests",
    "rerun_after_rca": true
  }'
```

## 5. 项目结构

```text
multi-agent-test-factory/
  app.py
  requirements.txt
  agents/
    test_gen_agent.py
    test_run_agent.py
    rca_fix_agent.py
  pipeline/
    orchestrator.py
  sample_app/
    calculator.py
    tests/
      test_calculator.py
```

## 6. 如何接入真实大模型

你可以在 `agents/test_gen_agent.py` 与 `agents/rca_fix_agent.py` 中替换当前规则逻辑：
- 把 `generate_plan()` 改成调用 LLM 生成结构化测试计划
- 把 `analyze_failures()` 改成基于日志 + stacktrace 的 RCA Prompt

建议输出 JSON schema，保证流水线可稳定消费。

## 7. GitHub 上传建议

```bash
git init
git add .
git commit -m "feat: init multi-agent test factory mvp"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## 8. 打包

项目根目录执行：

```bash
powershell -ExecutionPolicy Bypass -File .\scripts\package.ps1
```

会生成：`multi-agent-test-factory.zip`
