# AgendaFlow Lightweight Runner

这是一个轻量版 AgendaFlow 多智能体推理系统。它的目标是让用户输入一个 problem/task 后，系统能够自动选择推理流程、生成角色、组织多阶段讨论，并输出最终答案。

当前实现以“能跑通”和“结构上贴近论文思想”为优先目标，不追求完整复现论文中的提示词、协议表格或实验框架。

## Features

- 交互式输入 API key、API base URL、模型名称、角色数量和任务正文
- 自动选择推理协议：
  - `planning`
  - `problem_solving`
  - `verification`
  - `decision_selection`
- 自动生成 2 到 8 个功能角色，默认 4 个
- 每个协议按 4 个阶段顺序执行
- 每阶段收集角色贡献并生成阶段产物
- 最终答案只基于阶段产物生成
- 自动保存运行结果到 `agendaflow_results/`

## Project Structure

```text
.
├── AGENDAFLOW/
│   ├── __init__.py
│   ├── llm.py          # Minimal LLM factory and retry helper
│   ├── models.py       # Pydantic data models
│   ├── prompts.py      # Lightweight prompt templates
│   ├── protocols.py    # Small protocol phase templates
│   ├── runner.py       # Main AgendaFlow execution flow
│   └── storage.py      # JSON result persistence
├── config.py           # Default runtime configuration
├── requirements.txt
├── run_agendaflow.py   # Interactive CLI entrypoint
└── README.md
```

## Installation

```powershell
pip install -r requirements.txt
```

## Configuration

运行时会交互式询问以下配置：

- API key
- API base URL
- 模型名称
- 角色数量，可选，默认 `4`

如果直接回车，会使用 `config.py` 中的默认值。也可以通过环境变量覆盖默认配置：

```powershell
$env:OPENAI_API_KEY="your-api-key"
$env:OPENAI_API_BASE="https://api.example.com/v1"
$env:MODEL_NAME="your-model-name"
$env:LLM_TIMEOUT_SECONDS="60"
```

## Usage

```powershell
python run_agendaflow.py
```

示例交互：

```text
AgendaFlow lightweight runner
--------------------------------
API key:
API base URL [https://api.moonshot.cn/v1]:
Model name [kimi-k2-turbo-preview]:
Role count (2-8, optional) [4]:

Enter your problem/task. Finish with an empty line:
我们的线上服务最近间歇性超时，请分析可能原因并给出修复方案。

```

程序会输出：

- selected protocol
- generated roles
- phase artifacts
- final answer
- saved result path

## Output

每次运行会保存一个 JSON 文件到 `agendaflow_results/`，主要字段包括：

- `task`
- `protocol`
- `routing_justification`
- `roles`
- `phase_artifacts`
- `unresolved_issues`
- `final_answer`
- `transcript`

## Design Notes

当前版本已经移除了旧 EasyMeeting 代码中的复杂产品功能，包括：

- 13 类真实会议类型
- fact checker
- Tavily / arXiv / RAG / embedding 检索
- Belbin 团队角色分析
- 人工插话
- 会议确认 checklist

这版代码只保留一个集中、可运行的 AgendaFlow 核心流程。

## Quick Check

```powershell
python -m compileall .
```

如果需要确认旧模块没有残留引用，可以运行：

```powershell
rg "fact_checker|Tavily|arxiv|KnowledgePreloader|Belbin|MEETING_TYPES|STEP_0|RAG|embedding"
```
