from agents import build_reader_agent , build_search_agent , writer_chain , critic_chain
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential
import time


def is_rate_limit_error(error: Exception) -> bool:
    response = getattr(error, "response", None)
    return getattr(response, "status_code", None) == 429

def run_research_pipeline(topic : str) -> dict:

    state = {}

    #search agent working 
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    @retry(retry=retry_if_exception(is_rate_limit_error), stop=stop_after_attempt(3), wait=wait_exponential(multiplier=30, min=30, max=120), reraise=True)
    def call_search_agent():
        search_agent = build_search_agent()
        return search_agent.invoke({
            "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
    
    try:
        search_result = call_search_agent()
    except Exception as e:
        print(f"\n❌ Search agent failed after retries: {str(e)}")
        print("⚠️  Please check: 1) MISTRAL_API_KEY in .env, 2) API rate limits, 3) API quota")
        return state
    
    time.sleep(2)  # Respect 1 RPS rate limit
    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ",state['search_results'])

    #step 2 - reader agent 
    print("\n"+" ="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    @retry(retry=retry_if_exception(is_rate_limit_error), stop=stop_after_attempt(3), wait=wait_exponential(multiplier=30, min=30, max=120), reraise=True)
    def call_reader_agent():
        reader_agent = build_reader_agent()
        return reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })

    try:
        reader_result = call_reader_agent()
    except Exception as e:
        print(f"\n❌ Reader agent failed after retries: {str(e)}")
        return state

    time.sleep(2)  # Respect 1 RPS rate limit

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])

    #step 3 - writer chain 

    print("\n"+" ="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    @retry(retry=retry_if_exception(is_rate_limit_error), stop=stop_after_attempt(3), wait=wait_exponential(multiplier=30, min=30, max=120), reraise=True)
    def call_writer_chain():
        return writer_chain.invoke({
            "topic" : topic,
            "research" : research_combined
        })

    try:
        state["report"] = call_writer_chain()
    except Exception as e:
        print(f"\n❌ Writer chain failed after retries: {str(e)}")
        return state

    time.sleep(2)  # Respect 1 RPS rate limit

    print("\n Final Report\n",state['report'])

    #critic report 

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    @retry(retry=retry_if_exception(is_rate_limit_error), stop=stop_after_attempt(3), wait=wait_exponential(multiplier=30, min=30, max=120), reraise=True)
    def call_critic_chain():
        return critic_chain.invoke({
            "report":state['report']
        })

    try:
        state["feedback"] = call_critic_chain()
    except Exception as e:
        print(f"\n❌ Critic chain failed after retries: {str(e)}")
        return state

    print("\n critic report \n", state['feedback'])

    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)