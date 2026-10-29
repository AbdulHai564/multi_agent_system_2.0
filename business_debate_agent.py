from config import *
from business_debate_tools import search,extract
from langchain_classic.tools import Tool
from langchain_classic.agents import AgentExecutor,create_tool_calling_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

llm=ChatGroq(model=MODEL,api_key=GROQ_API_KEY)
tools=[search,extract]
prompt=ChatPromptTemplate([
    ("system","you are a debater,i want you to debate  with the user about his busines plan.I also want ypu to search up the web when you dont have relevent information about a topic or need certain info using tools provided"),
    ("human","{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")



]
)

agent=create_tool_calling_agent(llm,tools,prompt)
executor=AgentExecutor(agent=agent,tools=tools,verbose=True)


def debate(input:str)->str:
    result=executor.invoke({"input":input})
    return result["output"]


if __name__=="__main__":
    response=debate("i think starting a chicken farm is a good idea ")
    print(response)


