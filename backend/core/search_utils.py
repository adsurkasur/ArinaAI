import requests
import logging

DUCKDUCKGO_API_URL = "https://api.duckduckgo.com/"

def needs_web_search(query):
    """Determine if a query requires web search based on keywords."""
    web_search_keywords = [
        "news", "update", "latest", "recent", "event", "schedule", "release",
        "stock price", "weather", "sports score", "match result", "forecast",
        "celebrities", "trending", "movie times", "game release", "scientific discovery",
        "politics", "economic news", "current time", "today's date", "happening now"
    ]
    
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in web_search_keywords)

def search_duckduckgo(query):
    """Perform a DuckDuckGo search and return summarized results."""
    try:
        params = {"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"}
        response = requests.get(DUCKDUCKGO_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract useful data
        summary = data.get("AbstractText", "")
        related_topics = data.get("RelatedTopics", [])
        external_links = [data.get("AbstractURL")] if data.get("AbstractURL") else []

        # Get additional links from RelatedTopics
        for topic in related_topics:
            if isinstance(topic, dict) and "FirstURL" in topic:
                external_links.append(topic["FirstURL"])
        
        return summary, external_links[:3]  # Limit to top 3 links

    except requests.RequestException as e:
        logging.error(f"Error fetching search results: {e}")
        return None, None
