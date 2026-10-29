import json
import redis
from config import REDIS_URL


r=redis.Redis.from_url(REDIS_URL,decode_responses=True)

SESSION_TTL=60*60*24 #24 hours till the session lives


def get_history(session_id:str)->list[dict]:
    raw=r.get(f"session:{session_id}")
    if raw is None:
        return []
    return json.loads(raw)

def save_history(session_id:str,history: list[dict]):
    r.setex(
        f"session:{session_id}",SESSION_TTL,json.dumps(history)
    )

def append_exchange(session_id:str,human_message:str,ai_message:str):
    history=get_history(session_id)
    history.append({"role":"human","content":human_message})
    history.append({"role":"ai","content":ai_message})
    save_history(session_id,history)

def clear_history(session_id:str):
    r.delete("session:{session_id}")

                   