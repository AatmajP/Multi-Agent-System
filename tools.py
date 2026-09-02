from langchain.tools import Tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

