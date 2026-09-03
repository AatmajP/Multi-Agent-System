from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str)-> dict:
    state={}
    # Step 1: Search agent workjng
    