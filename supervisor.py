
from config import *
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Literal
import operator
from pydantic import BaseModel
from langchain_groq import ChatGroq

from business_debate_agent import debate
from data_analyst_agent import run_analyst
from financial_analyst_agent import finance

from memory import get_history, append_exchange
from db import log_message


class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_agent: str
    user_input: str
    final_response: str


llm = ChatGroq(
    model=MODEL,
    api_key=GROQ_API_KEY,
    max_tokens=50
)


class Route(BaseModel):
    next_agent: Literal["analyst", "financial", "debate"]


router = llm.with_structured_output(Route)


def supervisor(state: AgentState):
    decision = router.invoke(f"""
You are the supervisor of a multi-agent AI system.

Your job is to route the user's request to exactly ONE appropriate agent.

Choose the agent based on the user's PRIMARY INTENTION, not merely
the keywords or subject mentioned in the question.

AVAILABLE AGENTS:

1. ANALYST

Choose "analyst" when the user wants to:

- Analyze CSV files, datasets, or other provided business data.
- Perform data analysis using pandas, statistics, or similar methods.
- Identify patterns, trends, anomalies, or correlations in data.
- Investigate changes in sales, revenue, profit, expenses, or business
  performance using available data.
- Understand why a business metric has increased or decreased.
- Generate data-driven business insights.

Examples:
- "Analyze my CSV."
- "Why did my sales decrease according to my data?"
- "What is the main reason my business is taking a hit?"
- "Can you tell me if my profit will increase according to my data?"
- "Should I sell more goods based on the data I provided?"

Business-related questions do not automatically belong to the financial
agent. When the primary task is analyzing existing business data,
choose "analyst".

2. FINANCIAL

Choose "financial" when the user wants to:

- Analyze stocks, securities, or financial markets.
- Research investment opportunities.
- Evaluate stock performance or potential future market movements.
- Discuss IPOs from an investment perspective.
- Compare investment opportunities in publicly traded companies.
- Obtain financial-market research or investment analysis.

Examples:
- "Will Apple's stock price increase in 2027?"
- "Should I invest in an upcoming IPO?"
- "Which AI company should I invest in?"
- "How has Microsoft's stock performed historically?"
- "What are the investment risks of buying Nvidia stock?"

Choose "financial" when the main task concerns investments or financial
markets, not simply because the user mentions money, profit, or revenue.

3. DEBATE

Choose "debate" when the user wants to:

- Evaluate a business idea or proposed venture.
- Discuss the advantages and disadvantages of a business decision.
- Compare strategic alternatives and their trade-offs.
- Decide whether to start, expand, or close a business.
- Evaluate a business model, business strategy, or entrepreneurial idea.
- Receive critical feedback on a proposal or pitch.
- Explore the risks and feasibility of a hypothetical business scenario.

Examples:
- "Should I start a poultry business with $1 million?"
- "Should I build my own LLM or use an existing API?"
- "Is starting an AI agency for international clients a good idea?"
- "Should I start a dog farm in China?"
- "Should I close my business or invest more money in it?"

When the user primarily wants to evaluate a business idea or decide
between strategic alternatives, choose "debate".

ROUTING PRIORITIES:

1. If the user wants to analyze provided data, choose "analyst".
2. If the user wants investment or financial-market analysis, choose
   "financial".
3. If the user wants to evaluate a business idea or strategic decision,
   choose "debate".

For questions that combine multiple topics, identify the primary task
the user wants performed.

Examples:

- "Why is my business losing money according to my CSV?"
  -> analyst

- "Why is Apple's stock losing value?"
  -> financial

- "My business is losing money. Should I close it or invest more?"
  -> debate

- "Analyze my company's revenue and identify the biggest decline."
  -> analyst

- "Should I invest in Apple or start my own business?"
  -> debate, because the primary task is comparing strategic alternatives.

Do not classify a request based only on words such as:
"business", "money", "profit", "revenue", or "investment".

Instead, determine what the user actually wants the system to do.

If the user's request is ambiguous, infer the most likely primary intention
using the available context and the rules above.

USER REQUEST:
{state["user_input"]}
""")

    print(f"Routed to: {decision.next_agent}")

    return {"next_agent": decision.next_agent}


def analyst_mode(state: AgentState):
    response = run_analyst(state["user_input"])
    return {"final_response": response}


def finance_mode(state: AgentState):
    response = finance(state["user_input"])
    return {"final_response": response}


def debate_mode(state: AgentState):
    response = debate(state["user_input"])
    return {"final_response": response}


def route(state: AgentState):
    return state["next_agent"]


graph = StateGraph(AgentState)

graph.add_node("supervisor", supervisor)
graph.add_node("analyst", analyst_mode)
graph.add_node("finance", finance_mode)
graph.add_node("debate", debate_mode)

graph.set_entry_point("supervisor")

graph.add_conditional_edges(
    "supervisor",
    route,
    {
        "analyst": "analyst",
        "financial": "finance",
        "debate": "debate",
    }
)

graph.add_edge("analyst", END)
graph.add_edge("finance", END)
graph.add_edge("debate", END)

app = graph.compile()


def run_supervisor(user_input: str, session_id: str) -> str:
    history = get_history(session_id)

    result = app.invoke({
        "user_input": user_input,
        "messages": []
    })

    response = result["final_response"]

    append_exchange(session_id, user_input, response)

    log_message(session_id, "human", user_input)
    log_message(session_id, "ai", response)

    return response


def run_supervisor_eval(user_input: str) -> dict:
    result = app.invoke({
        "user_input": user_input,
        "messages": []
    })

    return {
        "response": result["final_response"],
        "actual_agent": result["next_agent"]
    }


if __name__ == "__main__":
    test_input = "What is the main reason my business is taking a hit?"

    result = app.invoke({
        "user_input": test_input,
        "messages": []
    })

    print("\nUser:", test_input)
    print("Selected agent:", result["next_agent"])
    print("Response:", result["final_response"])
