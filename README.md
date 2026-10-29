# Multi-Agent AI System

A production-ready multi-agent AI system built from scratch, featuring three specialized agents orchestrated by a LangGraph supervisor, wrapped in a FastAPI backend, and fully containerized with Docker.

## What It Does

Users send a message to the system. The supervisor automatically routes it to the most appropriate agent based on intent — no need to select manually. Each agent is specialized and uses different tools to give the best possible response.

## Agents

### Data Analyst Agent

Analyzes CSV files and datasets using real Python execution via E2B sandbox. Runs actual pandas code, returns real results — not hallucinated analysis.

### Financial Analyst Agent

Researches stocks, markets, and investment opportunities using Tavily for live web search and E2B for calculations. Also accepts CSV files for financial data analysis.

### Business Debate Agent

Acts as a devil's advocate for business ideas. Debates the user's proposal, identifies risks, challenges assumptions, and forces critical thinking before committing to a decision.

## Architecture

```
User Message
     │
     ▼
┌─────────────────┐
│  LangGraph      │
│  Supervisor     │  ← Gemini flash-lite for routing
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Data   │ │Finance │ │Debate  │
│Analyst │ │Analyst │ │ Agent  │
└────────┘ └────────┘ └────────┘
    │           │
  E2B        Tavily
Sandbox      Search
```

## Tech Stack

| Layer | Technology |
| --- | --- |
| Agent Framework | LangChain AgentExecutor |
| Orchestration | LangGraph StateGraph |
| LLM (Agents) | Groq — Qwen 3.8B 27B |
| LLM (Routing) | Gemini flash-lite |
| Code Execution | E2B Sandbox |
| Web Search | Tavily |
| API | FastAPI + Uvicorn |
| Session Memory | Redis |
| Permanent Logging | PostgreSQL |
| Observability | LangSmith |
| Containerization | Docker + Docker Compose |

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/chat/supervisor` | Main endpoint — auto-routes to correct agent |
| POST | `/chat/analyst` | Direct access to Data Analyst |
| POST | `/chat/finance` | Direct access to Financial Analyst |
| POST | `/chat/debate` | Direct access to Business Debate Agent |
| GET | `/health` | Health check |

## Memory Architecture

- **Redis** — Short-term session memory. Agents remember conversation history within a 24-hour session window, enabling contextual multi-turn conversations.
- **PostgreSQL** — Permanent logging. Every message is logged with session ID, role, and timestamp for analytics and future eval datasets.

## Evals

Routing accuracy evaluated using LangSmith with a custom dataset of 11 test cases across all three agents.

- **Routing Accuracy: 82%**
- **Answer Quality: 0.75 avg**
- **Task Completion: 0.75 avg**
- 2 failures caused by Groq rate limits (free tier), not logic errors

## Running Locally

### Prerequisites

- Docker + Docker Compose
- Python 3.11+

### Setup

1. Clone the repo

```bash
git clone https://github.com/AbdulHai564/multi_agent_system_2.0
cd multi_agent_system_2.0
```

2. Create `.env` file

```
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
E2B_API_KEY=your_key
TAVILY_API_KEY=your_key
LANGCHAIN_API_KEY=your_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=your_project
MODEL=qwen/qwen3.8-27b
```

3. Start everything

```bash
docker-compose up --build
```

4. Hit the API

```bash
curl -X POST http://localhost:8000/chat/supervisor \
  -H 'Content-Type: application/json' \
  -d '{"message": "analyze my sales data", "session_id": "user123"}'
```

5. Open the frontend

```
frontend/index.html
```

## Project Structure

```
multi_agent_system_2.0/
├── main.py                    # FastAPI app
├── supervisor.py              # LangGraph supervisor + routing
├── data_analyst_agent.py      # Data Analyst agent
├── financial_analyst_agent.py # Financial Analyst agent
├── business_debate_agent.py   # Business Debate agent
├── memory.py                  # Redis session memory
├── db.py                      # PostgreSQL logging
├── config.py                  # Environment config
├── evals.py                   # LangSmith routing evals
├── dataset.py                 # Eval test cases
├── docker-compose.yml         # Redis + Postgres + App
├── Dockerfile                 # FastAPI container
├── requirements.txt
└── frontend/
    └── index.html             # Pixel-themed chat UI
```

## What I Learned

- Building multi-agent systems with LangGraph StateGraph and conditional routing
- Containerizing a full stack app with Docker Compose (app + Redis + Postgres as separate services)
- Session memory with Redis vs permanent logging with Postgres — when to use each
- Evaluating AI systems with LangSmith — routing accuracy, response quality, task completion
- FastAPI async endpoints and Pydantic request validation
- E2B sandboxed code execution for safe real-time data analysis
