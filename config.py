from dotenv import load_dotenv
import os 


load_dotenv()


GROQ_API_KEY=os.getenv("GROQ_API_KEY")
E2B_API_KEY=os.getenv("E2B_API_KEY")
LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY")
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
MODEL=os.getenv("MODEL")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://abdulhai:password@postgres:5432/multi_agent_db")