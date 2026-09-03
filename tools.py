from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
     """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
     results = tavily.search(query=query, max_results=3)

     out = []

     for r in results['results']:
         out.append(
             f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
         )
    
     return "\n----\n".join(out)

#This part is BeautifulSoup code to scrape the content of a given URL and return clean text for deeper reading. It removes unnecessary tags like script, style, nav, and footer to provide a cleaner output. The function also handles exceptions and returns an error message if scraping fails.

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        # Fetch the content of the URL with a timeout and a user-agent header
                     #we are using a user-agent header to mimic a browser request,
                     #  which can help avoid being blocked by some websites.                               
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        # Check if the request was successful
        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove script, style, nav, and footer tags to clean the text
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
            # Get the text content, join it with spaces, and strip leading/trailing 
            # whitespace with only the first 3000 characters
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
print(scrape_url.invoke("https://www.hindustantimes.com/world-news"))
kml