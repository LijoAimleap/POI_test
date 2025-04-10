# import requests
# from bs4 import BeautifulSoup
# from typing import List, Dict, Optional
# import os
# from pydantic import BaseModel, Field
# from langchain_community.tools import DuckDuckGoSearchResults
# from tavily import TavilyClient
# from duckduckgo_search import DDGS

# class WebSearchResult(BaseModel):
#     source: str = Field(..., description="Source of the search result")
#     title: Optional[str] = Field(None, description="Title of the result")
#     link: Optional[str] = Field(None, description="URL of the result")
#     snippet: Optional[str] = Field(None, description="Brief description or snippet")

# class WebSearchTools:
#     @staticmethod
#     def duckduckgo_search(query: str, max_results: int = 5):
#         try:
#             with DDGS() as ddgs:
#                 search_results = list(ddgs.text(query, max_results=max_results))
                
#             if not search_results:
#                 return []

#             formatted_results = [
#                 WebSearchResult(
#                     source="duckduckgo",
#                     title=r.get("title", ""),
#                     link=r.get("href", ""),
#                     snippet=r.get("body", "")
#                 )
#                 for r in search_results if isinstance(r, dict)
#             ]
#             return formatted_results
        
#         except Exception as e:
#             print(f"DuckDuckGo search error: {e}")
#             return []

#     @staticmethod
#     def tavily_search(query: str, num_results: int = 5) -> List[WebSearchResult]:
#         """Search Tavily and return structured results."""
#         try:
#             api_key = os.getenv("TAVILY_API_KEY")
#             if not api_key:
#                 print("Error: Tavily API key not set.")
#                 return []
            
#             tavily = TavilyClient(api_key=api_key)
#             search_results = tavily.search(query=query, max_results=num_results)
#             return [
#                 WebSearchResult(
#                     source="tavily",
#                     title=result.get("title", ""),
#                     link=result.get("url", ""),
#                     snippet=result.get("excerpt", "")
#                 )
#                 for result in search_results.get("results", [])
#             ]
        
#         except Exception as e:
#             print(f"Tavily search error: {e}")
#             return []

#     @staticmethod
#     def scrape_webpage(url: str) -> Dict:
#         try:
#             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
#             response = requests.get(url, headers=headers, timeout=10)
#             soup = BeautifulSoup(response.text, 'html.parser')

#             print(f"DEBUG: Scraping {url} for NFL game information")
            
#             return {
#                 'title': soup.title.string if soup.title else '',
#                 'text': soup.get_text(strip=True),
#                 'links': [a.get('href') for a in soup.find_all('a', href=True)],
#                 'source_url': url
#             }
#         except Exception as e:
#             print(f"Webpage scraping error for {url}: {e}")
#             return {}
            
#     @staticmethod
#     def scrape_nfl_sources() -> List[Dict]:
#         """Scrape predefined NFL sources for game information"""
#         nfl_sources = [
#             "https://www.foxsports.com/stories/nfl",
#             "https://www.cbssports.com/nfl/2/",
#             "https://lastwordonsports.com/nfl/category/nfl-teams/",
#             "https://www.nbcsportsbayarea.com/nfl/",
#             "https://ninerswire.usatoday.com/lists/",
#             "https://sportsnaut.com/nfl/",
#             "https://www.nfl.com/"
#         ]
        
#         results = []
#         for url in nfl_sources:
#             try:
#                 data = WebSearchTools.scrape_webpage(url)
#                 if data:
#                     results.append(data)
#             except Exception as e:
#                 print(f"Failed to scrape {url}: {e}")
                
#         return results
    


#     nba_sources = [
#         "https://www.nbcsports.com/betting/nba/tools/game-predictions",
#         "https://www.pickswise.com/nba/picks/",
#         "https://www.nba.com/",
#         "https://www.espn.in/nba/",
#         "https://www.nba.com/news",
#         "https://bleacherreport.com/nba",
#         "https://www.cbssports.com/nba/expert-picks/"
#         ]



# import requests
# from bs4 import BeautifulSoup
# from typing import List, Dict, Optional, Set
# import os
# from pydantic import BaseModel, Field
# from langchain_community.tools import DuckDuckGoSearchResults
# from tavily import TavilyClient
# from duckduckgo_search import DDGS

# class WebSearchResult(BaseModel):
#     source: str = Field(..., description="Source of the search result")
#     title: Optional[str] = Field(None, description="Title of the result")
#     link: Optional[str] = Field(None, description="URL of the result")
#     snippet: Optional[str] = Field(None, description="Brief description or snippet")

# class WebSearchTools:
#     @staticmethod
#     def duckduckgo_search(query: str, max_results: int = 5):
#         try:
#             with DDGS() as ddgs:
#                 search_results = list(ddgs.text(query, max_results=max_results))
                
#             if not search_results:
#                 return []
#             formatted_results = [
#                 WebSearchResult(
#                     source="duckduckgo",
#                     title=r.get("title", ""),
#                     link=r.get("href", ""),
#                     snippet=r.get("body", "")
#                 )
#                 for r in search_results if isinstance(r, dict)
#             ]
#             return formatted_results
        
#         except Exception as e:
#             print(f"DuckDuckGo search error: {e}")
#             return []

#     @staticmethod
#     def tavily_search(query: str, num_results: int = 5) -> List[WebSearchResult]:
#         """Search Tavily and return structured results."""
#         try:
#             api_key = os.getenv("TAVILY_API_KEY")
#             if not api_key:
#                 print("Error: Tavily API key not set.")
#                 return []
            
#             tavily = TavilyClient(api_key=api_key)
#             search_results = tavily.search(query=query, max_results=num_results)
#             return [
#                 WebSearchResult(
#                     source="tavily",
#                     title=result.get("title", ""),
#                     link=result.get("url", ""),
#                     snippet=result.get("excerpt", "")
#                 )
#                 for result in search_results.get("results", [])
#             ]
        
#         except Exception as e:
#             print(f"Tavily search error: {e}")
#             return []

#     @staticmethod
#     def scrape_webpage(url: str) -> Dict:
#         try:
#             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
#             response = requests.get(url, headers=headers, timeout=10)
#             soup = BeautifulSoup(response.text, 'html.parser')
#             print(f"DEBUG: Scraping {url} for game information")
            
#             return {
#                 'title': soup.title.string if soup.title else '',
#                 'text': soup.get_text(strip=True),
#                 'links': [a.get('href') for a in soup.find_all('a', href=True)],
#                 'source_url': url
#             }
#         except Exception as e:
#             print(f"Webpage scraping error for {url}: {e}")
#             return {}
            
#     @staticmethod
#     def scrape_league_sources(league_sources: List[str]) -> List[Dict]:
#         """Scrape predefined sources for game information"""
#         results = []
#         for url in league_sources:
#             try:
#                 data = WebSearchTools.scrape_webpage(url)
#                 if data:
#                     results.append(data)
#             except Exception as e:
#                 print(f"Failed to scrape {url}: {e}")
                
#         return results
    
#     @staticmethod
#     def get_league_sources(league: str) -> List[str]:
#         """Get predefined sources for different leagues"""
#         sources = {
#             "NFL": [
#                 "https://www.foxsports.com/stories/nfl",
#                 "https://www.cbssports.com/nfl/2/",
#                 "https://lastwordonsports.com/nfl/category/nfl-teams/",
#                 "https://www.nbcsportsbayarea.com/nfl/",
#                 "https://ninerswire.usatoday.com/lists/",
#                 "https://sportsnaut.com/nfl/",
#                 "https://www.nfl.com/"
#             ],
#             "NBA": [
#                 "https://www.nbcsports.com/betting/nba/tools/game-predictions",
#                 "https://www.pickswise.com/nba/picks/",
#                 "https://www.nba.com/",
#                 "https://www.espn.in/nba/",
#                 "https://www.nba.com/news",
#                 "https://bleacherreport.com/nba",
#                 "https://www.cbssports.com/nba/expert-picks/"
#             ],
#             "MLB": [
#                 "https://www.mlb.com/",
#                 "https://www.espn.com/mlb/",
#                 "https://www.cbssports.com/mlb/",
#                 "https://www.foxsports.com/mlb",
#                 "https://www.sportingnews.com/us/mlb"
#             ],
#             "NHL": [
#                 "https://www.nhl.com/",
#                 "https://www.espn.com/nhl/",
#                 "https://www.cbssports.com/nhl/",
#                 "https://www.foxsports.com/nhl",
#                 "https://www.sportingnews.com/us/nhl"
#             ],
#             "EPL": [
#                 "https://www.premierleague.com/",
#                 "https://www.skysports.com/premier-league",
#                 "https://www.espn.com/soccer/league/_/name/eng.1",
#                 "https://www.bbc.com/sport/football/premier-league"
#             ]
#         }
        
#         # Default to NFL if league not found
#         return sources.get(league.upper(), sources["NFL"])






# import os
# from typing import Optional, Any, List, Dict
# from pydantic import BaseModel, Field
# from composio import Action, ComposioToolSet
# from dotenv import load_dotenv
# from duckduckgo_search.duckduckgo_search import DDGS
 
# load_dotenv()
 
# class WebSearchResult(BaseModel):
#     source: str = Field(..., description="Source of the search result")
#     title: Optional[str] = Field(None, description="Title of the result")
#     link: Optional[str] = Field(None, description="URL of the result")
#     snippet: Optional[str] = Field(None, description="Brief description or snippet")

# class WebSearchRequest(BaseModel):
#     url: str = Field(..., min_length=3, description="Search keywords")
#     depth: int = Field(5, ge=1, le=100, description="Number of results")
 
# class Metadata(BaseModel):
#     favicon: Optional[str] = None
#     language: Optional[str] = None
#     title: Optional[str] = None
#     robots: Optional[str] = None
#     description: Optional[str] = None
#     sourceURL: Optional[str] = None
#     url: Optional[str] = None
#     statusCode: Optional[int] = None
 
# class Response(BaseModel):
#     markdown: str
#     metadata: Metadata
#     error: Optional[Any]
#     successful: bool

# class WebSearchTools:
#     @staticmethod
#     def duckduckgo_search(query: str, max_results: int = 5):
#         try:
#             with DDGS() as ddgs:
#                 search_results = list(ddgs.text(query, max_results=max_results))
                
#             if not search_results:
#                 return []
#             formatted_results = [
#                 WebSearchResult(
#                     source="duckduckgo",
#                     title=r.get("title", ""),
#                     link=r.get("href", ""),
#                     snippet=r.get("body", "")
#                 )
#                 for r in search_results if isinstance(r, dict)
#             ]
#             return formatted_results
        
#         except Exception as e:
#             print(f"DuckDuckGo search error: {e}")
#             return []
            
#     @staticmethod
#     def webscraper(request: WebSearchRequest) -> Response:
#         toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY", "ejm8n03dk9bivq6ltf1y9e"))
#         raw_response = toolset.execute_action(
#             action=Action.FIRECRAWL_SCRAPE_EXTRACT_DATA_LLM,
#             params=request.model_dump()
#         )
       
#         try:
#             markdown = raw_response["data"]["data"]["data"]["markdown"]
#             metadata = raw_response["data"]["data"]["data"]["metadata"]
            
#             # Ensure description is a string type
#             if "description" in metadata and not isinstance(metadata["description"], str):
#                 metadata["description"] = str(metadata["description"]) if metadata["description"] else ""
           
#             return Response(
#                 markdown=markdown,
#                 metadata=Metadata(**metadata),
#                 error=raw_response["error"],
#                 successful=raw_response["successful"]
#             ).model_dump()
           
#         except KeyError as e:
#             return Response(
#                 markdown="",
#                 metadata=Metadata(),
#                 error=str(e),
#                 successful=False
#             ).model_dump()
    
#     @staticmethod
#     def scrape_webpage(url: str) -> Dict:
#         """Scrape webpage using Composio"""
#         try:
#             search_request = WebSearchRequest(
#                 url=url,
#                 depth=2
#             )
            
#             response = WebSearchTools.webscraper(search_request)
            
#             if response.get("successful", False):
#                 metadata = response.get("metadata", {})
#                 return {
#                     'title': metadata.get("title", ""),
#                     'text': response.get("markdown", ""),
#                     'links': [],  # No links extraction in this version
#                     'source_url': url
#                 }
#             else:
#                 print(f"Failed to scrape {url}: {response.get('error', 'Unknown error')}")
#                 return {}
#         except Exception as e:
#             print(f"Webpage scraping error for {url}: {e}")
#             return {}
            
#     @staticmethod
#     def scrape_league_sources(league_sources: List[str]) -> List[Dict]:
#         """Scrape predefined sources for game information"""
#         results = []
#         for url in league_sources:
#             try:
#                 data = WebSearchTools.scrape_webpage(url)
#                 if data:
#                     results.append(data)
#             except Exception as e:
#                 print(f"Failed to scrape {url}: {e}")
                
#         return results
    
#     @staticmethod
#     def get_league_sources(league: str) -> List[str]:
#         """Get predefined sources for different leagues"""
#         sources = {
#             "NFL": [
#                 "https://www.foxsports.com/stories/nfl",
#                 "https://www.cbssports.com/nfl/2/",
#                 "https://lastwordonsports.com/nfl/category/nfl-teams/",
#                 "https://www.nbcsportsbayarea.com/nfl/",
#                 "https://ninerswire.usatoday.com/lists/",
#                 "https://sportsnaut.com/nfl/",
#                 "https://www.nfl.com/"
#             ],
#             "NBA": [
#                 "https://www.nbcsports.com/betting/nba/tools/game-predictions",
#                 "https://www.pickswise.com/nba/picks/",
#                 "https://www.nba.com/",
#                 "https://www.espn.com/nba/",
#                 "https://www.nba.com/news",
#                 "https://bleacherreport.com/nba",
#                 "https://www.cbssports.com/nba/expert-picks/"
#             ],
#             "MLB": [
#                 "https://www.mlb.com/",
#                 "https://www.espn.com/mlb/",
#                 "https://www.cbssports.com/mlb/",
#                 "https://www.foxsports.com/mlb",
#                 "https://www.sportingnews.com/us/mlb"
#             ],
#             "NHL": [
#                 "https://www.nhl.com/",
#                 "https://www.espn.com/nhl/",
#                 "https://www.cbssports.com/nhl/",
#                 "https://www.foxsports.com/nhl",
#                 "https://www.sportingnews.com/us/nhl"
#             ],
#             "EPL": [
#                 "https://www.premierleague.com/",
#                 "https://www.skysports.com/premier-league",
#                 "https://www.espn.com/soccer/league/_/name/eng.1",
#                 "https://www.bbc.com/sport/football/premier-league"
#             ]
#         }
        
#         # Default to NFL if league not found
#         return sources.get(league.upper(), sources["NFL"])

#     @staticmethod
#     def research_tool(query: str, max_result: int = 5, max_depth: int = 2):
#         """Integrated research tool using both search and scrape capabilities"""
#         search_results = []
#         try:
#             with DDGS() as ddgs:
#                 search_results = list(ddgs.text(query, max_results=max_result))
#         except Exception as e:
#             return {"error": str(e)}
       
#         urls = [result["href"] for result in search_results if "href" in result]
       
#         results = []
#         for url in urls:
#             search_request = WebSearchRequest(
#                 url=url,
#                 depth=max_depth
#             )
#             response = WebSearchTools.webscraper(search_request)
#             results.append(response)
       
#         return results




# import os
# from typing import Optional, Any, List, Dict
# from pydantic import BaseModel, Field
# from composio import Action, ComposioToolSet
# from dotenv import load_dotenv
# from duckduckgo_search.duckduckgo_search import DDGS
 
# load_dotenv()
 
# class WebSearchResult(BaseModel):
#     source: str = Field(..., description="Source of the search result")
#     title: Optional[str] = Field(None, description="Title of the result")
#     link: Optional[str] = Field(None, description="URL of the result")
#     snippet: Optional[str] = Field(None, description="Brief description or snippet")

# class WebSearchRequest(BaseModel):
#     url: str = Field(..., min_length=3, description="Search keywords")
#     depth: int = Field(5, ge=1, le=100, description="Number of results")
 
# class Metadata(BaseModel):
#     favicon: Optional[str] = None
#     language: Optional[str] = None
#     title: Optional[str] = None
#     robots: Optional[str] = None
#     description: Optional[str] = None
#     sourceURL: Optional[str] = None
#     url: Optional[str] = None
#     statusCode: Optional[int] = None
 
# class Response(BaseModel):
#     markdown: str
#     metadata: Metadata
#     error: Optional[Any]
#     successful: bool

# class WebSearchTools:
#     @staticmethod
#     def duckduckgo_search(query: str, max_results: int = 5):
#         print(f"[DEBUG] Starting DuckDuckGo search for query: {query}")
#         try:
#             with DDGS() as ddgs:
#                 search_results = list(ddgs.text(query, max_results=max_results))
#             if not search_results:
#                 return []
#             formatted_results = [
#                 WebSearchResult(
#                     source="duckduckgo",
#                     title=r.get("title", ""),
#                     link=r.get("href", ""),
#                     snippet=r.get("body", "")
#                 )
#                 for r in search_results if isinstance(r, dict)
#             ]
#             print(f"[DEBUG] DuckDuckGo search returned {len(formatted_results)} results")
#             return formatted_results
        
#         except Exception as e:
#             print(f"[ERROR] DuckDuckGo search error: {e}")
#             return []
            
#     @staticmethod
#     def webscraper(request: WebSearchRequest) -> Response:
#         print(f"[DEBUG] Starting webscraper for URL: {request.url}")
#         toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY", "ejm8n03dk9bivq6ltf1y9e"))
#         raw_response = toolset.execute_action(
#             action=Action.FIRECRAWL_SCRAPE_EXTRACT_DATA_LLM,
#             params=request.model_dump()
#         )
       
#         try:
#             markdown = raw_response["data"]["data"]["data"]["markdown"]
#             metadata = raw_response["data"]["data"]["data"]["metadata"]
#             if "description" in metadata and not isinstance(metadata["description"], str):
#                 metadata["description"] = str(metadata["description"]) if metadata["description"] else ""
           
#             print(f"[DEBUG] Webscraper successfully scraped URL: {request.url}")
#             return Response(
#                 markdown=markdown,
#                 metadata=Metadata(**metadata),
#                 error=raw_response["error"],
#                 successful=raw_response["successful"]
#             ).model_dump()
           
#         except KeyError as e:
#             print(f"[ERROR] KeyError in webscraper for URL {request.url}: {e}")
#             return Response(
#                 markdown="",
#                 metadata=Metadata(),
#                 error=str(e),
#                 successful=False
#             ).model_dump()
    
#     @staticmethod
#     def scrape_webpage(url: str) -> Dict:
#         print(f"[DEBUG] Attempting to scrape webpage: {url}")
#         try:
#             search_request = WebSearchRequest(
#                 url=url,
#                 depth=2
#             )
#             response = WebSearchTools.webscraper(search_request)
#             if response.get("successful", False):
#                 metadata = response.get("metadata", {})
#                 print(f"[DEBUG] Successfully scraped {url}")
#                 return {
#                     'title': metadata.get("title", ""),
#                     'text': response.get("markdown", ""),
#                     'links': [],
#                     'source_url': url
#                 }
#             else:
#                 print(f"[ERROR] Failed to scrape {url}: {response.get('error', 'Unknown error')}")
#                 return {}
#         except Exception as e:
#             print(f"[ERROR] Exception while scraping {url}: {e}")
#             return {}
            
#     @staticmethod
#     def scrape_league_sources(league_sources: List[str]) -> List[Dict]:
#         print(f"[DEBUG] Starting scrape of league sources: {league_sources}")
#         results = []
#         for url in league_sources:
#             try:
#                 data = WebSearchTools.scrape_webpage(url)
#                 if data:
#                     results.append(data)
#             except Exception as e:
#                 print(f"[ERROR] Failed to scrape {url}: {e}")
#         print(f"[DEBUG] Completed scraping league sources. Total entries: {len(results)}")
#         return results
    
#     @staticmethod
#     def get_league_sources(league: str) -> List[str]:
#         sources = {
#             "NFL": [
#                 "https://www.foxsports.com/stories/nfl",
#                 "https://www.cbssports.com/nfl/2/",
#                 "https://lastwordonsports.com/nfl/category/nfl-teams/",
#                 "https://www.nbcsportsbayarea.com/nfl/",
#                 "https://ninerswire.usatoday.com/lists/",
#                 "https://sportsnaut.com/nfl/",
#                 "https://www.nfl.com/"
#             ],
#             "NBA": [
#                 "https://www.nbcsports.com/betting/nba/tools/game-predictions",
#                 "https://www.pickswise.com/nba/picks/",
#                 "https://www.nba.com/",
#                 "https://www.espn.com/nba/",
#                 "https://www.nba.com/news",
#                 "https://bleacherreport.com/nba",
#                 "https://www.cbssports.com/nba/expert-picks/"
#             ],
#             "MLB": [
#                 "https://www.mlb.com/",
#                 "https://www.espn.com/mlb/",
#                 "https://www.cbssports.com/mlb/",
#                 "https://www.foxsports.com/mlb",
#                 "https://www.sportingnews.com/us/mlb"
#             ],
#             "NHL": [
#                 "https://www.nhl.com/",
#                 "https://www.espn.com/nhl/",
#                 "https://www.cbssports.com/nhl/",
#                 "https://www.foxsports.com/nhl",
#                 "https://www.sportingnews.com/us/nhl"
#             ],
#             "EPL": [
#                 "https://www.premierleague.com/",
#                 "https://www.skysports.com/premier-league",
#                 "https://www.espn.com/soccer/league/_/name/eng.1",
#                 "https://www.bbc.com/sport/football/premier-league"
#             ]
#         }
#         league_sources = sources.get(league.upper(), sources["NFL"])
#         print(f"[DEBUG] get_league_sources for {league}: {league_sources}")
#         return league_sources

#     @staticmethod
#     def research_tool(query: str, max_result: int = 5, max_depth: int = 2):
#         print(f"[DEBUG] Starting research_tool with query: {query}")
#         search_results = []
#         try:
#             with DDGS() as ddgs:
#                 search_results = list(ddgs.text(query, max_results=max_result))
#         except Exception as e:
#             return {"error": str(e)}
       
#         urls = [result["href"] for result in search_results if "href" in result]
#         print(f"[DEBUG] research_tool found {len(urls)} URLs")
       
#         results = []
#         for url in urls:
#             search_request = WebSearchRequest(
#                 url=url,
#                 depth=max_depth
#             )
#             response = WebSearchTools.webscraper(search_request)
#             results.append(response)
#         print(f"[DEBUG] research_tool completed with {len(results)} results")
#         return results






# import os
# from typing import Optional, Any, List, Dict
# from pydantic import BaseModel, Field
# from composio import Action, ComposioToolSet
# from dotenv import load_dotenv
# from duckduckgo_search.duckduckgo_search import DDGS

# load_dotenv()

# class WebSearchRequest(BaseModel):
#     url: str = Field(..., min_length=3, description="Search keywords")
#     depth: int = Field(5, ge=1, le=100, description="Number of results")

# class Metadata(BaseModel):
#     favicon: Optional[str] = None
#     language: Optional[str] = None
#     title: Optional[str] = None
#     robots: Optional[str] = None
#     description: Optional[str] = None
#     sourceURL: Optional[str] = None
#     url: Optional[str] = None
#     statusCode: Optional[int] = None

# class Response(BaseModel):
#     markdown: str
#     metadata: Metadata
#     error: Optional[Any]
#     successful: bool

# def search(query: str, max_result: int) -> List[Dict[str, str]]:
#     try:
#         print(f"[DEBUG] Attempting DuckDuckGo search for: {query}")
#         with DDGS() as ddgs:
#             results = list(ddgs.text(query, max_results=max_result))
#             print(f"[DEBUG] DuckDuckGo search returned {len(results)} results for query: {query}")
#             return results
#     except Exception as e:
#         print(f"[ERROR] DuckDuckGo search failed with error: {str(e)}")
#         return {"error": str(e)}

# def webscraper(request: WebSearchRequest) -> Response:
#     try:
#         print(f"[DEBUG] Attempting to scrape URL: {request.url}")
#         api_key = os.getenv("COMPOSIO_API_KEY", "ejm8n03dk9bivq6ltf1y9e")
#         if not api_key:
#             print("[WARNING] No COMPOSIO_API_KEY found in environment variables")
        
#         toolset = ComposioToolSet(api_key=api_key)
#         raw_response = toolset.execute_action(
#             action=Action.FIRECRAWL_SCRAPE_EXTRACT_DATA_LLM,
#             params=request.model_dump()
#         )
        
#         try:
#             markdown = raw_response["data"]["data"]["data"]["markdown"]
#             metadata = raw_response["data"]["data"]["data"]["metadata"]
#             print(f"[DEBUG] Successfully scraped URL: {request.url} (Metadata title: {metadata.get('title', 'No title')})")
#             return Response(
#                 markdown=markdown,
#                 metadata=Metadata(**metadata),
#                 error=raw_response["error"],
#                 successful=raw_response["successful"]
#             ).model_dump()
#         except KeyError as e:
#             print(f"[ERROR] KeyError processing scrape result for {request.url}: {str(e)}")
#             return Response(
#                 markdown="",
#                 metadata=Metadata(),
#                 error=f"KeyError processing response: {str(e)}",
#                 successful=False
#             ).model_dump()
#     except Exception as e:
#         print(f"[ERROR] Exception during scraping of {request.url}: {str(e)}")
#         return Response(
#             markdown="",
#             metadata=Metadata(),
#             error=str(e),
#             successful=False
#         ).model_dump()

# def scrape(url: str, max_depth=2) -> Response:
#     print(f"[DEBUG] scrape called for URL: {url}")
#     search_request = WebSearchRequest(
#         url=url,
#         depth=max_depth
#     )
#     return webscraper(search_request)

# # Optional research_tool; not used as only provided links are scraped.
# def research_tool(query: str, max_result: int = 5, max_depth: int = 2):
#     print(f"[DEBUG] research_tool called with query: {query}")
#     search_results = search(query, max_result)
#     if "error" in search_results:
#         print(f"[ERROR] research_tool search error: {search_results['error']}")
#         return search_results
    
#     urls = [result["href"] for result in search_results]
#     print(f"[DEBUG] research_tool preparing to scrape {len(urls)} URLs")
    
#     results = []
#     for idx, url in enumerate(urls):
#         print(f"[DEBUG] research_tool scraping URL {idx+1}/{len(urls)}: {url}")
#         response = scrape(url, max_depth)
#         if response.get("successful", False):
#             print(f"[DEBUG] Successfully scraped {url}")
#         else:
#             print(f"[ERROR] Failed to scrape {url}: {response.get('error', 'Unknown error')}")
#         results.append(response)
    
#     print(f"[DEBUG] research_tool completed with {len(results)} results")
#     return results

# class WebSearchTools:
#     @staticmethod
#     def get_league_sources(league: str) -> List[str]:
#         sources = {
#             "NFL": [
#                 "https://www.foxsports.com/stories/nfl",
#                 "https://www.cbssports.com/nfl/2/",
#                 "https://lastwordonsports.com/nfl/category/nfl-teams/",
#                 "https://www.nbcsportsbayarea.com/nfl/",
#                 "https://ninerswire.usatoday.com/lists/",
#                 "https://sportsnaut.com/nfl/",
#                 "https://www.nfl.com/"
#             ],
#             "NBA": [
#                 "https://www.bleachernation.com/picks/2025/04/09/magic-vs-celtics-prediction-expert-picks-odds-stats-and-best-bets-wednesday-april-9-2025/",
#                 "https://www.nbcsports.com/betting/nba/tools/game-predictions",
#                 "https://www.pickswise.com/nba/picks/",
#                 "https://www.nba.com/",
#                 "https://www.espn.com/nba/",
#                 "https://www.nba.com/news",
#                 "https://bleacherreport.com/nba",
#                 "https://www.cbssports.com/nba/expert-picks/"
#             ],
#             "MLB": [
#                 "https://www.mlb.com/",
#                 "https://www.espn.com/mlb/",
#                 "https://www.cbssports.com/mlb/",
#                 "https://www.foxsports.com/mlb",
#                 "https://www.sportingnews.com/us/mlb"
#             ],
#             "NHL": [
#                 "https://www.nhl.com/",
#                 "https://www.espn.com/nhl/",
#                 "https://www.cbssports.com/nhl/",
#                 "https://www.foxsports.com/nhl",
#                 "https://www.sportingnews.com/us/nhl"
#             ],
#             "EPL": [
#                 "https://www.premierleague.com/",
#                 "https://www.skysports.com/premier-league",
#                 "https://www.espn.com/soccer/league/_/name/eng.1",
#                 "https://www.bbc.com/sport/football/premier-league"
#             ]
#         }
#         league_sources = sources.get(league.upper(), sources["NFL"])
#         print(f"[DEBUG] get_league_sources for {league}: {league_sources}")
#         return league_sources
    
#     @staticmethod
#     def scrape(url: str, max_depth=2) -> dict:
#         print(f"[DEBUG] WebSearchTools.scrape called for URL: {url}")
#         try:
#             response = scrape(url, max_depth)
#             if response.get("successful", False):
#                 print(f"[DEBUG] WebSearchTools.scrape successful for {url}")
#             else:
#                 print(f"[ERROR] WebSearchTools.scrape failed for {url}: {response.get('error', 'Unknown error')}")
#             return response
#         except Exception as e:
#             print(f"[ERROR] Exception in WebSearchTools.scrape for {url}: {str(e)}")
#             return {
#                 "markdown": "",
#                 "metadata": {},
#                 "error": str(e),
#                 "successful": False
#             }

# if __name__ == "__main__":
#     import json
#     response = research_tool("What is the best way to learn to code?", max_result=2)
#     print(json.dumps(response, indent=4))



# import os
# from typing import Optional, Any, List, Dict
# from pydantic import BaseModel, Field
# from composio import Action, ComposioToolSet
# from dotenv import load_dotenv
# from duckduckgo_search.duckduckgo_search import DDGS

# load_dotenv()

# class WebSearchRequest(BaseModel):
#     url: str = Field(..., min_length=3, description="Search keywords")
#     depth: int = Field(5, ge=1, le=100, description="Number of results")

# class Metadata(BaseModel):
#     favicon: Optional[str] = None
#     language: Optional[str] = None
#     title: Optional[str] = None
#     robots: Optional[str] = None
#     description: Optional[str] = None
#     sourceURL: Optional[str] = None
#     url: Optional[str] = None
#     statusCode: Optional[int] = None

# class Response(BaseModel):
#     markdown: str
#     metadata: Metadata
#     error: Optional[Any]
#     successful: bool

# def search(query: str, max_result: int) -> List[Dict[str, str]]:
#     try:
#         print(f"[DEBUG] Attempting DuckDuckGo search for: {query}")
#         with DDGS() as ddgs:
#             results = list(ddgs.text(query, max_results=max_result))
#             print(f"[DEBUG] DuckDuckGo search returned {len(results)} results for query: {query}")
#             return results
#     except Exception as e:
#         print(f"[ERROR] DuckDuckGo search failed with error: {str(e)}")
#         return {"error": str(e)}

# def webscraper(request: WebSearchRequest) -> Response:
#     try:
#         print(f"[DEBUG] Attempting to scrape URL: {request.url}")
#         api_key = os.getenv("COMPOSIO_API_KEY", "ejm8n03dk9bivq6ltf1y9e")
#         if not api_key:
#             print("[WARNING] No COMPOSIO_API_KEY found in environment variables")
        
#         toolset = ComposioToolSet(api_key=api_key)
#         raw_response = toolset.execute_action(
#             action=Action.FIRECRAWL_SCRAPE_EXTRACT_DATA_LLM,
#             params=request.model_dump()
#         )
        
#         try:
#             # Attempt to extract the expected nested data
#             markdown = raw_response["data"]["data"]["data"]["markdown"]
#             metadata = raw_response["data"]["data"]["data"]["metadata"]
#             print(f"[DEBUG] Successfully scraped URL: {request.url} (Metadata title: {metadata.get('title', 'No title')})")
#             return Response(
#                 markdown=markdown,
#                 metadata=Metadata(**metadata),
#                 error=raw_response.get("error"),
#                 successful=raw_response.get("successful", False)
#             ).model_dump()
#         except KeyError as e:
#             # Log the error and the full raw response for debugging
#             print(f"[ERROR] KeyError processing scrape result for {request.url}: {str(e)}")
#             print(f"[ERROR] Full raw response: {raw_response}")
#             return Response(
#                 markdown="",
#                 metadata=Metadata(),
#                 error=f"KeyError processing response: {str(e)}",
#                 successful=False
#             ).model_dump()
#     except Exception as e:
#         print(f"[ERROR] Exception during scraping of {request.url}: {str(e)}")
#         return Response(
#             markdown="",
#             metadata=Metadata(),
#             error=str(e),
#             successful=False
#         ).model_dump()

# def scrape(url: str, max_depth=2) -> Response:
#     print(f"[DEBUG] scrape called for URL: {url}")
#     search_request = WebSearchRequest(
#         url=url,
#         depth=max_depth
#     )
#     return webscraper(search_request)

# # Optional research_tool; not used as only provided links are scraped.
# def research_tool(query: str, max_result: int = 5, max_depth: int = 2):
#     print(f"[DEBUG] research_tool called with query: {query}")
#     search_results = search(query, max_result)
#     if "error" in search_results:
#         print(f"[ERROR] research_tool search error: {search_results['error']}")
#         return search_results
    
#     urls = [result["href"] for result in search_results]
#     print(f"[DEBUG] research_tool preparing to scrape {len(urls)} URLs")
    
#     results = []
#     for idx, url in enumerate(urls):
#         print(f"[DEBUG] research_tool scraping URL {idx+1}/{len(urls)}: {url}")
#         response = scrape(url, max_depth)
#         if response.get("successful", False):
#             print(f"[DEBUG] Successfully scraped {url}")
#         else:
#             print(f"[ERROR] Failed to scrape {url}: {response.get('error', 'Unknown error')}")
#         results.append(response)
    
#     print(f"[DEBUG] research_tool completed with {len(results)} results")
#     return results

# class WebSearchTools:
#     @staticmethod
#     def get_league_sources(league: str) -> List[str]:
#         sources = {
#             "NFL": [
#                 "https://www.foxsports.com/stories/nfl",
#                 "https://www.cbssports.com/nfl/2/",
#                 "https://lastwordonsports.com/nfl/category/nfl-teams/",
#                 "https://www.nbcsportsbayarea.com/nfl/",
#                 "https://ninerswire.usatoday.com/lists/",
#                 "https://sportsnaut.com/nfl/",
#                 "https://www.nfl.com/"
#             ],
#             "NBA": [
#                 "https://www.bleachernation.com/picks/2025/04/09/magic-vs-celtics-prediction-expert-picks-odds-stats-and-best-bets-wednesday-april-9-2025/",
#                 "https://www.nbcsports.com/betting/nba/tools/game-predictions",
#                 "https://www.pickswise.com/nba/picks/",
#                 "https://www.nba.com/",
#                 "https://www.espn.com/nba/",
#                 "https://www.nba.com/news",
#                 "https://bleacherreport.com/nba",
#                 "https://www.cbssports.com/nba/expert-picks/"
#             ],
#             "MLB": [
#                 "https://www.mlb.com/",
#                 "https://www.espn.com/mlb/",
#                 "https://www.cbssports.com/mlb/",
#                 "https://www.foxsports.com/mlb",
#                 "https://www.sportingnews.com/us/mlb"
#             ],
#             "NHL": [
#                 "https://www.nhl.com/",
#                 "https://www.espn.com/nhl/",
#                 "https://www.cbssports.com/nhl/",
#                 "https://www.foxsports.com/nhl",
#                 "https://www.sportingnews.com/us/nhl"
#             ],
#             "EPL": [
#                 "https://www.premierleague.com/",
#                 "https://www.skysports.com/premier-league",
#                 "https://www.espn.com/soccer/league/_/name/eng.1",
#                 "https://www.bbc.com/sport/football/premier-league"
#             ]
#         }
#         league_sources = sources.get(league.upper(), sources["NFL"])
#         print(f"[DEBUG] get_league_sources for {league}: {league_sources}")
#         return league_sources
    
#     @staticmethod
#     def scrape(url: str, max_depth=2) -> dict:
#         print(f"[DEBUG] WebSearchTools.scrape called for URL: {url}")
#         try:
#             response = scrape(url, max_depth)
#             if response.get("successful", False):
#                 print(f"[DEBUG] WebSearchTools.scrape successful for {url}")
#             else:
#                 print(f"[ERROR] WebSearchTools.scrape failed for {url}: {response.get('error', 'Unknown error')}")
#             return response
#         except Exception as e:
#             print(f"[ERROR] Exception in WebSearchTools.scrape for {url}: {str(e)}")
#             return {
#                 "markdown": "",
#                 "metadata": {},
#                 "error": str(e),
#                 "successful": False
#             }

# if __name__ == "__main__":
#     import json
#     response = research_tool("What is the best way to learn to code?", max_result=2)
#     print(json.dumps(response, indent=4))




import os
from typing import Optional, Any, List, Dict
from pydantic import BaseModel, Field
from composio import Action, ComposioToolSet
from dotenv import load_dotenv
from duckduckgo_search.duckduckgo_search import DDGS

load_dotenv()

class WebSearchRequest(BaseModel):
    url: str = Field(..., min_length=3, description="Search keywords")
    depth: int = Field(5, ge=1, le=100, description="Number of results")

class Metadata(BaseModel):
    favicon: Optional[str] = None
    language: Optional[str] = None
    title: Optional[str] = None
    robots: Optional[str] = None
    description: Optional[str] = None
    sourceURL: Optional[str] = None
    url: Optional[str] = None
    statusCode: Optional[int] = None

class Response(BaseModel):
    markdown: str
    metadata: Metadata
    error: Optional[Any]
    successful: bool

def search(query: str, max_result: int) -> List[Dict[str, str]]:
    try:
        print(f"[DEBUG] Attempting DuckDuckGo search for: {query}")
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_result))
            print(f"[DEBUG] DuckDuckGo search returned {len(results)} results for query: {query}")
            return results
    except Exception as e:
        print(f"[ERROR] DuckDuckGo search failed with error: {str(e)}")
        return {"error": str(e)}

def webscraper(request: WebSearchRequest) -> Response:
    try:
        print(f"[DEBUG] Attempting to scrape URL: {request.url}")
        api_key = os.getenv("COMPOSIO_API_KEY", "ejm8n03dk9bivq6ltf1y9e")
        if not api_key:
            print("[WARNING] No COMPOSIO_API_KEY found in environment variables")
        
        toolset = ComposioToolSet(api_key=api_key)
        raw_response = toolset.execute_action(
            action=Action.FIRECRAWL_SCRAPE_EXTRACT_DATA_LLM,
            params=request.model_dump()
        )
        
        # Check if raw_response has the expected 'data' key and structure
        if not raw_response.get("data") or not isinstance(raw_response["data"], dict):
            error_message = f"Missing or invalid 'data' key in response."
            print(f"[ERROR] {error_message} Full raw response: {raw_response}")
            return Response(
                markdown="",
                metadata=Metadata(),
                error=error_message,
                successful=False
            ).model_dump()
        
        nested_data = raw_response["data"].get("data")
        if not nested_data or not isinstance(nested_data, dict):
            error_message = f"Missing or invalid nested 'data' structure."
            print(f"[ERROR] {error_message} Full raw response: {raw_response}")
            return Response(
                markdown="",
                metadata=Metadata(),
                error=error_message,
                successful=False
            ).model_dump()
        
        try:
            # Now attempt to extract markdown and metadata
            markdown = nested_data["data"]["markdown"]
            metadata = nested_data["data"]["metadata"]
            print(f"[DEBUG] Successfully scraped URL: {request.url} (Metadata title: {metadata.get('title', 'No title')})")
            return Response(
                markdown=markdown,
                metadata=Metadata(**metadata),
                error=raw_response.get("error"),
                successful=raw_response.get("successful", False)
            ).model_dump()
        except KeyError as e:
            print(f"[ERROR] KeyError processing scrape result for {request.url}: {str(e)}")
            print(f"[ERROR] Full raw response: {raw_response}")
            return Response(
                markdown="",
                metadata=Metadata(),
                error=f"KeyError processing response: {str(e)}",
                successful=False
            ).model_dump()
    except Exception as e:
        print(f"[ERROR] Exception during scraping of {request.url}: {str(e)}")
        return Response(
            markdown="",
            metadata=Metadata(),
            error=str(e),
            successful=False
        ).model_dump()

def scrape(url: str, max_depth=2) -> Response:
    print(f"[DEBUG] scrape called for URL: {url}")
    search_request = WebSearchRequest(
        url=url,
        depth=max_depth
    )
    return webscraper(search_request)

# Optional research_tool; not used as only provided links are scraped.
def research_tool(query: str, max_result: int = 5, max_depth: int = 2):
    print(f"[DEBUG] research_tool called with query: {query}")
    search_results = search(query, max_result)
    if "error" in search_results:
        print(f"[ERROR] research_tool search error: {search_results['error']}")
        return search_results
    
    urls = [result["href"] for result in search_results]
    print(f"[DEBUG] research_tool preparing to scrape {len(urls)} URLs")
    
    results = []
    for idx, url in enumerate(urls):
        print(f"[DEBUG] research_tool scraping URL {idx+1}/{len(urls)}: {url}")
        response = scrape(url, max_depth)
        if response.get("successful", False):
            print(f"[DEBUG] Successfully scraped {url}")
        else:
            print(f"[ERROR] Failed to scrape {url}: {response.get('error', 'Unknown error')}")
        results.append(response)
    
    print(f"[DEBUG] research_tool completed with {len(results)} results")
    return results

class WebSearchTools:
    @staticmethod
    def get_league_sources(league: str) -> List[str]:
        sources = {
            "NFL": [
                "https://www.foxsports.com/stories/nfl",
                "https://www.cbssports.com/nfl/2/",
                "https://lastwordonsports.com/nfl/category/nfl-teams/",
                "https://www.nbcsportsbayarea.com/nfl/",
                "https://ninerswire.usatoday.com/lists/",
                "https://sportsnaut.com/nfl/",
                "https://www.nfl.com/"
            ],
            "NBA": [
                "https://scores24.live/en/basketball/l-usa-nba/predictions",
                "https://scores24.live/en/basketball/m-09-04-2025-orlando-magic-boston-celtics-3-prediction",
                # "https://www.bleachernation.com/picks/2025/04/09/magic-vs-celtics-prediction-expert-picks-odds-stats-and-best-bets-wednesday-april-9-2025/",
                "https://www.nbcsports.com/betting/nba/tools/game-predictions",
                "https://www.pickswise.com/nba/picks/",
                "https://www.nba.com/",
                "https://www.espn.com/nba/",
                "https://www.nba.com/news",
                "https://bleacherreport.com/nba",
                "https://www.cbssports.com/nba/expert-picks/"
            ],
            "MLB": [
                "https://www.mlb.com/",
                "https://www.espn.com/mlb/",
                "https://www.cbssports.com/mlb/",
                "https://www.foxsports.com/mlb",
                "https://www.sportingnews.com/us/mlb"
            ],
            "NHL": [
                "https://www.nhl.com/",
                "https://www.espn.com/nhl/",
                "https://www.cbssports.com/nhl/",
                "https://www.foxsports.com/nhl",
                "https://www.sportingnews.com/us/nhl"
            ],
            "EPL": [
                "https://www.premierleague.com/",
                "https://www.skysports.com/premier-league",
                "https://www.espn.com/soccer/league/_/name/eng.1",
                "https://www.bbc.com/sport/football/premier-league"
            ]
        }
        league_sources = sources.get(league.upper(), sources["NFL"])
        print(f"[DEBUG] get_league_sources for {league}: {league_sources}")
        return league_sources
    
    @staticmethod
    def scrape(url: str, max_depth=2) -> dict:
        print(f"[DEBUG] WebSearchTools.scrape called for URL: {url}")
        try:
            response = scrape(url, max_depth)
            if response.get("successful", False):
                print(f"[DEBUG] WebSearchTools.scrape successful for {url}")
            else:
                print(f"[ERROR] WebSearchTools.scrape failed for {url}: {response.get('error', 'Unknown error')}")
            return response
        except Exception as e:
            print(f"[ERROR] Exception in WebSearchTools.scrape for {url}: {str(e)}")
            return {
                "markdown": "",
                "metadata": {},
                "error": str(e),
                "successful": False
            }

if __name__ == "__main__":
    import json
    response = research_tool("What is the best way to learn to code?", max_result=2)
    print(json.dumps(response, indent=4))
