import os
from langchain_core.tools import tool
from tavily import TavilyClient
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Initialize Tavily client if the API key is present
# Note: You need to set TAVILY_API_KEY in your .env file
tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key) if tavily_api_key else None

@tool
def web_search(query: str) -> str:
    """
    Search the web for a given query to gather information.
    Always use this tool to find facts, news, and context.
    """
    if not tavily_client:
        return "Error: TAVILY_API_KEY is not set in the environment variables."
    
    try:
        response = tavily_client.search(query=query, search_depth="advanced")
        # Extract the relevant snippets from the search results
        results = []
        for result in response.get("results", []):
            results.append(f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}")
        return "\n\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Error during web search: {str(e)}"

@tool
async def scrape_webpage(url: str) -> str:
    """
    Scrape the full text content of a specific webpage URL.
    Use this when you need detailed information from a specific link.
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=15000)
            html_content = await page.content()
            await browser.close()
            
            # Use BeautifulSoup to extract clean text
            soup = BeautifulSoup(html_content, 'html.parser')
            # Remove scripts and styles
            for script in soup(["script", "style", "header", "footer", "nav"]):
                script.decompose()
            
            text = soup.get_text(separator=' ', strip=True)
            
            # Limit the size to avoid overloading the LLM context window
            # Approx 8000 characters is a safe bet for most models
            return text[:8000] + ("..." if len(text) > 8000 else "")
            
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

# A list of tools to bind to the LLM
research_tools = [web_search, scrape_webpage]
