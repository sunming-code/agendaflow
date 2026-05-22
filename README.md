# AgendaFlow

AgendaFlow is a lightweight multi-agent reasoning runner inspired by meeting-style deliberation. Given a user task, it selects a reasoning protocol, creates complementary agent roles, runs a phased discussion, synthesizes intermediate artifacts, and produces a final answer.

## Features

- Interactive command-line runner
- Configurable API key, API base URL, model name, and role count
- Automatic protocol selection
- Role generation for complementary reasoning perspectives
- Four-phase structured deliberation
- Phase-level artifact synthesis
- Final answer generation from completed artifacts
- JSON result persistence

## Protocols

AgendaFlow can route a task to one of four protocols:

- `planning`: for plans, schedules, action sequences, and arrangements
- `problem_solving`: for diagnosing problems and proposing fixes
- `verification`: for reasoning over rules, evidence, claims, or internal consistency
- `decision_selection`: for choosing among options under criteria or constraints

If routing is uncertain, the runner defaults to `problem_solving`.

## Project Structure

```text
.
+-- AGENDAFLOW/
|   +-- __init__.py
|   +-- llm.py
|   +-- models.py
|   +-- prompts.py
|   +-- protocols.py
|   +-- runner.py
|   +-- storage.py
+-- config.py
+-- requirements.txt
+-- run_agendaflow.py
+-- README.md
```

## Installation

```powershell
pip install -r requirements.txt
```

## Configuration

The interactive runner asks for:

- API key
- API base URL
- Model name
- Role count, from 2 to 8, default `4`

You can also provide defaults through environment variables:

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

Example:

```text
AgendaFlow lightweight runner
--------------------------------
API key:
API base URL [https://api.example.com/v1]:
Model name [your-model-name]:
Role count (2-8, optional) [4]:

Enter your problem/task. Finish with an empty line:
Our production service has intermittent timeout spikes. Diagnose likely causes and recommend a fix plan.
```

The runner prints:

- Selected protocol
- Generated roles
- Phase artifacts
- Final answer
- Saved result path

## Output

Each run saves a JSON file under `agendaflow_results/`.

The saved result includes:

- `task`
- `protocol`
- `routing_justification`
- `roles`
- `phase_artifacts`
- `unresolved_issues`
- `final_answer`
- `transcript`

## Development Check

```powershell
python -m compileall .
```
