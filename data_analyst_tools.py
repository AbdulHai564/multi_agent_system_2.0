from config import *
from e2b_code_interpreter import Sandbox
from langsmith import traceable
from langchain_core.tools import tool

@tool
@traceable(name="my_code")
def my_code(code:str) ->dict:
    """Runs python code in e2b safe enviroment and returns the output"""
    sandbox=None
    try:
        sandbox=Sandbox.create()
        execution=sandbox.run_code(code)
        return {
            "success":True,
            "output":execution.logs.stdout,
            "warnings":execution.logs.stderr,
            "error":None,
            "results":[str(r) for r in execution.results]
        }
    except Exception as e:
        return {
            "success":False,
            "output":None,
            "warnings":None,
            "error":str(e),
            "results":[]

        }
    finally:
        if sandbox:
            sandbox.kill() 


        

   