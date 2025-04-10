# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from typing import List, Dict, Optional
# from tools.web_search_tool import WebSearchTools, WebSearchResult

# class NFLGameInfo(BaseModel):
#     teams: List[str] = Field(..., description="Teams playing in the game")
#     date: Optional[str] = Field(None, description="Date of the game")
#     location: Optional[str] = Field(None, description="Location of the game")
#     odds: Optional[Dict] = Field(None, description="Betting odds if available")
#     predictions: Optional[Dict] = Field(None, description="Predictions from the source")
#     source_url: str = Field(..., description="URL of the source")
    
#     def dict(self):
#         """Compatibility method for different pydantic versions"""
#         if hasattr(self, 'model_dump'):
#             return self.model_dump()
#         return super().dict()

# class WebSearchAgent:
#     def __init__(self, search_type: str):
#         self.search_type = search_type
    
#     def perform_search(self, query: str, num_results: int = 5) -> List[WebSearchResult]:
#         """Perform web search using specified search engine"""
#         if self.search_type == 'duckduckgo':
#             results = WebSearchTools.duckduckgo_search(query, num_results)
#         elif self.search_type == 'tavily':
#             results = WebSearchTools.tavily_search(query, num_results)
#         else:
#             raise ValueError(f"Unsupported search type: {self.search_type}")
        
#         return results
    
#     def search_nfl_games(self, teams: Optional[List[str]] = None) -> List[Dict]:
#         """Search for NFL game predictions with optional team filtering"""
#         base_query = "NFL game predictions"
#         if teams:
#             team_query = " ".join(teams)
#             query = f"{base_query} {team_query}"
#         else:
#             query = base_query
        
#         results = self.perform_search(query, num_results=7)
        
#         relevant_links = []
#         for result in results:
#             if result.link:
#                 relevant_links.append(result.link)
        
#         detailed_info = []
#         for link in relevant_links:
#             data = WebSearchTools.scrape_webpage(link)
#             if data:
#                 detailed_info.append(data)
        
#         return detailed_info
    
#     def scrape_official_nfl_sources(self) -> List[Dict]:
#         """Scrape official NFL sources for game information"""
#         return WebSearchTools.scrape_nfl_sources()
    
#     async def extract_game_predictions(self, teams: Optional[List[str]] = None) -> List[NFLGameInfo]:
#         """
#         Extract structured NFL game information and predictions from search results
#         """
#         system_prompt = """
#         You are an expert NFL analyst. Extract precise information about NFL games from the text.
#         Focus on identifying:
#         1. Teams playing in the game
#         2. Date of the game if available
#         3. Location of the game if available
#         4. Betting odds or lines if available
#         5. Expert predictions about the game's outcome
        
#         Return the structured information with proper team names. If information is not found,
#         omit those fields rather than making assumptions.
#         """
#         search_data = self.search_nfl_games(teams)
#         official_data = self.scrape_official_nfl_sources()
#         all_data = official_data  + search_data 

#         combined_texts = []
#         for item in all_data:
#             text = f"Title: {item.get('title', '')}\n\nContent: {item.get('text', '')}\n\nSource: {item.get('source_url', '')}"
#             combined_texts.append(text)
        
#         if not combined_texts:
#             return []

#         extraction_agent = Agent(
#             model="gpt-4o",  
#             system_prompt=system_prompt,
#             result_type=List[NFLGameInfo],
#             retries=3
#         )
        
#         agent_result = await extraction_agent.run({"texts": combined_texts})
        
#         if hasattr(agent_result, 'value'):
#             return agent_result.value
#         elif hasattr(agent_result, 'data'):
#             return agent_result.data
#         elif isinstance(agent_result, list):
#             return agent_result
#         else:
#             return [agent_result]


# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from typing import List, Dict, Optional, Set
# from tools.web_search_tool import WebSearchTools, WebSearchResult

# class GameInfo(BaseModel):
#     teams: List[str] = Field(..., description="Teams playing in the game")
#     date: Optional[str] = Field(None, description="Date of the game")
#     location: Optional[str] = Field(None, description="Location of the game")
#     odds: Optional[Dict] = Field(None, description="Betting odds if available")
#     predictions: Optional[Dict] = Field(None, description="Predictions from the source")
#     source_url: str = Field(..., description="URL of the source")
#     site_name: Optional[str] = Field(None, description="Name of the website source")
#     author_name: Optional[str] = Field(None, description="Author of the prediction if available")
    
#     def dict(self):
#         """Compatibility method for different pydantic versions"""
#         if hasattr(self, 'model_dump'):
#             return self.model_dump()
#         return super().dict()

# class WebSearchAgent:
#     def __init__(self, search_type: str, league: str, provided_links: Optional[List[str]] = None):
#         self.search_type = search_type
#         self.league = league
#         self.provided_links = provided_links or []
    
#     def perform_search(self, query: str, num_results: int = 5) -> List[WebSearchResult]:
#         """Perform web search using specified search engine"""
#         if self.search_type == 'duckduckgo':
#             results = WebSearchTools.duckduckgo_search(query, num_results)
#         elif self.search_type == 'tavily':
#             results = WebSearchTools.tavily_search(query, num_results)
#         else:
#             raise ValueError(f"Unsupported search type: {self.search_type}")
        
#         # Filter results to only use provided links if specified
#         if self.provided_links:
#             results = [r for r in results if any(link in r.link for link in self.provided_links)]
        
#         return results
    
#     def search_league_games(self, teams: Optional[List[str]] = None) -> List[Dict]:
#         """Search for game predictions with optional team filtering"""
#         base_query = f"{self.league} game predictions"
#         if teams:
#             team_query = " ".join(teams)
#             query = f"{base_query} {team_query}"
#         else:
#             query = base_query
        
#         results = self.perform_search(query, num_results=7)
        
#         relevant_links = []
#         # If provided links exist, only use those links
#         if self.provided_links:
#             relevant_links = self.provided_links
#         else:
#             for result in results:
#                 if result.link:
#                     relevant_links.append(result.link)
        
#         detailed_info = []
#         for link in relevant_links:
#             data = WebSearchTools.scrape_webpage(link)
#             if data:
#                 detailed_info.append(data)
        
#         return detailed_info
    
#     def scrape_official_league_sources(self) -> List[Dict]:
#         """Scrape official league sources for game information"""
#         # If provided links exist, only use those links
#         if self.provided_links:
#             return WebSearchTools.scrape_league_sources(self.provided_links)
#         else:
#             league_sources = WebSearchTools.get_league_sources(self.league)
#             return WebSearchTools.scrape_league_sources(league_sources)
    
#     async def extract_game_predictions(self, teams: Optional[List[str]] = None) -> List[GameInfo]:
#         """
#         Extract structured game information and predictions from search results
#         """
#         system_prompt = f"""
#         You are an expert {self.league} analyst. Extract precise information about {self.league} games from the text.
#         Focus on identifying:
#         1. Teams playing in the game
#         2. Date of the game if available
#         3. Location of the game if available
#         4. Betting odds or lines if available
#         5. Expert predictions about the game's outcome
#         6. Name of the website source
#         7. Author name if available
        
#         Return the structured information with proper team names. If information is not found,
#         omit those fields rather than making assumptions.
#         """
        
#         # If provided links exist, only use those
#         search_data = self.search_league_games(teams)
        
#         if not self.provided_links:
#             official_data = self.scrape_official_league_sources()
#             all_data = official_data + search_data
#         else:
#             all_data = search_data
            
#         combined_texts = []
#         for item in all_data:
#             site_name = item.get('title', '').split(' - ')[0] if ' - ' in item.get('title', '') else item.get('title', '')
#             text = f"Title: {item.get('title', '')}\n\nContent: {item.get('text', '')}\n\nSource: {item.get('source_url', '')}\n\nSite Name: {site_name}"
#             combined_texts.append(text)
        
#         if not combined_texts:
#             return []
            
#         extraction_agent = Agent(
#             model="gpt-4o",  
#             system_prompt=system_prompt,
#             result_type=List[GameInfo],
#             retries=3
#         )
        
#         agent_result = await extraction_agent.run({"texts": combined_texts})
        
#         if hasattr(agent_result, 'value'):
#             return agent_result.value
#         elif hasattr(agent_result, 'data'):
#             return agent_result.data
#         elif isinstance(agent_result, list):
#             return agent_result
#         else:
#             return [agent_result]


# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from typing import List, Dict, Optional, Set
# from tools.web_search_tool import WebSearchTools, WebSearchResult

# class GameInfo(BaseModel):
#     teams: List[str] = Field(..., description="Teams playing in the game")
#     date: Optional[str] = Field(None, description="Date of the game")
#     location: Optional[str] = Field(None, description="Location of the game")
#     odds: Optional[Dict] = Field(None, description="Betting odds if available")
#     predictions: Optional[Dict] = Field(None, description="Predictions from the source")
#     source_url: str = Field(..., description="URL of the source")
#     site_name: Optional[str] = Field(None, description="Name of the website source")
#     author_name: Optional[str] = Field(None, description="Author of the prediction if available")
#     summary: Optional[str] = Field(None, description="Summary of the prediction content")
    
#     def dict(self):
#         """Compatibility method for different pydantic versions"""
#         if hasattr(self, 'model_dump'):
#             return self.model_dump()
#         return super().dict()

# class WebSearchAgent:
#     def __init__(self, search_type: str, league: str, provided_links: Optional[List[str]] = None):
#         self.search_type = search_type
#         self.league = league
        
#         # If provided_links are not given, use league sources
#         if not provided_links:
#             self.provided_links = WebSearchTools.get_league_sources(league)
#         else:
#             self.provided_links = provided_links
    
#     def perform_search(self, query: str, num_results: int = 5) -> List[WebSearchResult]:
#         """Perform web search using specified search engine"""
#         if self.search_type == 'duckduckgo':
#             results = WebSearchTools.duckduckgo_search(query, num_results)
#         else:
#             raise ValueError(f"Unsupported search type: {self.search_type}")
        
#         return results
    
#     def search_league_games(self, teams: Optional[List[str]] = None) -> List[Dict]:
#         """Search for game predictions with optional team filtering"""
#         if teams:
#             # Make the query more specific for the matchup
#             team_query = " vs ".join(teams)
#             query = f"{self.league} {team_query} game prediction analysis"
#         else:
#             query = f"{self.league} upcoming games predictions"
        
#         results = self.perform_search(query, num_results=7)
        
#         # Only use provided links for scraping
#         detailed_info = []
#         for link in self.provided_links:
#             data = WebSearchTools.scrape_webpage(link)
#             if data:
#                 detailed_info.append(data)
        
#         return detailed_info
    
#     def scrape_official_league_sources(self) -> List[Dict]:
#         """Scrape official league sources for game information"""
#         return WebSearchTools.scrape_league_sources(self.provided_links)
    
#     async def extract_game_predictions(self, teams: Optional[List[str]] = None) -> List[GameInfo]:
#         """
#         Extract structured game information and predictions from search results
#         """
#         team_specific_prompt = ""
#         if teams:
#             team_specific_prompt = f"""
#             Focus specifically on the matchup between {" and ".join(teams)}. 
#             ONLY return information about this specific matchup.
#             Do not extract information about other games.
#             """
            
#         system_prompt = f"""
#         You are an expert {self.league} analyst. Extract precise information about {self.league} games from the text.
#         Focus on identifying:
#         1. Teams playing in the game
#         2. Date of the game if available
#         3. Location of the game if available
#         4. Betting odds or lines if available
#         5. Expert predictions about the game's outcome
#         6. Name of the website source
#         7. Author name if available
#         {team_specific_prompt}
        
#         Return the structured information with proper team names. If information is not found,
#         omit those fields rather than making assumptions.
        
#         IMPORTANT: Add a 'summary' field with a brief summary of the prediction content.
#         """
        
#         # Use search data from league sources
#         search_data = self.search_league_games(teams)
        
#         # Collect additional data from scraping the official sources
#         official_data = self.scrape_official_league_sources()
        
#         # Combine all data sources
#         all_data = search_data + official_data
            
#         combined_texts = []
#         for item in all_data:
#             site_name = item.get('title', '').split(' - ')[0] if ' - ' in item.get('title', '') else item.get('title', '')
#             text = f"Title: {item.get('title', '')}\n\nContent: {item.get('text', '')}\n\nSource: {item.get('source_url', '')}\n\nSite Name: {site_name}"
#             combined_texts.append(text)
        
#         if not combined_texts:
#             return []
            
#         extraction_agent = Agent(
#             model="gpt-4o",  
#             system_prompt=system_prompt,
#             result_type=List[GameInfo],
#             retries=3
#         )
        
#         agent_result = await extraction_agent.run({"texts": combined_texts})
        
#         # Filter results to only include the specific teams if provided
#         if hasattr(agent_result, 'value'):
#             results = agent_result.value
#         elif hasattr(agent_result, 'data'):
#             results = agent_result.data
#         elif isinstance(agent_result, list):
#             results = agent_result
#         else:
#             results = [agent_result]
            
#         # Additional filtering for specific teams match
#         if teams:
#             filtered_results = []
#             for result in results:
#                 # Check if result teams match the specific teams
#                 result_teams = [team.lower() for team in result.teams]
#                 specific_teams = [team.lower() for team in teams]
                
#                 # Count how many specific teams appear in the result teams
#                 matches = sum(1 for team in specific_teams if any(team in rt for rt in result_teams))
                
#                 # Include only if all specific teams are matched
#                 if matches == len(specific_teams):
#                     filtered_results.append(result)
                    
#             return filtered_results if filtered_results else results  # Return filtered or original if no matches
#         else:
#             return results



# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from typing import List, Dict, Optional
# from tools.web_search_tool import WebSearchTools, WebSearchResult

# class GameInfo(BaseModel):
#     teams: List[str] = Field(..., description="Teams playing in the game")
#     date: Optional[str] = Field(None, description="Date of the game")
#     location: Optional[str] = Field(None, description="Location of the game")
#     odds: Optional[Dict] = Field(None, description="Betting odds if available")
#     predictions: Optional[Dict] = Field(None, description="Predictions from the source")
#     source_url: str = Field(..., description="URL of the source")
#     site_name: Optional[str] = Field(None, description="Name of the website source")
#     author_name: Optional[str] = Field(None, description="Author of the prediction if available")
#     summary: Optional[str] = Field(None, description="Summary of the prediction content")
    
#     def dict(self):
#         if hasattr(self, 'model_dump'):
#             return self.model_dump()
#         return super().dict()

# class WebSearchAgent:
#     def __init__(self, search_type: str, league: str, provided_links: Optional[List[str]] = None):
#         self.search_type = search_type
#         self.league = league
#         if not provided_links:
#             self.provided_links = WebSearchTools.get_league_sources(league)
#             print(f"[DEBUG] WebSearchAgent retrieved league sources for {league}: {self.provided_links}")
#         else:
#             self.provided_links = provided_links
#             print(f"[DEBUG] WebSearchAgent using provided links for {league}: {self.provided_links}")
    
#     def perform_search(self, query: str, num_results: int = 5) -> List[WebSearchResult]:
#         print(f"[DEBUG] Performing search with query: {query}")
#         if self.search_type == 'duckduckgo':
#             results = WebSearchTools.duckduckgo_search(query, num_results)
#         else:
#             raise ValueError(f"Unsupported search type: {self.search_type}")
#         print(f"[DEBUG] Search returned {len(results)} results")
#         return results
    
#     def search_league_games(self, teams: Optional[List[str]] = None) -> List[Dict]:
#         if teams:
#             team_query = " vs ".join(teams)
#             query = f"{self.league} {team_query} game prediction analysis"
#         else:
#             query = f"{self.league} upcoming games predictions"
#         print(f"[DEBUG] search_league_games query: {query}")
        
#         results = self.perform_search(query, num_results=7)
#         print(f"[DEBUG] search_league_games received {len(results)} results from search")
        
#         detailed_info = []
#         for link in self.provided_links:
#             print(f"[DEBUG] Scraping detailed info from provided link: {link}")
#             data = WebSearchTools.scrape_webpage(link)
#             if data:
#                 detailed_info.append(data)
#         print(f"[DEBUG] search_league_games scraped {len(detailed_info)} detailed info entries")
#         return detailed_info
    
#     def scrape_official_league_sources(self) -> List[Dict]:
#         print("[DEBUG] Scraping official league sources...")
#         results = WebSearchTools.scrape_league_sources(self.provided_links)
#         print(f"[DEBUG] scrape_official_league_sources returned {len(results)} entries")
#         return results
    
#     async def extract_game_predictions(self, teams: Optional[List[str]] = None) -> List[GameInfo]:
#         print("[DEBUG] Starting extract_game_predictions...")
#         team_specific_prompt = ""
#         if teams:
#             team_specific_prompt = f"""
#             Focus specifically on the matchup between {" and ".join(teams)}. 
#             ONLY return information about this specific matchup.
#             Do not extract information about other games.
#             """
#             print(f"[DEBUG] extract_game_predictions using team-specific prompt for teams: {teams}")
            
#         system_prompt = f"""
#         You are an expert {self.league} analyst. Extract precise information about {self.league} games from the text.
#         Focus on identifying:
#         1. Teams playing in the game
#         2. Date of the game if available
#         3. Location of the game if available
#         4. Betting odds or lines if available
#         5. Expert predictions about the game's outcome
#         6. Name of the website source
#         7. Author name if available
#         {team_specific_prompt}
        
#         Return the structured information with proper team names. If information is not found,
#         omit those fields rather than making assumptions.
        
#         IMPORTANT: Add a 'summary' field with a brief summary of the prediction content.
#         """
#         print("[DEBUG] extract_game_predictions system_prompt constructed")
        
#         search_data = self.search_league_games(teams)
#         official_data = self.scrape_official_league_sources()
#         print(f"[DEBUG] extract_game_predictions combining {len(search_data)} search_data and {len(official_data)} official_data entries")
        
#         all_data = search_data + official_data
#         combined_texts = []
#         for item in all_data:
#             site_name = item.get('title', '').split(' - ')[0] if ' - ' in item.get('title', '') else item.get('title', '')
#             text = f"Title: {item.get('title', '')}\n\nContent: {item.get('text', '')}\n\nSource: {item.get('source_url', '')}\n\nSite Name: {site_name}"
#             combined_texts.append(text)
#         print(f"[DEBUG] extract_game_predictions prepared {len(combined_texts)} combined text entries for extraction")
        
#         if not combined_texts:
#             return []
            
#         extraction_agent = Agent(
#             model="gpt-4o",  
#             system_prompt=system_prompt,
#             result_type=List[GameInfo],
#             retries=3
#         )
        
#         agent_result = await extraction_agent.run({"texts": combined_texts})
#         print(f"[DEBUG] extraction_agent returned: {agent_result}")
        
#         if hasattr(agent_result, 'value'):
#             results = agent_result.value
#         elif hasattr(agent_result, 'data'):
#             results = agent_result.data
#         elif isinstance(agent_result, list):
#             results = agent_result
#         else:
#             results = [agent_result]
            
#         if teams:
#             filtered_results = []
#             for result in results:
#                 result_teams = [team.lower() for team in result.teams]
#                 specific_teams = [team.lower() for team in teams]
#                 matches = sum(1 for team in specific_teams if any(team in rt for rt in result_teams))
#                 if matches == len(specific_teams):
#                     filtered_results.append(result)
#             print(f"[DEBUG] extract_game_predictions filtered down to {len(filtered_results)} results for teams: {teams}")
#             return filtered_results if filtered_results else results
#         else:
#             return results




# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from typing import List, Dict, Optional
# from tools.web_search_tool import WebSearchTools, Response
# import json

# from pydantic_ai.providers.openai import OpenAIProvider
# from pydantic_ai.models import openai
# provider = OpenAIProvider(
#     base_url='https://openrouter.ai/api/v1',
#     api_key='OPENROUTER_API_KEY'
# )
# model = openai.OpenAIModel(
#     "openrouter/quasar-alpha",
#     provider=provider
# )

# class GameInfo(BaseModel):
#     teams: List[str] = Field(..., description="Teams playing in the game")
#     date: Optional[str] = Field(None, description="Date of the game")
#     location: Optional[str] = Field(None, description="Location of the game")
#     odds: Optional[Dict] = Field(None, description="Betting odds if available")
#     predictions: Optional[Dict] = Field(None, description="Predictions from the source")
#     source_url: str = Field(..., description="URL of the source")
#     site_name: Optional[str] = Field(None, description="Name of the website source")
#     author_name: Optional[str] = Field(None, description="Author of the prediction if available")
#     summary: Optional[str] = Field(None, description="Summary of the prediction content")
    
#     def dict(self):
#         if hasattr(self, 'model_dump'):
#             return self.model_dump()
#         return super().dict()

# class WebSearchAgent:
#     def __init__(self, search_type: str, league: str, provided_links: Optional[List[str]] = None):
#         self.search_type = search_type
#         self.league = league
#         if not provided_links:
#             self.provided_links = WebSearchTools.get_league_sources(league)
#             print(f"[DEBUG] WebSearchAgent retrieved league sources for {league}: {self.provided_links}")
#         else:
#             self.provided_links = provided_links
#             print(f"[DEBUG] WebSearchAgent using provided links for {league}: {self.provided_links}")
    
#     def perform_search(self, query: str, num_results: int = 5) -> List:
#         # External search is disabled. Only provided links will be scraped.
#         print(f"[DEBUG] perform_search called with query: {query} (external search is disabled)")
#         return []
    
#     async def extract_game_predictions(self, teams: Optional[List[str]] = None) -> List[GameInfo]:
#         print("[DEBUG] Starting extract_game_predictions using provided links only...")
#         team_specific_prompt = ""
#         if teams:
#             # Relaxed instructions allow extraction of any prediction information related to the teams
#             team_specific_prompt = f"""
#             Focus on extracting information regarding the matchup between {teams[0]} and {teams[1]}. 
#             If detailed prediction data is available for this matchup, include it. 
#             Otherwise, extract any relevant prediction information about the game.
#             If any output variable is missing, use "none" as the default value.
#             """
#             print(f"[DEBUG] extract_game_predictions using relaxed team-specific prompt for teams: {teams}")
            
#         system_prompt = f"""
#         You are an expert {self.league} analyst. Extract structured prediction information from the provided text regarding season games.
#         Your task is to identify:
#         1. Teams playing in the game (team_A and team_B)
#         2. Date of the game if available
#         3. Location of the game if available
#         4. Betting odds or lines if available
#         5. Expert predictions about the game's outcome
#         6. Name of the website source
#         7. Author name if available
#         8. A brief summary of the prediction content

#         {team_specific_prompt}
        
#         Return the structured information in the following JSON format:
#         {{
#         "teams": [team_A, team_B],
#         "date": <string or "none">,
#         "location": <string or "none">,
#         "odds": <object or "none">,
#         "predictions": <object or "none">,
#         "source_url": <string or "none">,
#         "site_name": <string or "none">,
#         "author_name": <string or "none">,
#         "summary": <string or "none">
#         }}
        
#         If the relevant information is not present, omit the field or set its value to "none".
#         If no prediction information is available at all, return an empty list.
#         """
#         print("[DEBUG] extract_game_predictions system_prompt constructed")
        
#         # Iterate over the provided links for scraping.
#         official_data = []
#         for link_index, link in enumerate(self.provided_links):
#             print(f"[DEBUG] Scraping provided link ({link_index+1}/{len(self.provided_links)}): {link}")
#             try:
#                 response: dict = WebSearchTools.scrape(link)
#                 if response and response.get("successful", False):
#                     site_name = response.get("metadata", {}).get("title", "")
#                     data = {
#                         'title': site_name,
#                         'text': response.get("markdown", ""),
#                         'source_url': link
#                     }
#                     official_data.append(data)
#                     print(f"[DEBUG] Successfully scraped {link} (title: {site_name[:30]}...)")
#                 else:
#                     error_msg = response.get("error", "Unknown error") if response else "Empty response"
#                     print(f"[ERROR] Failed to scrape {link}: {error_msg}")
#             except Exception as e:
#                 print(f"[ERROR] Exception scraping {link}: {str(e)}")
        
#         print(f"[DEBUG] extract_game_predictions scraped {len(official_data)}/{len(self.provided_links)} entries from provided links")
        
#         if not official_data:
#             print("[WARNING] No content was successfully scraped from any of the provided links")
#             return []
        
        
#         summarization_prompt = """
#         You are a sports analyst. Read the following article content and provide a concise summary (max 150 words) of any predictions, key stats, or insights related to upcoming games. If it's unrelated, return: "No relevant prediction".
#         """

#         summary_agent = Agent(
#             model=model,
#             system_prompt=summarization_prompt,
#             result_type=str,
#             retries=2
#         )

#         summarized_entries = []

#         for idx, item in enumerate(official_data):
#             print(f"[DEBUG] Summarizing entry #{idx+1}: {item['title'][:50]}...")
#             input_text = f"Title: {item['title']}\n\nContent: {item['text']}"
#             try:
#                 result = await summary_agent.run({"text": input_text})
#                 summary = result.value if hasattr(result, "value") else result
#                 summarized_entry = {
#                     "text": item["text"],
#                     "title": item["title"],
#                     "source_url": item["source_url"],
#                     "summary": summary
#                 }
#                 summarized_entries.append(summarized_entry)
#                 print(f"[DEBUG] Summary #{idx+1} done.")
#             except Exception as e:
#                 print(f"[ERROR] Summarization failed for entry #{idx+1}: {str(e)}")

#         # combined_texts = []
#         # for item in official_data:
#         # site_name = item.get('title', 'none')
#         # text = f"Title: {item.get('title', 'none')}\n\nContent: {item.get('text', '')}\n\nSource: {item.get('source_url', 'none')}\n\nSite Name: {site_name}"
#         # combined_texts.append(text)
#         # print(f"[DEBUG] extract_game_predictions prepared {len(combined_texts)} combined text entries for extraction")

#         # # Save to file
#         # debug_file_path = "combined_texts_debug.txt"
#         # try:
#         #     with open(debug_file_path, "w", encoding="utf-8") as f:
#         #         for idx, ct in enumerate(combined_texts, start=1):
#         #             f.write(f"[Combined Text #{idx}]\n{ct}\n{'-'*80}\n")
#         #     print(f"[DEBUG] Combined texts successfully written to: {debug_file_path}")
#         # except Exception as e:
#         #     print(f"[ERROR] Failed to write combined texts to file: {e}")


#         # # Added print to view the content of combined_texts
#         # print("[DEBUG] Combined Texts Content:")
#         # for idx, ct in enumerate(combined_texts, start=1):
#         #     print(f"[DEBUG] Combined Text #{idx}:\n{ct}\n{'-'*40}")
        
#         # if not combined_texts:
#         #     return []
            
#         # extraction_agent = Agent(
#         #     model=model,  
#         #     system_prompt=system_prompt,
#         #     result_type=List[GameInfo],
#         #     retries=3
#         # )
        
#         print(f"[DEBUG] Sending {len(combined_texts)} texts to extraction agent")
#         agent_result = await extraction_agent.run({"texts": combined_texts})
#         print(f"[DEBUG] extraction_agent returned result of type: {type(agent_result)}")
        
#         if hasattr(agent_result, 'value'):
#             results = agent_result.value
#         elif hasattr(agent_result, 'data'):
#             results = agent_result.data
#         elif isinstance(agent_result, list):
#             results = agent_result
#         else:
#             results = [agent_result]
            
#         print(f"[DEBUG] extraction_agent returned {len(results)} initial results")
#         return results


from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Dict, Optional
from tools.web_search_tool import WebSearchTools, Response
import json
import os

from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models import openai

provider = OpenAIProvider(
    base_url='https://openrouter.ai/api/v1',
    api_key='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' #os.environ.get("OPENROUTER_API_KEY") 
)
model = openai.OpenAIModel(
    "openrouter/quasar-alpha",
    provider=provider
)


class GameSummary(BaseModel):
    summary: str
    site_name: str
    source_url: str
    author_name: str


class GameInfo(BaseModel):
    teams: List[str] = Field(..., description="Teams playing in the game")
    date: Optional[str] = Field(None, description="Date of the game")
    location: Optional[str] = Field(None, description="Location of the game")
    odds: Optional[Dict] = Field(None, description="Betting odds if available")
    predictions: Optional[Dict] = Field(None, description="Predictions from the source")
    source_url: str = Field(..., description="URL of the source")
    site_name: Optional[str] = Field(None, description="Name of the website source")
    author_name: Optional[str] = Field(None, description="Author of the prediction if available")
    summary: Optional[str] = Field(None, description="Summary of the prediction content")

    def dict(self):
        if hasattr(self, 'model_dump'):
            return self.model_dump()
        return super().dict()


class WebSearchAgent:
    def __init__(self, search_type: str, league: str, provided_links: Optional[List[str]] = None):
        self.search_type = search_type
        self.league = league
        if not provided_links:
            self.provided_links = WebSearchTools.get_league_sources(league)
            print(f"[DEBUG] WebSearchAgent retrieved league sources for {league}: {self.provided_links}")
        else:
            self.provided_links = provided_links
            print(f"[DEBUG] WebSearchAgent using provided links for {league}: {self.provided_links}")

    def perform_search(self, query: str, num_results: int = 5) -> List:
        # External search is disabled. Only provided links will be scraped.
        print(f"[DEBUG] perform_search called with query: {query} (external search is disabled)")
        return []

    async def extract_game_predictions(self, teams: Optional[List[str]] = None) -> List[Dict]:
        print("[DEBUG] Starting extract_game_predictions using provided links only...")
        team_specific_prompt = ""
        if teams:
            team_specific_prompt = f"""
            Focus on extracting information regarding the matchup between {teams[0]} and {teams[1]}. 
            If detailed prediction data is available for this matchup, include it. 
            Otherwise, extract any relevant prediction information about the game.
            """

        summarization_prompt = """
        
        You are a sports analyst. Read the following article content and provide a concise summary (max 300 words) focusing on any prediction insights, betting tips, or game analysis. If there are no clear predictions, please mention that no detailed prediction information is available.

        """
        # You are a sports analyst. Read the following article content and provide a concise summary (max 300 words) of any predictions, key stats, or insights related to upcoming games. 
        # If no predictions are found, respond with: "No relevant prediction".



        summary_agent = Agent(
            model=model,
            system_prompt=summarization_prompt,
            result_type=str,
            retries=2
        )

        official_data = []

        for link_index, link in enumerate(self.provided_links):
            print(f"[DEBUG] Scraping link ({link_index + 1}/{len(self.provided_links)}): {link}")
            try:
                response: dict = WebSearchTools.scrape(link)
                if response and response.get("successful", False):
                    site_name = response.get("metadata", {}).get("title", "")
                    markdown_text = response.get("markdown", "")
                    input_text = f"Title: {site_name}\n\nContent: {markdown_text}"
                    summary_result = await summary_agent.run({"text": input_text})
                    summary = summary_result.value if hasattr(summary_result, "value") else str(summary_result)

                    item = {
                        "title": site_name or "none",
                        "text": markdown_text,
                        "source_url": link,
                        "site_name": site_name or "none",
                        "summary": summary
                    }
                    official_data.append(item)
                    print(f"[DEBUG] Summary for link done: {link}")
                else:
                    error_msg = response.get("error", "Unknown error") if response else "Empty response"
                    print(f"[ERROR] Failed to scrape {link}: {error_msg}")
            except Exception as e:
                print(f"[ERROR] Exception scraping {link}: {str(e)}")

        print(f"[DEBUG] Completed summarizing {len(official_data)}/{len(self.provided_links)} articles")

        if not official_data:
            print("[WARNING] No content was successfully scraped or summarized.")
            return []

        # Write debug file
        try:
            with open("summarized_entries_debug.txt", "w", encoding="utf-8") as f:
                for idx, entry in enumerate(official_data, 1):
                    f.write(f"[Summary #{idx}]\n")
                    f.write(json.dumps({
                        "title": entry["title"],
                        "text": entry["text"],
                        "source_url": entry["source_url"],
                        "site_name": entry["site_name"],
                        "summary": str(entry["summary"])
                    }, indent=2))
                    f.write("\n" + "-" * 80 + "\n")
            print("[DEBUG] Written summaries to summarized_entries_debug.txt")
        except Exception as e:
            print(f"[ERROR] Failed to write debug file: {e}")

        return official_data  # Each entry has text + summary + metadata for manager agent
