from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langsmith import Client
from langsmith.evaluation import evaluate

from config import MODEL, GROQ_API_KEY
from dataset import test_cases
from supervisor import run_supervisor_eval


client = Client()

# Use a new name so this dataset includes the new reference fields.
dataset_name = "agent eval v2"

existing_datasets = list(client.list_datasets(dataset_name=dataset_name))

if not existing_datasets:
    dataset = client.create_dataset(dataset_name=dataset_name)

    for test in test_cases:
        client.create_example(
            inputs={"input": test["input"]},
            outputs={
                "expected_agent": test["expected_agent"],
                "expected_facts": test["expected_facts"],
                "task_success_criteria": test["task_success_criteria"],
            },
            dataset_id=dataset.id,
        )


def predict(inputs: dict) -> dict:
    result = run_supervisor_eval(inputs["input"])

    return {
        "actual_agent": result["actual_agent"],
        "response": result["response"],
    }


def routing_evaluator(run, example) -> dict:
    actual = run.outputs.get("actual_agent")
    expected = example.outputs.get("expected_agent")

    return {
        "key": "routing_accuracy",
        "score": 1.0 if actual == expected else 0.0,
        "comment": f"Expected {expected}; got {actual}.",
    }


class AnswerScores(BaseModel):
    correctness: float = Field(ge=0.0, le=1.0)
    correctness_reason: str

    task_completion: float = Field(ge=0.0, le=1.0)
    task_completion_reason: str

    answer_quality: float = Field(ge=0.0, le=1.0)
    answer_quality_reason: str


judge = ChatGroq(
    model=MODEL,
    api_key=GROQ_API_KEY,
    temperature=0,
    max_tokens=400,
).with_structured_output(AnswerScores)


def answer_evaluator(run, example) -> list[dict]:
    user_input = example.inputs.get("input", "")
    response = run.outputs.get("response", "")
    expected_facts = example.outputs.get("expected_facts", [])
    task_criteria = example.outputs.get("task_success_criteria", [])

    scores = judge.invoke(f"""
You are evaluating an AI assistant's final answer.

Score each category from 0.0 to 1.0.

USER REQUEST:
{user_input}

ASSISTANT RESPONSE:
{response}

EXPECTED FACTS FOR CORRECTNESS:
{expected_facts}

TASK COMPLETION CRITERIA:
{task_criteria}

Scoring guidance:
- correctness: Is the response accurate and consistent with the expected facts?
  Penalize unsupported or contradicted claims.
- task_completion: Does it fulfill the listed task criteria?
- answer_quality: Is it clear, relevant, organized, and useful?

Use 1.0 for fully successful, 0.5 for partially successful, and 0.0
for unsuccessful. Give a short reason for each score.
""")

    # One judge call returns all three answer metrics.
    return [
        {
            "key": "final_answer_correctness",
            "score": scores.correctness,
            "comment": scores.correctness_reason,
        },
        {
            "key": "task_completion",
            "score": scores.task_completion,
            "comment": scores.task_completion_reason,
        },
        {
            "key": "final_answer_quality",
            "score": scores.answer_quality,
            "comment": scores.answer_quality_reason,
        },
    ]


results = evaluate(
    predict,
    data=dataset_name,
    evaluators=[routing_evaluator, answer_evaluator],
    experiment_prefix="agent-eval",
)

print(results)