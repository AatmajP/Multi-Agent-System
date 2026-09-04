from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

#Pipeline function to run the research process in a structured manner. 
#It takes a topic as input, uses the search agent to gather information,
# the reader agent to scrape content from URLs, and then generates a research report and critique. The function returns a dictionary containing the research report, critique, and the sources used.

def run_research_pipeline(topic: str)-> dict:
    state = {}

    # Step 1: Search agent workjng

    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
                                          #-1 helps to get the last message in 
                                          # the list of messages
    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ",state['search_results'])

     #step 2 - reader agent 
    print("\n"+" ="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])