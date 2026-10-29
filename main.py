from fastapi import FastAPI
from pydantic import BaseModel
from data_analyst_agent import run_analyst
from business_debate_agent import debate
from financial_analyst_agent import finance
from supervisor import run_supervisor

app=FastAPI()

class Request(BaseModel):
    message:str
    session_id:str="default"

@app.post("/chat/analyst")
async def analyst_endpoint(request:Request):
    response=run_analyst(request.message)
    return {"response":response}

@app.post("/chat/debate")
async def debate_endpoint(request:Request):
    response=debate(request.message)
    return {"response":response}

@app.post("/chat/finance")
async def finance_endpoint(request: Request):
    response = finance(request.message)
    return {"response": response}

@app.post("/chat/supervisor")
async def supervisor_endpoint(request: Request):
    response = run_supervisor(request.message,request.session_id)
    return {"response": response}

@app.get("/health")
async def health():
    return {"status":"Ok"}