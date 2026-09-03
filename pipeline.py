from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

#Pipeline function to run the research process in a structured manner. 
#It takes a topic as input, uses the search agent to gather information,
# the reader agent to scrape content from URLs, and then generates a research report and critique. The function returns a dictionary containing the research report, critique, and the sources used.

def run_research_pipeline(topic: str)-> dict:
    state={}
    # Step 1: Search agent workjng
    