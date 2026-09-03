from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
from dotenv import load_dotenv
load_dotenv()

llm=ChatMistralAI(
    model="mistral-small-2603",temperature=0)

#1st agent
