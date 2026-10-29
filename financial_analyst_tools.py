from e2b_code_interpreter import Sandbox
from tavily import TavilyClient
from langsmith import traceable
from langchain_core.tools import tool
from config import *
client=TavilyClient(api_key=TAVILY_API_KEY)


@tool
@traceable
def run_code(code:str)->dict:
    """used by the llm to run python code"""
    sandbox=None
    try:
        sandbox=Sandbox.create()
        execute=sandbox.run_code(code)
        return {
            "success":True,
            "output":execute.logs.stdout,
            "warnings":execute.logs.stderr,
            "errors":None,
            "result":[str(r) for r in execute.results] }
    except Exception as e:
        return {
            "success":False,
            "output":None,
            "warnings":None,
            "errors":str[e],
            "result":[]
        }
    finally:
        if sandbox:
            sandbox.kill()

@tool
@traceable
def search_up(query:str,max_results:int=5)->dict:
    """used for searching up relevent info on web"""
    search_result=client.search(query=query,max_results=max_results)
    return search_result["results"]

@tool
@traceable
def extract_up(url):
    """used for extracting the information from url"""
    extract_results=client.extract(url)
    return extract_results["results"]





    


