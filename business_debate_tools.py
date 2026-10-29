from config import *
from langchain_core.tools import tool
from langsmith import traceable
from tavily import TavilyClient


client=TavilyClient(api_key=TAVILY_API_KEY)


@tool
@traceable
def search(query:str,max_results:int=7 )->str:
    """used for searching up relevent information"""
    search_results=client.search(query=query,max_results=max_results)
    return search_results["results"]


@tool
@traceable
def extract(url:list)->str:
    """used to extract information from searched urls """
    extracted_results=client.extract(urls=url)
    return extracted_results["results"]





if __name__ == "__main__":
    searches = search.invoke({"query": "search about strawberry"})
    urls = [r["url"] for r in searches]
    result = extract.invoke({"url": urls})
    print(result)