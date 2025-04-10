# import asyncio
# from typing import Dict, Any, List, Optional
# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from datetime import datetime, timedelta
# from .web_search_agent import WebSearchAgent, NFLGameInfo

# class Teams(BaseModel):
#     team_A: str
#     # team_A_win: bool
#     team_B: str
#     winner: str = Field(description="Name of the predicted winning team")
#     # team_B_win: bool

# class Predictions(BaseModel):
#     predictions: str = Field(description="Predicted outcome for each game")
#     reasoning: str
#     teams: Teams
#     sources: List[str]

# class NoGamesFound(BaseModel):
#     message: str
#     reason: str

# class ManagerAgent:
#     def __init__(self, teams: Optional[List[str]] = None):
#         self.teams = teams
#         self.duckduckgo_agent = WebSearchAgent('duckduckgo')
#         self.tavily_agent = WebSearchAgent('tavily')
    
#     async def check_upcoming_games(self) -> Dict[str, Any]:
#         """Check if there are any upcoming NFL games"""
#         now = datetime.now()
        
       
#         if self.teams:
#             teams_str = " vs ".join(self.teams)
#             query = f"NFL {teams_str} game schedule 2025 next game date time"
#             # query = f"NFL {teams_str} game schedule next 7 days"
#         else:
#             query = f"NFL games schedule next 7 days"
        
        
#         search_agent = WebSearchAgent('duckduckgo')
#         results = search_agent.perform_search(query, num_results=5)
        
        
#         system_prompt = """
#         You are an NFL schedule expert. Analyze the provided search results to determine if there are any NBA games 
#         scheduled for today or in the upcoming 7 days. Today's date is {today}.
        
#         If you can identify specific upcoming games, respond with:
#         {{"has_games": true, "games": [list of games]}}
        
#         If there are no games scheduled, respond with:
#         {{"has_games": false, "reason": "Specific reason why (off-season, no games today, etc.)"}}
        
#         Be accurate and conservative - only indicate games exist if you have clear evidence.
#         """
        
        
#         search_text = "\n\n".join([
#             f"Title: {r.title}\nSnippet: {r.snippet}\nLink: {r.link}" 
#             for r in results if r.title and r.snippet
#         ])
        
       
#         schedule_agent = Agent(
#             model="gpt-4o",
#             system_prompt=system_prompt.format(today=now.strftime("%A, %B %d, %Y")),
#             result_type=Dict[str, Any],
#             retries=15
#         )
        
#         agent_result = await schedule_agent.run(search_text)
        
#         if hasattr(agent_result, 'value'):
#             return agent_result.value
#         elif hasattr(agent_result, 'data'):
#             return agent_result.data
#         else:
#             return agent_result
    
#     async def gather_game_data(self) -> List[NFLGameInfo]:
#         """Gather data from both search agents"""
#         data = await self.duckduckgo_agent.extract_game_predictions(self.teams)
#         if not data or len(data) < 2:
#             tavily_data = await self.tavily_agent.extract_game_predictions(self.teams)
#             # Combine unique results
#             existing_sources = {item.source_url for item in data}
#             for item in tavily_data:
#                 if item.source_url not in existing_sources:
#                     data.append(item)
        
#         return data
    
#     async def analyze_predictions(self, game_data: List[NFLGameInfo]) -> List[Predictions]:
#         """Analyze gathered data and generate predictions"""
#         if not game_data:
#             return []
#         try:
#             system_prompt = """
#             You are an expert NFL analyst. Based on the provided game information, generate accurate predictions
#             for each NFL game. For each matchup:
            
#             1. Identify the two teams (team_A and team_B)
#             2. Determine which team is more likely to win based on the provided data
#             3. Provide detailed reasoning for your prediction
#             4. Cite the sources you've used for each prediction
            
#             Return predictions in the specified format, ensuring boolean values for team_A_win and team_B_win
#             (one must be True and one must be False).
#             """
            
#             analysis_agent = Agent(
#                 model="gpt-4o",
#                 system_prompt=system_prompt,
#                 result_type=List[Predictions],
#                 retries=7
#             )

#             agent_result = await analysis_agent.run({"game_data": [game.dict() for game in game_data]})
            
#             if hasattr(agent_result, 'value'):
#                 return agent_result.value
#             elif hasattr(agent_result, 'data'):
#                 return agent_result.data
#             else:
#                 return agent_result
#         except Exception as e:
#             print(f"Error during prediction analysis: {str(e)}")
#             return self.create_fallback_predictions(game_data)
        
#     def create_fallback_predictions(self, game_data: List[NFLGameInfo]) -> List[Predictions]:
#         """Create simple predictions when the agent-based approach fails"""
#         results = []
#         for game in game_data:
#             teams_mentioned = set()
#             for team in self.teams if self.teams else []:
#                 if team.lower() in game.summary.lower():
#                     teams_mentioned.add(team)
                    
#             if len(teams_mentioned) >= 2:
#                 team_list = list(teams_mentioned)
#                 results.append(Predictions(
#                     predictions=f"Prediction for {team_list[0]} vs {team_list[1]}",
#                     reasoning="Based on limited analysis due to processing constraints",
#                     teams=Teams(
#                         team_A=team_list[0],
#                         team_A_win=True, 
#                         team_B=team_list[1],
#                         team_B_win=False 
#                     ),
#                     sources=[game.source_url]
#                 ))
#         return results

#     async def execute_prediction(self) -> Dict[str, Any]:
#         """Execute the full prediction process with game availability check"""
#         print(f"DEBUG: Checking for NFL games: {self.teams if self.teams else 'all teams'}")
#         # Step 1: Check for upcoming games
#         game_check = await self.check_upcoming_games()
        
#         if not game_check.get('has_games', False):
#             reason = game_check.get('reason', 'No upcoming games found')
#             if self.teams:
#                 message = f"There are no upcoming games for {' vs '.join(self.teams)}"
#             else:
#                 message = "There are no upcoming NFL games"
            
#             return {
#                 "status": "no_games",
#                 "message": message,
#                 "reason": reason
#             }
            
#         #  Games found, gather data from search agents
#         print("DEBUG: Found upcoming games, gathering prediction data")
#         game_data = await self.gather_game_data()
        
#         if not game_data:
#             print("WARNING: No game data found despite games being scheduled")
#             return {
#                 "status": "no_data",
#                 "message": "Games are scheduled but no prediction data was found",
#                 "reason": "Unable to retrieve predictions"
#             }
            
#         print(f"DEBUG: Found data for {len(game_data)} games")

#         def validate_predictions(pred_list):
#             valid_predictions = []
#             for p in pred_list:
#                 try:
#                     validated = Predictions(**p.dict() if hasattr(p, 'dict') else p)
#                     valid_predictions.append(validated)
#                 except Exception as e:
#                     print(f"Skipping invalid prediction: {str(e)}")
#             return valid_predictions

               
#         # Analyze data and generate predictions
#         predictions = await self.analyze_predictions(game_data)
#         validated_predictions = validate_predictions(predictions)
#         return {
#             "status": "success",
#             "predictions": validated_predictions
#         }

        

# # async def predict_games(teams: Optional[List[str]] = None) -> Dict[str, Any]:
# #     """Function to be called from main.py"""
# #     manager = ManagerAgent(teams)
# #     result = await manager.execute_prediction()
# #     return result

# async def predict_games(teams: Optional[List[str]] = None) -> Dict[str, Any]:
#     """Function to be called from main.py"""
#     try:
#         manager = ManagerAgent(teams)
#         max_retries = 3
#         retry_count = 0
        
#         while retry_count < max_retries:
#             try:
#                 result = await manager.execute_prediction()
#                 return result
#             except Exception as e:
#                 retry_count += 1
#                 print(f"Attempt {retry_count} failed: {str(e)}")
#                 await asyncio.sleep(1)
#         return {
#             "status": "error",
#             "message": f"Failed after {max_retries} attempts"
#         }
        
#     except Exception as e:
#         return {
#             "status": "error",
#             "message": f"Error in predict_games: {str(e)}"
#         }


# import asyncio
# from typing import Dict, Any, List, Optional
# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from datetime import datetime, timedelta
# from .web_search_agent import WebSearchAgent, GameInfo

# class Teams(BaseModel):
#     team_A: str
#     team_B: str
#     winner: str = Field(description="Name of the predicted winning team")

# class Predictions(BaseModel):
#     site_name: str = Field(description="Name of the website source")
#     site_url: str = Field(description="URL of the source website")
#     author_name: Optional[str] = Field(None, description="Author of the prediction if available")
#     team_A: str = Field(description="First team in the matchup")
#     team_B: str = Field(description="Second team in the matchup")
#     winner: str = Field(description="Name of the predicted winning team")
#     reasoning: str = Field(description="Reasoning behind the prediction")

# class NoGamesFound(BaseModel):
#     message: str
#     reason: str

# class ManagerAgent:
#     def __init__(self, league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None):
#         self.league = league
#         self.teams = teams
#         self.provided_links = provided_links
#         self.duckduckgo_agent = WebSearchAgent('duckduckgo', league, provided_links)
#         self.tavily_agent = WebSearchAgent('tavily', league, provided_links)
    
#     async def check_upcoming_games(self) -> Dict[str, Any]:
#         """Check if there are any upcoming games for the specified league"""
#         now = datetime.now()
        
#         if self.teams:
#             teams_str = " vs ".join(self.teams)
#             query = f"{self.league} {teams_str} game schedule next 7 days"
#         else:
#             query = f"{self.league} games schedule next 7 days"
        
#         search_agent = WebSearchAgent('duckduckgo', self.league, self.provided_links)
#         results = search_agent.perform_search(query, num_results=5)
        
#         system_prompt = f"""
#         You are a {self.league} schedule expert. Analyze the provided search results to determine if there are any {self.league} games 
#         scheduled for today or in the upcoming 7 days. Today's date is {{today}}.
        
#         If you can identify specific upcoming games, respond with:
#         {{{{\"has_games\": true, \"games\": [list of games]}}}}
        
#         If there are no games scheduled, respond with:
#         {{{{\"has_games\": false, \"reason\": \"Specific reason why (off-season, no games today, etc.)\"}}}}
        
#         Be accurate and conservative - only indicate games exist if you have clear evidence.
#         """
        
#         search_text = "\n\n".join([
#             f"Title: {r.title}\nSnippet: {r.snippet}\nLink: {r.link}" 
#             for r in results if r.title and r.snippet
#         ])
        
#         schedule_agent = Agent(
#             model="gpt-4o",
#             system_prompt=system_prompt.format(today=now.strftime("%A, %B %d, %Y")),
#             result_type=Dict[str, Any],
#             retries=15
#         )
        
#         agent_result = await schedule_agent.run(search_text)
        
#         if hasattr(agent_result, 'value'):
#             return agent_result.value
#         elif hasattr(agent_result, 'data'):
#             return agent_result.data
#         else:
#             return agent_result
    
#     async def gather_game_data(self) -> List[GameInfo]:
#         """Gather data from both search agents"""
#         data = await self.duckduckgo_agent.extract_game_predictions(self.teams)
#         if not data or len(data) < 2:
#             tavily_data = await self.tavily_agent.extract_game_predictions(self.teams)
#             # Combine unique results
#             existing_sources = {item.source_url for item in data}
#             for item in tavily_data:
#                 if item.source_url not in existing_sources:
#                     data.append(item)
        
#         return data
    
#     async def analyze_predictions(self, game_data: List[GameInfo]) -> List[Predictions]:
#         """Analyze gathered data and generate predictions"""
#         if not game_data:
#             return []
#         try:
#             system_prompt = f"""
#             You are an expert {self.league} analyst. Based on the provided game information, generate accurate predictions
#             for each {self.league} game. For each matchup:
            
#             1. Identify the two teams (team_A and team_B)
#             2. Determine which team is more likely to win based on the provided data
#             3. Provide detailed reasoning for your prediction
#             4. Include the site_name, site_url, and author_name (if available) for each prediction
            
#             Format your predictions as requested in the JSON structure with the following fields:
#             - site_name: Name of the website source
#             - site_url: URL of the source website
#             - author_name: Author of the prediction (if available)
#             - team_A: First team in the matchup
#             - team_B: Second team in the matchup
#             - winner: Name of the predicted winning team
#             - reasoning: Detailed reasoning for the prediction
#             """
            
#             analysis_agent = Agent(
#                 model="gpt-4o",
#                 system_prompt=system_prompt,
#                 result_type=List[Predictions],
#                 retries=7
#             )
#             agent_result = await analysis_agent.run({"game_data": [game.dict() for game in game_data]})
            
#             if hasattr(agent_result, 'value'):
#                 return agent_result.value
#             elif hasattr(agent_result, 'data'):
#                 return agent_result.data
#             else:
#                 return agent_result
#         except Exception as e:
#             print(f"Error during prediction analysis: {str(e)}")
#             return self.create_fallback_predictions(game_data)
        
#     def create_fallback_predictions(self, game_data: List[GameInfo]) -> List[Predictions]:
#         """Create simple predictions when the agent-based approach fails"""
#         results = []
#         for game in game_data:
#             teams_mentioned = set()
#             for team in self.teams if self.teams else []:
#                 if team.lower() in game.summary.lower() if hasattr(game, 'summary') else '':
#                     teams_mentioned.add(team)
                    
#             if len(teams_mentioned) >= 2:
#                 team_list = list(teams_mentioned)
#                 results.append(Predictions(
#                     site_name=game.site_name if hasattr(game, 'site_name') else "Unknown",
#                     site_url=game.source_url,
#                     author_name=game.author_name if hasattr(game, 'author_name') else None,
#                     team_A=team_list[0],
#                     team_B=team_list[1],
#                     winner=team_list[0],  # Default prediction
#                     reasoning="Based on limited analysis due to processing constraints"
#                 ))
#         return results
        
#     async def execute_prediction(self) -> Dict[str, Any]:
#         """Execute the full prediction process with game availability check"""
#         print(f"DEBUG: Checking for {self.league} games: {self.teams if self.teams else 'all teams'}")
        
#         # Step 1: Check for upcoming games
#         game_check = await self.check_upcoming_games()
        
#         if not game_check.get('has_games', False):
#             reason = game_check.get('reason', f'No upcoming {self.league} games found')
#             if self.teams:
#                 message = f"There are no upcoming {self.league} games for {' vs '.join(self.teams)}"
#             else:
#                 message = f"There are no upcoming {self.league} games"
            
#             return {
#                 "status": "no_games",
#                 "message": message,
#                 "reason": reason
#             }
            
#         # Games found, gather data from search agents
#         print(f"DEBUG: Found upcoming {self.league} games, gathering prediction data")
#         game_data = await self.gather_game_data()
        
#         if not game_data:
#             print(f"WARNING: No {self.league} game data found despite games being scheduled")
#             return {
#                 "status": "no_data",
#                 "message": f"{self.league} games are scheduled but no prediction data was found",
#                 "reason": "Unable to retrieve predictions"
#             }
            
#         print(f"DEBUG: Found data for {len(game_data)} {self.league} games")
        
#         def validate_predictions(pred_list):
#             valid_predictions = []
#             for p in pred_list:
#                 try:
#                     validated = Predictions(**p.dict() if hasattr(p, 'dict') else p)
#                     valid_predictions.append(validated)
#                 except Exception as e:
#                     print(f"Skipping invalid prediction: {str(e)}")
#             return valid_predictions
               
#         # Analyze data and generate predictions
#         predictions = await self.analyze_predictions(game_data)
#         validated_predictions = validate_predictions(predictions)
#         return {
#             "status": "success",
#             "predictions": validated_predictions
#         }

# async def predict_games(league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None) -> Dict[str, Any]:
#     """Function to be called from main.py"""
#     try:
#         manager = ManagerAgent(league, teams, provided_links)
#         max_retries = 3
#         retry_count = 0
        
#         while retry_count < max_retries:
#             try:
#                 result = await manager.execute_prediction()
#                 return result
#             except Exception as e:
#                 retry_count += 1
#                 print(f"Attempt {retry_count} failed: {str(e)}")
#                 await asyncio.sleep(1)
#         return {
#             "status": "error",
#             "message": f"Failed after {max_retries} attempts"
#         }
        
#     except Exception as e:
#         return {
#             "status": "error",
#             "message": f"Error in predict_games: {str(e)}"
#         }




# import asyncio
# from typing import Dict, Any, List, Optional
# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from datetime import datetime, timedelta
# from .web_search_agent import WebSearchAgent, GameInfo
# from tools.web_search_tool import WebSearchTools

# class Teams(BaseModel):
#     team_A: str
#     team_B: str
#     winner: str = Field(description="Name of the predicted winning team")

# class Predictions(BaseModel):
#     site_name: str = Field(description="Name of the website source")
#     site_url: str = Field(description="URL of the source website")
#     author_name: Optional[str] = Field(None, description="Author of the prediction if available")
#     team_A: str = Field(description="First team in the matchup")
#     team_B: str = Field(description="Second team in the matchup")
#     winner: str = Field(description="Name of the predicted winning team")
#     reasoning: str = Field(description="Reasoning behind the prediction")

# class NoGamesFound(BaseModel):
#     message: str
#     reason: str

# class ManagerAgent:
#     def __init__(self, league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None):
#         self.league = league
#         self.teams = teams
        
#         # Get league sources if not provided
#         if not provided_links:
#             self.provided_links = WebSearchTools.get_league_sources(league)
#         else:
#             self.provided_links = provided_links
            
#         self.duckduckgo_agent = WebSearchAgent('duckduckgo', league, self.provided_links)
    
#     async def check_upcoming_games(self) -> Dict[str, Any]:
#         """Check if there are any upcoming games for the specified league"""
#         now = datetime.now()
        
#         if self.teams:
#             teams_str = " vs ".join(self.teams)
#             query = f"{self.league} {teams_str} game schedule next 7 days"
#         else:
#             query = f"{self.league} games schedule next 7 days"
        
#         search_agent = WebSearchAgent('duckduckgo', self.league, self.provided_links)
#         results = search_agent.perform_search(query, num_results=5)
        
#         system_prompt = f"""
#         You are a {self.league} schedule expert. Analyze the provided search results to determine if there are any {self.league} games 
#         scheduled for today or in the upcoming 7 days. Today's date is {{today}}.
        
#         If you can identify specific upcoming games, respond with:
#         {{{{\"has_games\": true, \"games\": [list of games]}}}}
        
#         If there are no games scheduled, respond with:
#         {{{{\"has_games\": false, \"reason\": \"Specific reason why (off-season, no games today, etc.)\"}}}}
        
#         Be accurate and conservative - only indicate games exist if you have clear evidence.
#         """
        
#         search_text = "\n\n".join([
#             f"Title: {r.title}\nSnippet: {r.snippet}\nLink: {r.link}" 
#             for r in results if r.title and r.snippet
#         ])
        
#         schedule_agent = Agent(
#             model="gpt-4o",
#             system_prompt=system_prompt.format(today=now.strftime("%A, %B %d, %Y")),
#             result_type=Dict[str, Any],
#             retries=15
#         )
        
#         agent_result = await schedule_agent.run(search_text)
        
#         if hasattr(agent_result, 'value'):
#             return agent_result.value
#         elif hasattr(agent_result, 'data'):
#             return agent_result.data
#         else:
#             return agent_result
    
#     async def gather_game_data(self) -> List[GameInfo]:
#         """Gather data from search agent"""
#         data = await self.duckduckgo_agent.extract_game_predictions(self.teams)
#         return data
    
#     async def analyze_predictions(self, game_data: List[GameInfo]) -> List[Predictions]:
#         """Analyze gathered data and generate predictions"""
#         if not game_data:
#             return []
            
#         try:
#             # Build a system prompt that emphasizes the specific teams if provided
#             team_specific_instructions = ""
#             if self.teams and len(self.teams) == 2:
#                 team_specific_instructions = f"""
#                 FOCUS ONLY ON THE MATCHUP BETWEEN {self.teams[0]} and {self.teams[1]}.
                
#                 Any predictions MUST be for this specific matchup only. Do not make predictions for any other games.
#                 team_A should be {self.teams[0]} and team_B should be {self.teams[1]}.
#                 """
            
#             system_prompt = f"""
#             You are an expert {self.league} analyst. Based on the provided game information, generate accurate predictions
#             for {self.league} games. For each matchup:
            
#             1. Identify the two teams (team_A and team_B)
#             2. Determine which team is more likely to win based on the provided data
#             3. Provide detailed reasoning for your prediction
#             4. Include the site_name, site_url, and author_name (if available) for each prediction
            
#             {team_specific_instructions}
            
#             Format your predictions as requested in the JSON structure with the following fields:
#             - site_name: Name of the website source
#             - site_url: URL of the source website
#             - author_name: Author of the prediction (if available)
#             - team_A: First team in the matchup
#             - team_B: Second team in the matchup
#             - winner: Name of the predicted winning team
#             - reasoning: Detailed reasoning for the prediction
#             """
            
#             analysis_agent = Agent(
#                 model="gpt-4o",
#                 system_prompt=system_prompt,
#                 result_type=List[Predictions],
#                 retries=7
#             )
#             agent_result = await analysis_agent.run({"game_data": [game.dict() for game in game_data]})
            
#             if hasattr(agent_result, 'value'):
#                 predictions = agent_result.value
#             elif hasattr(agent_result, 'data'):
#                 predictions = agent_result.data
#             else:
#                 predictions = agent_result
                
#             # If we have specific teams, filter predictions to match only those teams
#             if self.teams and len(self.teams) == 2:
#                 filtered_predictions = []
#                 for pred in predictions:
#                     teams_match = (
#                         (pred.team_A.lower() in self.teams[0].lower() or self.teams[0].lower() in pred.team_A.lower()) and
#                         (pred.team_B.lower() in self.teams[1].lower() or self.teams[1].lower() in pred.team_B.lower())
#                     ) or (
#                         (pred.team_A.lower() in self.teams[1].lower() or self.teams[1].lower() in pred.team_A.lower()) and
#                         (pred.team_B.lower() in self.teams[0].lower() or self.teams[0].lower() in pred.team_B.lower())
#                     )
                    
#                     if teams_match:
#                         filtered_predictions.append(pred)
                
#                 # If no exact matches, try to create one from the game data
#                 if not filtered_predictions and game_data:
#                     return self.create_fallback_predictions(game_data)
                
#                 return filtered_predictions
            
#             return predictions
            
#         except Exception as e:
#             print(f"Error during prediction analysis: {str(e)}")
#             return self.create_fallback_predictions(game_data)
        
#     def create_fallback_predictions(self, game_data: List[GameInfo]) -> List[Predictions]:
#         """Create simple predictions when the agent-based approach fails"""
#         results = []
        
#         if not self.teams or len(self.teams) != 2:
#             return results
            
#         for game in game_data:
#             # Check for team mentions in the game data
#             team_a_mentioned = any(self.teams[0].lower() in team.lower() for team in game.teams)
#             team_b_mentioned = any(self.teams[1].lower() in team.lower() for team in game.teams)
            
#             # Only include if both teams are mentioned
#             if team_a_mentioned and team_b_mentioned:
#                 # Use a basic winner selection logic - could be improved
#                 prediction = Predictions(
#                     site_name=game.site_name if hasattr(game, 'site_name') and game.site_name else "Analysis",
#                     site_url=game.source_url,
#                     author_name=game.author_name if hasattr(game, 'author_name') and game.author_name else None,
#                     team_A=self.teams[0],
#                     team_B=self.teams[1],
#                     winner=self.teams[0],  # Default prediction, could be improved
#                     reasoning="Based on limited analysis of available data. This is a fallback prediction."
#                 )
#                 results.append(prediction)
                
#         # If we couldn't create any predictions from game data, create at least one generic prediction
#         if not results and self.teams:
#             results.append(Predictions(
#                 site_name="System Analysis",
#                 site_url="N/A",
#                 author_name=None,
#                 team_A=self.teams[0],
#                 team_B=self.teams[1],
#                 winner=self.teams[0],  # Default prediction
#                 reasoning="Insufficient specific prediction data available. This is a basic prediction based on team history."
#             ))
            
#         return results
        
#     async def execute_prediction(self) -> Dict[str, Any]:
#         """Execute the full prediction process with game availability check"""
#         print(f"DEBUG: Checking for {self.league} games: {self.teams if self.teams else 'all teams'}")
        
#         # Step 1: Check for upcoming games
#         game_check = await self.check_upcoming_games()
        
#         if not game_check.get('has_games', False):
#             reason = game_check.get('reason', f'No upcoming {self.league} games found')
#             if self.teams:
#                 message = f"There are no upcoming {self.league} games for {' vs '.join(self.teams)}"
#             else:
#                 message = f"There are no upcoming {self.league} games"
            
#             return {
#                 "status": "no_games",
#                 "message": message,
#                 "reason": reason
#             }
            
#         # Games found, gather data from search agent
#         print(f"DEBUG: Found upcoming {self.league} games, gathering prediction data")
#         game_data = await self.gather_game_data()
        
#         if not game_data:
#             print(f"WARNING: No {self.league} game data found despite games being scheduled")
#             return {
#                 "status": "no_data",
#                 "message": f"{self.league} games are scheduled but no prediction data was found",
#                 "reason": "Unable to retrieve predictions"
#             }
            
#         print(f"DEBUG: Found data for {len(game_data)} {self.league} games")
        
#         def validate_predictions(pred_list):
#             valid_predictions = []
#             for p in pred_list:
#                 try:
#                     validated = Predictions(**p.dict() if hasattr(p, 'dict') else p)
#                     valid_predictions.append(validated)
#                 except Exception as e:
#                     print(f"Skipping invalid prediction: {str(e)}")
#             return valid_predictions
               
#         # Analyze data and generate predictions
#         predictions = await self.analyze_predictions(game_data)
#         validated_predictions = validate_predictions(predictions)
        
#         # Final check: if we have specific teams but no valid predictions, create a basic one
#         if self.teams and len(self.teams) == 2 and not validated_predictions:
#             fallback = self.create_fallback_predictions([])
#             validated_predictions = validate_predictions(fallback)
            
#         return {
#             "status": "success",
#             "predictions": validated_predictions
#         }

# async def predict_games(league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None) -> Dict[str, Any]:
#     """Function to be called from main.py"""
#     try:
#         manager = ManagerAgent(league, teams, provided_links)
#         max_retries = 3
#         retry_count = 0
        
#         while retry_count < max_retries:
#             try:
#                 result = await manager.execute_prediction()
#                 return result
#             except Exception as e:
#                 retry_count += 1
#                 print(f"Attempt {retry_count} failed: {str(e)}")
#                 await asyncio.sleep(1)
#         return {
#             "status": "error",
#             "message": f"Failed after {max_retries} attempts"
#         }
        
#     except Exception as e:
#         return {
#             "status": "error",
#             "message": f"Error in predict_games: {str(e)}"
#         }







# import asyncio
# from typing import Dict, Any, List, Optional
# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from datetime import datetime, timedelta
# from .web_search_agent import WebSearchAgent, GameInfo
# from tools.web_search_tool import WebSearchTools

# class Teams(BaseModel):
#     team_A: str
#     team_B: str
#     winner: str = Field(description="Name of the predicted winning team")

# class Predictions(BaseModel):
#     site_name: str = Field(description="Name of the website source")
#     site_url: str = Field(description="URL of the source website")
#     author_name: Optional[str] = Field(None, description="Author of the prediction if available")
#     team_A: str = Field(description="First team in the matchup")
#     team_B: str = Field(description="Second team in the matchup")
#     winner: str = Field(description="Name of the predicted winning team")
#     reasoning: str = Field(description="Reasoning behind the prediction")

# class NoGamesFound(BaseModel):
#     message: str
#     reason: str

# class ManagerAgent:
#     def __init__(self, league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None):
#         self.league = league
#         self.teams = teams
        
#         if not provided_links:
#             self.provided_links = WebSearchTools.get_league_sources(league)
#             print(f"[DEBUG] Retrieved league sources for {league}: {self.provided_links}")
#         else:
#             self.provided_links = provided_links
#             print(f"[DEBUG] Using provided links for {league}: {self.provided_links}")
            
#         self.duckduckgo_agent = WebSearchAgent('duckduckgo', league, self.provided_links)
    
#     async def check_upcoming_games(self) -> Dict[str, Any]:
#         now = datetime.now()
#         if self.teams:
#             teams_str = " vs ".join(self.teams)
#             query = f"{self.league} {teams_str} game schedule"
#         else:
#             query = f"{self.league} games schedule"
#         print(f"[DEBUG] check_upcoming_games query: {query}")
        
#         search_agent = WebSearchAgent('duckduckgo', self.league, self.provided_links)
#         results = search_agent.perform_search(query, num_results=5)
#         print(f"[DEBUG] check_upcoming_games received {len(results)} search results")
        
#         system_prompt = f"""
#         You are a {self.league} schedule expert. Analyze the provided search results to determine if there are any {self.league} games 
#         scheduled for today or in the upcoming 7 days. Today's date is {{today}}.
        
#         If you can identify specific upcoming games, respond with:
#         {{{{"has_games": true, "games": [list of games]}}}}
        
#         If there are no games scheduled, respond with:
#         {{{{"has_games": false, "reason": "Specific reason why (off-season, no games today, etc.)"}}}}
        
#         Be accurate and conservative - only indicate games exist if you have clear evidence.
#         """
        
#         search_text = "\n\n".join([
#             f"Title: {r.title}\nSnippet: {r.snippet}\nLink: {r.link}" 
#             for r in results if r.title and r.snippet
#         ])
#         print(f"[DEBUG] check_upcoming_games search_text constructed for agent analysis")
        
#         schedule_agent = Agent(
#             model="gpt-4o",
#             system_prompt=system_prompt.format(today=now.strftime("%A, %B %d, %Y")),
#             result_type=Dict[str, Any],
#             retries=15
#         )
        
#         agent_result = await schedule_agent.run(search_text)
#         print(f"[DEBUG] check_upcoming_games agent result: {agent_result}")
        
#         if hasattr(agent_result, 'value'):
#             return agent_result.value
#         elif hasattr(agent_result, 'data'):
#             return agent_result.data
#         else:
#             return agent_result
    
#     async def gather_game_data(self) -> List[GameInfo]:
#         print("[DEBUG] Starting to gather game data...")
#         data = await self.duckduckgo_agent.extract_game_predictions(self.teams)
#         print(f"[DEBUG] gather_game_data extracted {len(data)} game data entries")
#         return data
    
#     async def analyze_predictions(self, game_data: List[GameInfo]) -> List[Predictions]:
#         print("[DEBUG] Starting analysis of predictions...")
#         if not game_data:
#             print("[DEBUG] No game data provided to analyze_predictions")
#             return []
            
#         try:
#             team_specific_instructions = ""
#             if self.teams and len(self.teams) == 2:
#                 team_specific_instructions = f"""
#                 FOCUS ONLY ON THE MATCHUP BETWEEN {self.teams[0]} and {self.teams[1]}.
                
#                 Any predictions MUST be for this specific matchup only. Do not make predictions for any other games.
#                 team_A should be {self.teams[0]} and team_B should be {self.teams[1]}.
#                 """
#             system_prompt = f"""
#             You are an expert {self.league} analyst. Based on the provided game information, generate accurate predictions
#             for {self.league} games. For each matchup:
            
#             1. Identify the two teams (team_A and team_B)
#             2. Determine which team is more likely to win based on the provided data
#             3. Provide detailed reasoning for your prediction
#             4. Include the site_name, site_url, and author_name (if available) for each prediction
            
#             {team_specific_instructions}
            
#             Format your predictions as requested in the JSON structure with the following fields:
#             - site_name: Name of the website source
#             - site_url: URL of the source website
#             - author_name: Author of the prediction (if available)
#             - team_A: First team in the matchup
#             - team_B: Second team in the matchup
#             - winner: Name of the predicted winning team
#             - reasoning: Detailed reasoning for the prediction
#             """
#             print("[DEBUG] Sending data to analysis_agent with system_prompt:")
#             print(system_prompt)
            
#             analysis_agent = Agent(
#                 model="gpt-4o",
#                 system_prompt=system_prompt,
#                 result_type=List[Predictions],
#                 retries=7
#             )
#             agent_result = await analysis_agent.run({"game_data": [game.dict() for game in game_data]})
#             print(f"[DEBUG] analysis_agent returned: {agent_result}")
            
#             if hasattr(agent_result, 'value'):
#                 predictions = agent_result.value
#             elif hasattr(agent_result, 'data'):
#                 predictions = agent_result.data
#             else:
#                 predictions = agent_result
                
#             if self.teams and len(self.teams) == 2:
#                 filtered_predictions = []
#                 for pred in predictions:
#                     teams_match = (
#                         (pred.team_A.lower() in self.teams[0].lower() or self.teams[0].lower() in pred.team_A.lower()) and
#                         (pred.team_B.lower() in self.teams[1].lower() or self.teams[1].lower() in pred.team_B.lower())
#                     ) or (
#                         (pred.team_A.lower() in self.teams[1].lower() or self.teams[1].lower() in pred.team_A.lower()) and
#                         (pred.team_B.lower() in self.teams[0].lower() or self.teams[0].lower() in pred.team_B.lower())
#                     )
                    
#                     if teams_match:
#                         filtered_predictions.append(pred)
#                 print(f"[DEBUG] analyze_predictions filtered predictions count: {len(filtered_predictions)}")
                
#                 if not filtered_predictions and game_data:
#                     print("[DEBUG] No exact team match found. Creating fallback predictions.")
#                     return self.create_fallback_predictions(game_data)
                
#                 return filtered_predictions
            
#             return predictions
            
#         except Exception as e:
#             print(f"[ERROR] Error during prediction analysis: {str(e)}")
#             return self.create_fallback_predictions(game_data)
        
#     def create_fallback_predictions(self, game_data: List[GameInfo]) -> List[Predictions]:
#         print("[DEBUG] Creating fallback predictions...")
#         results = []
#         if not self.teams or len(self.teams) != 2:
#             return results
            
#         for game in game_data:
#             team_a_mentioned = any(self.teams[0].lower() in team.lower() for team in game.teams)
#             team_b_mentioned = any(self.teams[1].lower() in team.lower() for team in game.teams)
            
#             if team_a_mentioned and team_b_mentioned:
#                 prediction = Predictions(
#                     site_name=game.site_name if hasattr(game, 'site_name') and game.site_name else "Analysis",
#                     site_url=game.source_url,
#                     author_name=game.author_name if hasattr(game, 'author_name') and game.author_name else None,
#                     team_A=self.teams[0],
#                     team_B=self.teams[1],
#                     winner=self.teams[0],
#                     reasoning="Based on limited analysis of available data. This is a fallback prediction."
#                 )
#                 results.append(prediction)
#                 print(f"[DEBUG] Fallback prediction created from game data: {prediction}")
                
#         if not results and self.teams:
#             fallback = Predictions(
#                 site_name="System Analysis",
#                 site_url="N/A",
#                 author_name=None,
#                 team_A=self.teams[0],
#                 team_B=self.teams[1],
#                 winner=self.teams[0],
#                 reasoning="Insufficient specific prediction data available. This is a basic prediction based on team history."
#             )
#             results.append(fallback)
#             print(f"[DEBUG] Fallback prediction created as generic prediction: {fallback}")
            
#         return results
        
#     async def execute_prediction(self) -> Dict[str, Any]:
#         print(f"[DEBUG] Executing prediction for {self.league} games. Teams: {self.teams if self.teams else 'all teams'}")
        
#         game_check = await self.check_upcoming_games()
#         print(f"[DEBUG] Game availability check result: {game_check}")
        
#         if not game_check.get('has_games', False):
#             reason = game_check.get('reason', f'No upcoming {self.league} games found')
#             message = f"There are no upcoming {self.league} games for {' vs '.join(self.teams)}" if self.teams else f"There are no upcoming {self.league} games"
#             return {
#                 "status": "no_games",
#                 "message": message,
#                 "reason": reason
#             }
            
#         print(f"[DEBUG] Upcoming games found. Proceeding to gather game data...")
#         game_data = await self.gather_game_data()
#         if not game_data:
#             print(f"[WARNING] No {self.league} game data found despite games being scheduled")
#             return {
#                 "status": "no_data",
#                 "message": f"{self.league} games are scheduled but no prediction data was found",
#                 "reason": "Unable to retrieve predictions"
#             }
            
#         print(f"[DEBUG] Analyzing predictions from {len(game_data)} game data entries")
#         predictions = await self.analyze_predictions(game_data)
        
#         def validate_predictions(pred_list):
#             valid_predictions = []
#             for p in pred_list:
#                 try:
#                     validated = Predictions(**p.dict() if hasattr(p, 'dict') else p)
#                     valid_predictions.append(validated)
#                 except Exception as e:
#                     print(f"[DEBUG] Skipping invalid prediction: {str(e)}")
#             return valid_predictions
               
#         validated_predictions = validate_predictions(predictions)
        
#         if self.teams and len(self.teams) == 2 and not validated_predictions:
#             print("[DEBUG] No valid predictions found for specific teams. Generating fallback prediction.")
#             fallback = self.create_fallback_predictions([])
#             validated_predictions = validate_predictions(fallback)
            
#         print(f"[DEBUG] Final prediction count: {len(validated_predictions)}")
#         return {
#             "status": "success",
#             "predictions": validated_predictions
#         }

# async def predict_games(league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None) -> Dict[str, Any]:
#     try:
#         manager = ManagerAgent(league, teams, provided_links)
#         max_retries = 3
#         retry_count = 0
        
#         while retry_count < max_retries:
#             try:
#                 result = await manager.execute_prediction()
#                 return result
#             except Exception as e:
#                 retry_count += 1
#                 print(f"[ERROR] Attempt {retry_count} failed in predict_games: {str(e)}")
#                 await asyncio.sleep(1)
#         return {
#             "status": "error",
#             "message": f"Failed after {max_retries} attempts"
#         }
        
#     except Exception as e:
#         return {
#             "status": "error",
#             "message": f"Error in predict_games: {str(e)}"
#         }



# import asyncio
# from typing import Dict, Any, List, Optional
# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from datetime import datetime
# from .web_search_agent import WebSearchAgent, GameInfo
# from tools.web_search_tool import WebSearchTools

# class Teams(BaseModel):
#     team_A: str
#     team_B: str
#     winner: str = Field(description="Name of the predicted winning team")

# class Predictions(BaseModel):
#     site_name: str = Field(description="Name of the website source")
#     site_url: str = Field(description="URL of the source website")
#     author_name: Optional[str] = Field(None, description="Author of the prediction if available")
#     team_A: str = Field(description="First team in the matchup")
#     team_B: str = Field(description="Second team in the matchup")
#     winner: str = Field(description="Name of the predicted winning team")
#     reasoning: str = Field(description="Reasoning behind the prediction")

# class NoGamesFound(BaseModel):
#     message: str
#     reason: str

# class ManagerAgent:
#     def __init__(self, league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None):
#         self.league = league
#         self.teams = teams
#         if not provided_links:
#             self.provided_links = WebSearchTools.get_league_sources(league)
#             print(f"[DEBUG] ManagerAgent: Retrieved league sources for {league}: {self.provided_links}")
#         else:
#             self.provided_links = provided_links
#             print(f"[DEBUG] ManagerAgent: Using provided links for {league}: {self.provided_links}")
            
#         self.duckduckgo_agent = WebSearchAgent('duckduckgo', league, self.provided_links)
    
#     async def check_season_schedule(self) -> Dict[str, Any]:
#         now = datetime.now()
#         if self.teams:
#             teams_str = " vs ".join(self.teams)
#             query = f"{self.league} {teams_str} season schedule"
#         else:
#             query = f"{self.league} season schedule"
#         print(f"[DEBUG] check_season_schedule query: {query}")
        
#         search_agent = WebSearchAgent('duckduckgo', self.league, self.provided_links)
#         results = search_agent.perform_search(query, num_results=5)
#         print(f"[DEBUG] check_season_schedule received {len(results)} search results")
        
#         # If no search results but we have provided links, assume schedule exists
#         if not results and self.provided_links:
#             print(f"[DEBUG] No search results but using provided links. Assuming schedule exists.")
#             return {"has_schedule": True, "reason": "Using provided links only"}
        
#         system_prompt = f"""
#         You are a {self.league} schedule expert. Analyze the provided search results to determine if there is a season schedule 
#         available for the matchup or for the league. Today's date is {{today}}.
        
#         If you can identify a season schedule, respond with:
#         {{{{"has_schedule": true, "schedule": [list of games]}}}}
        
#         If no season schedule is available, respond with:
#         {{{{"has_schedule": false, "reason": "No season schedule found or not available"}}}}
        
#         Be accurate and conservative.
#         """
        
#         search_text = "\n\n".join([
#             f"Title: {r.title}\nSnippet: {r.snippet}\nLink: {r.link}" 
#             for r in results if r.title and r.snippet
#         ]) if results else "No search results available."
#         print(f"[DEBUG] check_season_schedule search_text constructed for agent analysis")
        
#         if not results and self.provided_links:
#             print(f"[DEBUG] No search results but using provided links. Returning has_schedule=true")
#             return {"has_schedule": True, "reason": "Using provided links only"}
            
#         schedule_agent = Agent(
#             model="gpt-4o",
#             system_prompt=system_prompt.format(today=now.strftime("%A, %B %d, %Y")),
#             result_type=Dict[str, Any],
#             retries=15
#         )
        
#         agent_result = await schedule_agent.run(search_text)
#         print(f"[DEBUG] check_season_schedule agent result: {agent_result}")
        
#         if hasattr(agent_result, 'value'):
#             return agent_result.value
#         elif hasattr(agent_result, 'data'):
#             return agent_result.data
#         else:
#             return agent_result
    
#     async def gather_game_data(self) -> List[GameInfo]:
#         print(f"[DEBUG] Starting to gather game data for specific matchup: {self.teams}")
#         data = await self.duckduckgo_agent.extract_game_predictions(self.teams)
#         print(f"[DEBUG] gather_game_data extracted {len(data)} game data entries")
#         for i, entry in enumerate(data):
#             print(f"[DEBUG] Game data entry #{i+1}: Teams={entry.teams}, Source={entry.source_url}")
#         return data
    
#     async def analyze_predictions(self, game_data: List[GameInfo]) -> List[Predictions]:
#         print("[DEBUG] Starting analysis of predictions...")
#         if not game_data:
#             print("[DEBUG] No game data provided to analyze_predictions")
#             return []
            
#         try:
#             team_specific_instructions = ""
#             if self.teams and len(self.teams) == 2:
#                 team_specific_instructions = f"""
#                 FOCUS ONLY ON THE MATCHUP BETWEEN {self.teams[0]} and {self.teams[1]}.
                
#                 Any predictions MUST be for this specific matchup only. Do not make predictions for any other games.
#                 team_A should be {self.teams[0]} and team_B should be {self.teams[1]}.
#                 """
#             system_prompt = f"""
#             You are an expert {self.league} analyst. Based on the provided game information, generate accurate predictions
#             for {self.league} season games. For each matchup:
            
#             1. Identify the two teams (team_A and team_B)
#             2. Determine which team is more likely to win based on the provided data
#             3. Provide detailed reasoning for your prediction based ONLY on the source data
#             4. Include the site_name, site_url, and author_name (if available) for each prediction
            
#             {team_specific_instructions}
            
#             Format your predictions as requested in the JSON structure with the following fields:
#             - site_name: Name of the website source
#             - site_url: URL of the source website
#             - author_name: Author of the prediction (if available)
#             - team_A: First team in the matchup
#             - team_B: Second team in the matchup
#             - winner: Name of the predicted winning team (MUST be either team_A or team_B)
#             - reasoning: Detailed reasoning for the prediction based on the source data
            
#             If the data doesn't contain actual predictions for the matchup, DO NOT create fictional predictions.
#             Return an empty list instead.
#             """
#             print("[DEBUG] Sending data to analysis_agent with system_prompt for teams: " + ", ".join(self.teams))
            
#             analysis_agent = Agent(
#                 model="gpt-4o",
#                 system_prompt=system_prompt,
#                 result_type=List[Predictions],
#                 retries=7
#             )
            
#             # Convert game_data to dict for better agent understanding
#             game_data_dicts = [game.dict() for game in game_data]
#             print(f"[DEBUG] Sending {len(game_data_dicts)} game data entries to analysis agent")
            
#             agent_result = await analysis_agent.run({"game_data": game_data_dicts})
#             print(f"[DEBUG] analysis_agent returned result type: {type(agent_result)}")
            
#             if hasattr(agent_result, 'value'):
#                 predictions = agent_result.value
#             elif hasattr(agent_result, 'data'):
#                 predictions = agent_result.data
#             else:
#                 predictions = agent_result
                
#             print(f"[DEBUG] analysis_agent returned {len(predictions)} predictions")
                
#             if self.teams and len(self.teams) == 2:
#                 filtered_predictions = []
#                 for pred in predictions:
#                     # Check if prediction matches our specified teams
#                     team_a_match = any(self.teams[0].lower() in pred.team_A.lower() or 
#                                        pred.team_A.lower() in self.teams[0].lower())
#                     team_b_match = any(self.teams[1].lower() in pred.team_B.lower() or 
#                                        pred.team_B.lower() in self.teams[1].lower())
#                     reverse_match = any(self.teams[0].lower() in pred.team_B.lower() or 
#                                        pred.team_B.lower() in self.teams[0].lower()) and \
#                                     any(self.teams[1].lower() in pred.team_A.lower() or 
#                                        pred.team_A.lower() in self.teams[1].lower())
                    
#                     if (team_a_match and team_b_match) or reverse_match:
#                         print(f"[DEBUG] Matched prediction for {pred.team_A} vs {pred.team_B} from {pred.site_name}")
#                         filtered_predictions.append(pred)
#                     else:
#                         print(f"[DEBUG] Skipping prediction for {pred.team_A} vs {pred.team_B} - not matching target teams")
                
#                 print(f"[DEBUG] analyze_predictions filtered predictions count: {len(filtered_predictions)}")
                
#                 if not filtered_predictions and game_data:
#                     print("[DEBUG] No exact team match found. Checking if we need to create fallback predictions.")
#                     # Only create fallback if there was some game data but predictions weren't properly extracted
#                     relevant_games = 0
#                     for game in game_data:
#                         team_a_mentioned = any(self.teams[0].lower() in team.lower() or team.lower() in self.teams[0].lower() 
#                                                for team in game.teams)
#                         team_b_mentioned = any(self.teams[1].lower() in team.lower() or team.lower() in self.teams[1].lower() 
#                                                for team in game.teams)
#                         if team_a_mentioned and team_b_mentioned:
#                             relevant_games += 1
                    
#                     if relevant_games > 0:
#                         print(f"[DEBUG] Found {relevant_games} relevant games but no predictions. Creating fallback predictions.")
#                         return self.create_fallback_predictions(game_data)
#                     else:
#                         print("[DEBUG] No relevant games found. Returning empty predictions.")
#                         return []
                
#                 return filtered_predictions
            
#             return predictions
            
#         except Exception as e:
#             print(f"[ERROR] Error during prediction analysis: {str(e)}")
#             if game_data:
#                 return self.create_fallback_predictions(game_data)
#             return []
        
#     def create_fallback_predictions(self, game_data: List[GameInfo]) -> List[Predictions]:
#         print("[DEBUG] Creating fallback predictions...")
#         results = []
#         if not self.teams or len(self.teams) != 2:
#             print("[DEBUG] Cannot create fallback predictions without exactly 2 teams")
#             return results
            
#         # Group by source URL to avoid duplicates
#         sources_seen = set()
        
#         for game in game_data:
#             if game.source_url in sources_seen:
#                 continue
                
#             sources_seen.add(game.source_url)
            
#             team_a_mentioned = any(self.teams[0].lower() in team.lower() or team.lower() in self.teams[0].lower() 
#                                   for team in game.teams)
#             team_b_mentioned = any(self.teams[1].lower() in team.lower() or team.lower() in self.teams[1].lower() 
#                                   for team in game.teams)
            
#             if team_a_mentioned and team_b_mentioned:
#                 print(f"[DEBUG] Creating fallback prediction from source: {game.source_url}")
                
#                 fallback_reasoning = f"Prediction derived from limited available content. "
#                 if game.summary:
#                     fallback_reasoning += f"Based on source summary: {game.summary}"
#                 else:
#                     fallback_reasoning += "No detailed reasoning available from the source."
                    
#                 # Base winner determination on mentions in the data
#                 team_a_count = sum(1 for team in game.teams if self.teams[0].lower() in team.lower())
#                 team_b_count = sum(1 for team in game.teams if self.teams[1].lower() in team.lower())
#                 winner = self.teams[0] if team_a_count >= team_b_count else self.teams[1]
                
#                 prediction = Predictions(
#                     site_name=game.site_name if hasattr(game, 'site_name') and game.site_name else "Analysis",
#                     site_url=game.source_url,
#                     author_name=game.author_name if hasattr(game, 'author_name') and game.author_name else None,
#                     team_A=self.teams[0],
#                     team_B=self.teams[1],
#                     winner=winner,
#                     reasoning=fallback_reasoning
#                 )
#                 results.append(prediction)
#                 print(f"[DEBUG] Fallback prediction created from game data for {self.teams[0]} vs {self.teams[1]}")
                
#         if not results and self.teams:
#             print("[DEBUG] No game data matches found for fallback. Creating a generic fallback prediction.")
#             fallback = Predictions(
#                 site_name="System Analysis",
#                 site_url="N/A",
#                 author_name=None,
#                 team_A=self.teams[0],
#                 team_B=self.teams[1],
#                 winner=self.teams[0],  # Default to team A winning
#                 reasoning="Insufficient specific prediction data available. This is a basic prediction based on team history."
#             )
#             results.append(fallback)
#             print(f"[DEBUG] Generic fallback prediction created for {self.teams[0]} vs {self.teams[1]}")
            
#         return results
        
#     async def execute_prediction(self) -> Dict[str, Any]:
#         print(f"[DEBUG] Executing prediction for {self.league} season games. Teams: {self.teams if self.teams else 'all teams'}")
        
#         # Season schedule check (for the entire season)
#         game_check = await self.check_season_schedule()
#         print(f"[DEBUG] Season schedule check result: {game_check}")
        
#         if not game_check.get('has_schedule', False):
#             reason = game_check.get('reason', f'No season schedule found for {self.league}')
#             message = f"There is no season schedule for {self.league} games for {' vs '.join(self.teams)}" if self.teams else f"There is no season schedule for {self.league} games"
#             return {
#                 "status": "no_games",
#                 "message": message,
#                 "reason": reason
#             }
            
#         print(f"[DEBUG] Season schedule found. Proceeding to gather game data...")
#         game_data = await self.gather_game_data()
#         if not game_data:
#             print(f"[WARNING] No {self.league} game data found despite schedule being available")
#             return {
#                 "status": "no_data",
#                 "message": f"{self.league} season schedule is available but no prediction data was found for {' vs '.join(self.teams)}",
#                 "reason": "Unable to retrieve predictions for the specific matchup"
#             }
            
#         print(f"[DEBUG] Analyzing predictions from {len(game_data)} game data entries")
#         predictions = await self.analyze_predictions(game_data)
        
#         def validate_predictions(pred_list):
#             valid_predictions = []
#             for p in pred_list:
#                 try:
#                     if hasattr(p, 'dict'):
#                         p_dict = p.dict()
#                     else:
#                         p_dict = p
                    
#                     # Ensure the winner is one of the two teams
#                     if p_dict.get('winner') not in [p_dict.get('team_A'), p_dict.get('team_B')]:
#                         print(f"[WARNING] Invalid prediction: winner {p_dict.get('winner')} is not one of the teams {p_dict.get('team_A')} or {p_dict.get('team_B')}")
#                         p_dict['winner'] = p_dict.get('team_A')  # Default to team A if invalid
                        
#                     validated = Predictions(**p_dict)
#                     valid_predictions.append(validated)
#                 except Exception as e:
#                     print(f"[DEBUG] Skipping invalid prediction: {str(e)}")
#             return valid_predictions
               
#         validated_predictions = validate_predictions(predictions)
#         print(f"[DEBUG] Validated {len(validated_predictions)} of {len(predictions)} predictions")
        
#         if self.teams and len(self.teams) == 2 and not validated_predictions:
#             print("[DEBUG] No valid predictions found for specific teams. Generating fallback prediction.")
#             fallback = self.create_fallback_predictions([])
#             validated_predictions = validate_predictions(fallback)
            
#         print(f"[DEBUG] Final prediction count: {len(validated_predictions)}")
#         return {
#             "status": "success",
#             "predictions": validated_predictions
#         }

# async def predict_games(league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None) -> Dict[str, Any]:
#     try:
#         print(f"[DEBUG] predict_games called for {league} with teams: {teams}")
#         manager = ManagerAgent(league, teams, provided_links)
#         max_retries = 3
#         retry_count = 0
        
#         while retry_count < max_retries:
#             try:
#                 print(f"[DEBUG] predict_games attempt {retry_count+1}/{max_retries}")
#                 result = await manager.execute_prediction()
#                 print(f"[DEBUG] predict_games completed with status: {result.get('status')}")
#                 return result
#             except Exception as e:
#                 retry_count += 1
#                 print(f"[ERROR] Attempt {retry_count} failed in predict_games: {str(e)}")
#                 await asyncio.sleep(1)
        
#         print(f"[ERROR] predict_games failed after {max_retries} attempts")
#         return {
#             "status": "error",
#             "message": f"Failed after {max_retries} attempts"
#         }
        
#     except Exception as e:
#         print(f"[ERROR] Unhandled exception in predict_games: {str(e)}")
#         return {
#             "status": "error",
#             "message": f"Error in predict_games: {str(e)}"
#         }



# import asyncio
# from typing import Dict, Any, List, Optional
# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from .web_search_agent import WebSearchAgent, GameInfo
# from tools.web_search_tool import WebSearchTools

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
# # agent = Agent(model=model)

# class Predictions(BaseModel):
#     site_name: str = Field(description="Name of the website source")
#     site_url: str = Field(description="URL of the source website")
#     author_name: Optional[str] = Field(None, description="Author of the prediction if available")
#     team_A: str = Field(description="First team in the matchup")
#     team_B: str = Field(description="Second team in the matchup")
#     winner: str = Field(description="Name of the predicted winning team")
#     reasoning: str = Field(description="Reasoning behind the prediction")

# class ManagerAgent:
#     def __init__(self, league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None):
#         self.league = league
#         self.teams = teams
#         self.provided_links = provided_links or WebSearchTools.get_league_sources(league)
#         print(f"[DEBUG] ManagerAgent: Using links for {league}: {self.provided_links}")
#         self.duckduckgo_agent = WebSearchAgent('duckduckgo', league, self.provided_links)

#     async def gather_game_data(self) -> List[GameInfo]:
#         print(f"[DEBUG] Starting to gather game data for matchup: {self.teams}")
#         data = await self.duckduckgo_agent.extract_game_predictions(self.teams)
#         print(f"[DEBUG] Gathered {len(data)} game data entries")
#         return data

#     async def analyze_predictions(self, game_data: List[GameInfo]) -> List[Predictions]:
#         print("[DEBUG] Starting prediction analysis...")
#         if not game_data:
#             return []

#         team_specific_instructions = ""
#         if self.teams and len(self.teams) == 2:
#             team_specific_instructions = f"""
#             Focus only on the matchup between {self.teams[0]} and {self.teams[1]}.
#             Predictions must be for this specific matchup only.
#             team_A should be {self.teams[0]} and team_B should be {self.teams[1]}.
#             If any output variable is missing, use "none".
#             """

#         system_prompt = f"""
#         You are an expert {self.league} analyst. Based on the provided game data, predict outcomes of {self.league} matchups.

#         1. Identify team_A and team_B
#         2. Predict the winner between them
#         3. Justify your reasoning based only on the source data
#         4. Include site_name, site_url, and author_name if available

#         {team_specific_instructions}

#         Output format: JSON list of objects with
#         - site_name
#         - site_url
#         - author_name
#         - team_A
#         - team_B
#         - winner
#         - reasoning
#         """

#         analysis_agent = Agent(
#             model=model,
#             system_prompt=system_prompt,
#             result_type=List[Predictions],
#             retries=7
#         )

#         game_data_dicts = [g.dict() for g in game_data]
#         print(f"[DEBUG] Sending {len(game_data_dicts)} entries to analysis agent")

#         try:
#             result = await analysis_agent.run({"game_data": game_data_dicts})
#             predictions = getattr(result, 'value', getattr(result, 'data', result))
#             print(f"[DEBUG] Received {len(predictions)} predictions")
#             return predictions
#         except Exception as e:
#             print(f"[ERROR] Error in analysis agent: {str(e)}")
#             return []

#     async def execute_prediction(self) -> Dict[str, Any]:
#         print(f"[DEBUG] Executing prediction for {self.league}, Teams: {self.teams or 'All'}")
#         game_data = await self.gather_game_data()
#         if not game_data:
#             return {
#                 "status": "no_data",
#                 "message": f"No prediction data found for {' vs '.join(self.teams)}" if self.teams else f"No data found for {self.league}",
#                 "reason": "No matching data"
#             }

#         predictions = await self.analyze_predictions(game_data)

#         def validate(pred_list):
#             valid = []
#             for p in pred_list:
#                 try:
#                     p_dict = p.dict() if hasattr(p, 'dict') else p
#                     validated = Predictions(
#                         site_name=p_dict.get("site_name", "none"),
#                         site_url=p_dict.get("site_url", "none"),
#                         author_name=p_dict.get("author_name", "none"),
#                         team_A=p_dict.get("team_A", "none"),
#                         team_B=p_dict.get("team_B", "none"),
#                         winner=p_dict.get("winner") if p_dict.get("winner") in [p_dict.get("team_A"), p_dict.get("team_B")] else (p_dict.get("team_A") or "none"),
#                         reasoning=p_dict.get("reasoning", "none")
#                     )
#                     valid.append(validated)
#                 except Exception as e:
#                     print(f"[DEBUG] Skipping invalid prediction: {str(e)}")
#             return valid

#         validated_predictions = validate(predictions)
#         print(f"[DEBUG] Final prediction count: {len(validated_predictions)}")

#         return {
#             "status": "success",
#             "predictions": validated_predictions
#         }

# async def predict_games(league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None) -> Dict[str, Any]:
#     print(f"[DEBUG] predict_games called for {league} with teams: {teams}")
#     manager = ManagerAgent(league, teams, provided_links)
#     for attempt in range(3):
#         try:
#             print(f"[DEBUG] Attempt {attempt+1}/3")
#             return await manager.execute_prediction()
#         except Exception as e:
#             print(f"[ERROR] Attempt {attempt+1} failed: {str(e)}")
#             await asyncio.sleep(1)
#     return {
#         "status": "error",
#         "message": "Failed after 3 attempts"
#     }




# import os
# import asyncio
# import json
# from typing import Dict, Any, List, Optional
# from pydantic import BaseModel, Field
# from pydantic_ai import Agent
# from .web_search_agent import WebSearchAgent ,GameSummary
# from tools.web_search_tool import WebSearchTools

# from pydantic_ai.providers.openai import OpenAIProvider
# from pydantic_ai.models import openai
# provider = OpenAIProvider(
#     base_url='https://openrouter.ai/api/v1',
#     api_key=os.environ.get("OPENROUTER_API_KEY")
# )
# model = openai.OpenAIModel(
#     "openrouter/quasar-alpha",
#     provider=provider
# )

# class Predictions(BaseModel):
#     site_name: str
#     site_url: str
#     author_name: Optional[str] = "none"
#     team_A: str
#     team_B: str
#     winner: str
#     reasoning: str

# class ManagerAgent:
#     def __init__(self, league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None):
#         self.league = league
#         self.teams = teams
#         self.provided_links = provided_links or WebSearchTools.get_league_sources(league)
#         print(f"[DEBUG] ManagerAgent: Using links for {league}: {self.provided_links}")
#         self.web_agent = WebSearchAgent('duckduckgo', league, self.provided_links)

#     async def gather_game_summaries(self) -> List[GameSummary]:
#         print(f"[DEBUG] Gathering game summaries for teams: {self.teams}")
#         results = await self.web_agent.extract_game_predictions(self.teams)
#         print(f"[DEBUG] Extracted {len(results)} summaries")
#         return results

#     async def analyze_each_summary(self, summaries: List[GameSummary]) -> List[Predictions]:
#         print("[DEBUG] Starting prediction analysis for each summary...")
#         if not summaries:
#             return []

#         system_prompt_template = f"""
#         You are an expert {self.league} analyst. Based on the provided text summary, extract prediction details.

#         Requirements:
#         - Identify team_A and team_B
#         - Predict the winner
#         - Justify your reasoning based only on the provided summary
#         - Include site_name, site_url, and author_name if available

#         Only return predictions for {self.teams[0]} vs {self.teams[1]}.

#         Output format (single JSON):
#         {{
#             "site_name": "...",
#             "site_url": "...",
#             "author_name": "...",
#             "team_A": "...",
#             "team_B": "...",
#             "winner": "...",
#             "reasoning": "..."
#         }}
#         """

#         final_predictions = []
#         for idx, summary in enumerate(summaries):
#             print(f"[DEBUG] Analyzing summary #{idx+1} from {summary.site_name}")
#             system_prompt = system_prompt_template

#             analysis_agent = Agent(
#                 model=model,
#                 system_prompt=system_prompt,
#                 result_type=Predictions,
#                 retries=5
#             )

#             try:
#                 result = await analysis_agent.run({"summary": summary.summary})
#                 if isinstance(result, dict):
#                     pred = Predictions(**result)
#                 else:
#                     pred = result

#                 # Fill missing fields
#                 pred.site_name = summary.site_name or "none"
#                 pred.site_url = summary.source_url or "none"
#                 pred.author_name = summary.author_name or "none"
#                 final_predictions.append(pred)

#                 # Save each prediction individually to file
#                 file_name = f"prediction_summary_{idx+1}.json"
#                 with open(file_name, "w", encoding="utf-8") as f:
#                     json.dump(pred.dict(), f, indent=2)
#                 print(f"[DEBUG] Saved summary #{idx+1} to {file_name}")

#             except Exception as e:
#                 print(f"[ERROR] Failed to process summary #{idx+1}: {e}")

#         return final_predictions

#     async def execute_prediction(self) -> Dict[str, Any]:
#         summaries = await self.gather_game_summaries()
#         predictions = await self.analyze_each_summary(summaries)

#         if not predictions:
#             return {
#                 "status": "no_data",
#                 "message": f"No predictions found for {' vs '.join(self.teams)}" if self.teams else f"No data found for {self.league}"
#             }

#         all_preds = [p.dict() for p in predictions]
#         final_file = "final_predictions.json"
#         with open(final_file, "w", encoding="utf-8") as f:
#             json.dump(all_preds, f, indent=2)

#         print(f"[DEBUG] All predictions written to {final_file}")
#         return {
#             "status": "success",
#             "file": final_file,
#             "predictions": all_preds
#         }

# async def predict_games(league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None) -> Dict[str, Any]:
#     print(f"[DEBUG] Running predict_games for league={league}, teams={teams}")
#     manager = ManagerAgent(league, teams, provided_links)

#     for attempt in range(3):
#         try:
#             return await manager.execute_prediction()
#         except Exception as e:
#             print(f"[ERROR] Attempt {attempt+1} failed: {e}")
#             await asyncio.sleep(1)

#     return {
#         "status": "error",
#         "message": "Failed after 3 attempts"
#     }




import asyncio
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from .web_search_agent import WebSearchAgent  # Note: GameSummary is now a dict
from tools.web_search_tool import WebSearchTools

from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models import openai

provider = OpenAIProvider(
    base_url='https://openrouter.ai/api/v1',
    api_key='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'#'OPENROUTER_API_KEY'
)
model = openai.OpenAIModel(
    "openai/gpt-4o-mini",
    provider=provider
)

class Predictions(BaseModel):
    site_name: str = Field(description="Name of the website source")
    site_url: str = Field(description="URL of the source website")
    author_name: Optional[str] = Field("none", description="Author of the prediction if available")
    team_A: str = Field(description="First team in the matchup")
    team_B: str = Field(description="Second team in the matchup")
    winner: str = Field(description="Name of the predicted winning team")
    reasoning: str = Field(description="Reasoning behind the prediction")

class ManagerAgent:
    def __init__(self, league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None):
        self.league = league
        self.teams = teams
        self.provided_links = provided_links or WebSearchTools.get_league_sources(league)
        print(f"[DEBUG] ManagerAgent: Using links for {league}: {self.provided_links}")
        self.web_agent = WebSearchAgent('duckduckgo', league, self.provided_links)

    async def gather_game_summaries(self) -> List[dict]:
        print(f"[DEBUG] Gathering game summaries for teams: {self.teams}")
        summaries = await self.web_agent.extract_game_predictions(self.teams)
        print(f"[DEBUG] Extracted {len(summaries)} summaries")
        return summaries

    async def analyze_each_summary(self, summaries: List[dict]) -> List[Predictions]:
        print("[DEBUG] Starting prediction analysis for each summary...")
        if not summaries:
            return []

        system_prompt_template = f"""
        You are an expert {self.league} analyst. Based on the provided text summary, extract prediction details.

        Requirements:
        - Identify team_A and team_B
        - Predict the winner between them
        - Justify your reasoning based only on the provided summary
        - Include site_name, site_url, and author_name if available

        Only return predictions for {self.teams[0]} vs {self.teams[1]}.
        """

        final_predictions = []
        for idx, summary in enumerate(summaries):
            site_name = summary.get("site_name", "none")
            print(f"[DEBUG] Analyzing summary #{idx+1} from {site_name}")
            system_prompt = system_prompt_template

            analysis_agent = Agent(
                model=model,
                system_prompt=system_prompt,
                result_type=Predictions,
                retries=5
            )

            try:
                # Use dictionary access for the summary text
                result = await analysis_agent.run({"summary": summary.get("summary", "")})
                if hasattr(result, "value"):
                    pred = result.value
                elif hasattr(result, "data"):
                    pred = result.data
                else:
                    pred = result

                # Use the summary's metadata for missing values
                pred.site_name = summary.get("site_name", "none")
                pred.site_url = summary.get("source_url", "none")
                pred.author_name = summary.get("author_name", "none")
                final_predictions.append(pred)

                # Save each prediction individually to file
                file_name = f"prediction_summary_{idx+1}.json"
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(pred.dict(), f, indent=2)
                print(f"[DEBUG] Saved summary #{idx+1} prediction to {file_name}")

            except Exception as e:
                print(f"[ERROR] Failed to process summary #{idx+1}: {e}")

        return final_predictions

    async def execute_prediction(self) -> Dict[str, Any]:
        summaries = await self.gather_game_summaries()
        predictions = await self.analyze_each_summary(summaries)

        if not predictions:
            return {
                "status": "no_data",
                "message": f"No predictions found for {' vs '.join(self.teams)}" if self.teams else f"No data found for {self.league}"
            }

        all_preds = [p.dict() for p in predictions]
        final_file = "final_predictions.json"
        with open(final_file, "w", encoding="utf-8") as f:
            json.dump(all_preds, f, indent=2)

        print(f"[DEBUG] All predictions written to {final_file}")
        return {
            "status": "success",
            "file": final_file,
            "predictions": all_preds
        }

async def predict_games(league: str, teams: Optional[List[str]] = None, provided_links: Optional[List[str]] = None) -> Dict[str, Any]:
    print(f"[DEBUG] Running predict_games for league={league}, teams={teams}")
    manager = ManagerAgent(league, teams, provided_links)

    for attempt in range(3):
        try:
            print(f"[DEBUG] Attempt {attempt+1}/3")
            return await manager.execute_prediction()
        except Exception as e:
            print(f"[ERROR] Attempt {attempt+1} failed: {e}")
            await asyncio.sleep(1)

    return {
        "status": "error",
        "message": "Failed after 3 attempts"
    }
