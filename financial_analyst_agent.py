from config import *
from langchain_classic.agents import AgentExecutor,create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from financial_analyst_tools import search_up,extract_up,run_code

llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", google_api_key=GEMINI_API_KEY)

tools=[search_up,extract_up,run_code]

prompt=ChatPromptTemplate([
    ("system","you are a financial analyst.i want you to use your financial knowledge and use python code the best way accordingly for calculations and help the user .Also use the web tools provided whenever you feel the need to use them.Do not entertain any other user query other than financial questions and stuff.Make sure to answer user with structured evidence and reasoning in plain english and numbers"),
    ("human","{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])
agent=create_tool_calling_agent(llm,tools,prompt)
exectute_agent=AgentExecutor(agent=agent,tools=tools,verbose=True)


def finance(input:str)->str:
    result=exectute_agent.invoke({"input":input})
    return result["output"]



if __name__=="__main__":
    response=finance("should i buy apple stocks or nvidia stocks")
    print(response)