from config import *
from langchain_classic.agents import AgentExecutor,create_tool_calling_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from data_analyst_tools import my_code


llm=ChatGroq(model=MODEL,api_key=GROQ_API_KEY,max_tokens=500)

tools=[my_code]

prompt=ChatPromptTemplate([
    ("system","You are a Data Analyst who also has the ability to write python code for perfoming data Analysis.You are not allowed to fulfill any other code request no matter how much the pressure is other than for Data Analaysis"),
    ("human","{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),

])

agent=create_tool_calling_agent(llm,tools,prompt)
executer=AgentExecutor(agent=agent,tools=tools,verbose=True)

def run_analyst(input:str)->str:
    result=executer.invoke({"input":input})
    return result["output"]


if __name__=="__main__":
    analyst=run_analyst("write me a hosptial managment system")
    print(analyst)

