# import os
# import json
# import asyncio
# from dotenv import load_dotenv
# from agents.manager_agent import predict_games
# from tools.web_search_tool import WebSearchTools

# # Load environment variables
# load_dotenv()

# def convert_to_dict(obj):
#     """Helper function to convert pydantic models to dict"""
#     if hasattr(obj, 'dict'):
#         return obj.dict()
#     elif hasattr(obj, 'model_dump'):
#         return obj.model_dump()
#     return obj

# async def main():
#     results_output = {
#         "specific_matchup": None,
#         "all_games": None,
#         "search_test": None
#     }
    
#     # Get predictions for specific teams
#     try:
#         print("=" * 50)
#         print("Predicting specific matchup: Kansas City Chiefs vs San Francisco 49ers")
#         print("=" * 50)
        
#         specific_results = await predict_games(teams=["Orlando Magic", "Atlanta Hawks"])
        
#         if specific_results.get("status") == "success":
#             predictions = specific_results.get("predictions", [])
#             formatted_predictions = [convert_to_dict(pred) for pred in predictions]
#             results_output["specific_matchup"] = {
#                 "status": "success",
#                 "count": len(formatted_predictions),
#                 "predictions": formatted_predictions
#             }
#         else:
#             results_output["specific_matchup"] = {
#                 "status": specific_results.get("status", "unknown"),
#                 "message": specific_results.get("message", ""),
#                 "reason": specific_results.get("reason", "")
#             }
            
#         print(json.dumps(results_output["specific_matchup"], indent=2, default=str))
        
#     except Exception as e:
#         results_output["specific_matchup"] = {
#             "status": "error",
#             "message": f"Failed to predict specific matchup: {str(e)}"
#         }
#         print(json.dumps(results_output["specific_matchup"], indent=2))
    
#     #Get predictions for all upcoming games
#     try:
#         print("\n" + "=" * 50)
#         print("Predicting all upcoming NFL games")
#         print("=" * 50)
        
#         all_games_results = await predict_games()
        
#         if all_games_results.get("status") == "success":
#             predictions = all_games_results.get("predictions", [])
#             formatted_predictions = [convert_to_dict(pred) for pred in predictions]
#             results_output["all_games"] = {
#                 "status": "success",
#                 "count": len(formatted_predictions),
#                 "predictions": formatted_predictions
#             }
#         else:
#             results_output["all_games"] = {
#                 "status": all_games_results.get("status", "unknown"),
#                 "message": all_games_results.get("message", ""),
#                 "reason": all_games_results.get("reason", "")
#             }
            
#         print(json.dumps(results_output["all_games"], indent=2, default=str))
        
#     except Exception as e:
#         results_output["all_games"] = {
#             "status": "error",
#             "message": f"Failed to predict upcoming games: {str(e)}"
#         }
#         print(json.dumps(results_output["all_games"], indent=2))

#     # # Example 3: Test web search tools directly (optional - can be removed if not needed)
#     # try:
#     #     print("\n" + "=" * 50)
#     #     print("Testing Web Search Tools")
#     #     print("=" * 50)
        
#     #     search_results = WebSearchTools.duckduckgo_search("NFL schedule this week")
        
#     #     if search_results:
#     #         formatted_search_results = []
#     #         for result in search_results[:3]:
#     #             formatted_result = {
#     #                 "title": result.title,
#     #                 "link": result.link,
#     #                 "snippet": result.snippet[:100] if result.snippet else 'No snippet'
#     #             }
#     #             formatted_search_results.append(formatted_result)
                
#     #         results_output["search_test"] = {
#     #             "status": "success",
#     #             "count": len(search_results),
#     #             "results": formatted_search_results
#     #         }
#     #     else:
#     #         results_output["search_test"] = {
#     #             "status": "no_results",
#     #             "message": "No search results found"
#     #         }
            
#     #     print(json.dumps(results_output["search_test"], indent=2))
        
#     # except Exception as e:
#     #     results_output["search_test"] = {
#     #         "status": "error",
#     #         "message": f"Web search test failed: {str(e)}"
#     #     }
#     #     print(json.dumps(results_output["search_test"], indent=2))
    
#     print("\n" + "=" * 50)
#     print("COMPLETE JSON OUTPUT")
#     print("=" * 50)
#     print(json.dumps(results_output, indent=2, default=str))

#     with open('nfl_predictions_output.json', 'w') as f:
#         json.dump(results_output, f, indent=2, default=str)
#     print(f"Complete results saved to nfl_predictions_output.json")

# if __name__ == "__main__":
#     asyncio.run(main())




# import os
# import json
# import asyncio
# from dotenv import load_dotenv
# from agents.manager_agent import predict_games
# from tools.web_search_tool import WebSearchTools

# # Load environment variables
# load_dotenv()

# def convert_to_dict(obj):
#     """Helper function to convert pydantic models to dict"""
#     if hasattr(obj, 'dict'):
#         return obj.dict()
#     elif hasattr(obj, 'model_dump'):
#         return obj.model_dump()
#     return obj

# async def main():
#     # Set the target league here - can be "NFL", "NBA", "MLB", "NHL", "EPL", etc.
#     league = "NBA"  # Change this variable to the desired league
    
#     # Optional: Provide specific links to use (leave empty to use default sources)
#     provided_links = [
#         "https://www.cbssports.com/nba/expert-picks/",
#         "https://www.espn.com/nba/picks",
#         "https://www.nbcsports.com/betting/nba/tools/game-predictions"
#     ]
    
#     # Set specific teams for a matchup
#     specific_matchup = ["LA Clippers", "San Antonio Spurs"]
    
#     results_output = {
#         "specific_matchup": None,
#         "all_games": None
#     }
    
#     # Get predictions for specific teams
#     try:
#         print("=" * 50)
#         print(f"Predicting specific {league} matchup: {' vs '.join(specific_matchup)}")
#         print("=" * 50)
        
#         specific_results = await predict_games(league, teams=specific_matchup, provided_links=provided_links)
        
#         if specific_results.get("status") == "success":
#             predictions = specific_results.get("predictions", [])
#             formatted_predictions = [convert_to_dict(pred) for pred in predictions]
#             results_output["specific_matchup"] = {
#                 "status": "success",
#                 "count": len(formatted_predictions),
#                 "predictions": formatted_predictions
#             }
#         else:
#             results_output["specific_matchup"] = {
#                 "status": specific_results.get("status", "unknown"),
#                 "message": specific_results.get("message", ""),
#                 "reason": specific_results.get("reason", "")
#             }
            
#         print(json.dumps(results_output["specific_matchup"], indent=2, default=str))
        
#     except Exception as e:
#         results_output["specific_matchup"] = {
#             "status": "error",
#             "message": f"Failed to predict specific {league} matchup: {str(e)}"
#         }
#         print(json.dumps(results_output["specific_matchup"], indent=2))
    
#     # Get predictions for all upcoming games
#     try:
#         print("\n" + "=" * 50)
#         print(f"Predicting all upcoming {league} games")
#         print("=" * 50)
        
#         all_games_results = await predict_games(league, provided_links=provided_links)
        
#         if all_games_results.get("status") == "success":
#             predictions = all_games_results.get("predictions", [])
#             formatted_predictions = [convert_to_dict(pred) for pred in predictions]
#             results_output["all_games"] = {
#                 "status": "success",
#                 "count": len(formatted_predictions),
#                 "predictions": formatted_predictions
#             }
#         else:
#             results_output["all_games"] = {
#                 "status": all_games_results.get("status", "unknown"),
#                 "message": all_games_results.get("message", ""),
#                 "reason": all_games_results.get("reason", "")
#             }
            
#         print(json.dumps(results_output["all_games"], indent=2, default=str))
        
#     except Exception as e:
#         results_output["all_games"] = {
#             "status": "error",
#             "message": f"Failed to predict upcoming {league} games: {str(e)}"
#         }
#         print(json.dumps(results_output["all_games"], indent=2))
    
#     print("\n" + "=" * 50)
#     print("COMPLETE JSON OUTPUT")
#     print("=" * 50)
#     print(json.dumps(results_output, indent=2, default=str))
    
#     # Create output filename based on league
#     output_filename = f'{league.lower()}_predictions_output.json'
#     with open(output_filename, 'w') as f:
#         json.dump(results_output, f, indent=2, default=str)
#     print(f"Complete results saved to {output_filename}")

# if __name__ == "__main__":
#     asyncio.run(main())





# import os
# import json
# import asyncio
# from dotenv import load_dotenv
# from agents.manager_agent import predict_games
# from tools.web_search_tool import WebSearchTools

# # Load environment variables
# load_dotenv()

# def convert_to_dict(obj):
#     """Helper function to convert pydantic models to dict"""
#     if hasattr(obj, 'dict'):
#         return obj.dict()
#     elif hasattr(obj, 'model_dump'):
#         return obj.model_dump()
#     return obj

# async def main():
#     # Set the target league here - can be "NFL", "NBA", "MLB", "NHL", "EPL", etc.
#     league = "NBA"  # Change this variable to the desired league
    
#     # Get league sources from WebSearchTools
#     # These sources will be used by the agents
#     league_sources = WebSearchTools.get_league_sources(league)
    
#     # Set specific teams for a matchup
#     specific_matchup =  ["New York Knicks", "Cleveland Cavaliers"]
    
#     results_output = {
#         "specific_matchup": None,
#         "all_games": None
#     }
    
#     # Get predictions for specific teams
#     try:
#         print("=" * 50)
#         print(f"Predicting specific {league} matchup: {' vs '.join(specific_matchup)}")
#         print("=" * 50)
        
#         specific_results = await predict_games(league, teams=specific_matchup)
        
#         if specific_results.get("status") == "success":
#             predictions = specific_results.get("predictions", [])
#             formatted_predictions = [convert_to_dict(pred) for pred in predictions]
#             results_output["specific_matchup"] = {
#                 "status": "success",
#                 "count": len(formatted_predictions),
#                 "predictions": formatted_predictions
#             }
#         else:
#             results_output["specific_matchup"] = {
#                 "status": specific_results.get("status", "unknown"),
#                 "message": specific_results.get("message", ""),
#                 "reason": specific_results.get("reason", "")
#             }
            
#         print(json.dumps(results_output["specific_matchup"], indent=2, default=str))
        
#     except Exception as e:
#         results_output["specific_matchup"] = {
#             "status": "error",
#             "message": f"Failed to predict specific {league} matchup: {str(e)}"
#         }
#         print(json.dumps(results_output["specific_matchup"], indent=2))
    
#     # Get predictions for all upcoming games
#     try:
#         print("\n" + "=" * 50)
#         print(f"Predicting all upcoming {league} games")
#         print("=" * 50)
        
#         all_games_results = await predict_games(league)
        
#         if all_games_results.get("status") == "success":
#             predictions = all_games_results.get("predictions", [])
#             formatted_predictions = [convert_to_dict(pred) for pred in predictions]
#             results_output["all_games"] = {
#                 "status": "success",
#                 "count": len(formatted_predictions),
#                 "predictions": formatted_predictions
#             }
#         else:
#             results_output["all_games"] = {
#                 "status": all_games_results.get("status", "unknown"),
#                 "message": all_games_results.get("message", ""),
#                 "reason": all_games_results.get("reason", "")
#             }
            
#         print(json.dumps(results_output["all_games"], indent=2, default=str))
        
#     except Exception as e:
#         results_output["all_games"] = {
#             "status": "error",
#             "message": f"Failed to predict upcoming {league} games: {str(e)}"
#         }
#         print(json.dumps(results_output["all_games"], indent=2))
    
#     print("\n" + "=" * 50)
#     print("COMPLETE JSON OUTPUT")
#     print("=" * 50)
#     print(json.dumps(results_output, indent=2, default=str))
    
#     # Create output filename based on league
#     output_filename = f'{league.lower()}_predictions_output.json'
#     with open(output_filename, 'w') as f:
#         json.dump(results_output, f, indent=2, default=str)
#     print(f"Complete results saved to {output_filename}")

# if __name__ == "__main__":
#     asyncio.run(main())





# import os
# import json
# import asyncio
# from dotenv import load_dotenv
# from agents.manager_agent import predict_games
# from tools.web_search_tool import WebSearchTools

# load_dotenv()

# def convert_to_dict(obj):
#     if hasattr(obj, 'dict'):
#         return obj.dict()
#     elif hasattr(obj, 'model_dump'):
#         return obj.model_dump()
#     return obj

# async def main():
#     league = "NBA"  # Change this variable to the desired league
#     league_sources = WebSearchTools.get_league_sources(league)
#     print(f"[DEBUG] Main: Retrieved league sources for {league}: {league_sources}")
    
#     specific_matchup =  ["LA Clippers", "Houston Rockets"]
#     results_output = {
#         "specific_matchup": None,
#         "all_games": None
#     }
    
#     try:
#         print("=" * 50)
#         print(f"[DEBUG] Predicting specific {league} matchup: {' vs '.join(specific_matchup)}")
#         print("=" * 50)
        
#         specific_results = await predict_games(league, teams=specific_matchup)
#         if specific_results.get("status") == "success":
#             predictions = specific_results.get("predictions", [])
#             formatted_predictions = [convert_to_dict(pred) for pred in predictions]
#             results_output["specific_matchup"] = {
#                 "status": "success",
#                 "count": len(formatted_predictions),
#                 "predictions": formatted_predictions
#             }
#         else:
#             results_output["specific_matchup"] = {
#                 "status": specific_results.get("status", "unknown"),
#                 "message": specific_results.get("message", ""),
#                 "reason": specific_results.get("reason", "")
#             }
#         print(json.dumps(results_output["specific_matchup"], indent=2, default=str))
        
#     except Exception as e:
#         results_output["specific_matchup"] = {
#             "status": "error",
#             "message": f"Failed to predict specific {league} matchup: {str(e)}"
#         }
#         print(json.dumps(results_output["specific_matchup"], indent=2))
    
#     # try:
#     #     print("\n" + "=" * 50)
#     #     print(f"[DEBUG] Predicting all upcoming {league} games")
#     #     print("=" * 50)
        
#     #     all_games_results = await predict_games(league)
#     #     if all_games_results.get("status") == "success":
#     #         predictions = all_games_results.get("predictions", [])
#     #         formatted_predictions = [convert_to_dict(pred) for pred in predictions]
#     #         results_output["all_games"] = {
#     #             "status": "success",
#     #             "count": len(formatted_predictions),
#     #             "predictions": formatted_predictions
#     #         }
#     #     else:
#     #         results_output["all_games"] = {
#     #             "status": all_games_results.get("status", "unknown"),
#     #             "message": all_games_results.get("message", ""),
#     #             "reason": all_games_results.get("reason", "")
#     #         }
#     #     print(json.dumps(results_output["all_games"], indent=2, default=str))
        
#     # except Exception as e:
#     #     results_output["all_games"] = {
#     #         "status": "error",
#     #         "message": f"Failed to predict upcoming {league} games: {str(e)}"
#     #     }
#     #     print(json.dumps(results_output["all_games"], indent=2))
    
#     print("\n" + "=" * 50)
#     print("[DEBUG] COMPLETE JSON OUTPUT")
#     print("=" * 50)
#     print(json.dumps(results_output, indent=2, default=str))
    
#     output_filename = f'{league.lower()}_predictions_output.json'
#     with open(output_filename, 'w') as f:
#         json.dump(results_output, f, indent=2, default=str)
#     print(f"[DEBUG] Complete results saved to {output_filename}")

# if __name__ == "__main__":
#     asyncio.run(main())




import os
import json
import asyncio
from dotenv import load_dotenv
from agents.manager_agent import predict_games
from tools.web_search_tool import WebSearchTools

load_dotenv()

def convert_to_dict(obj):
    if hasattr(obj, 'dict'):
        return obj.dict()
    elif hasattr(obj, 'model_dump'):
        return obj.model_dump()
    return obj

async def main():
    league = "NBA"  # Change this variable to the desired league
    league_sources = WebSearchTools.get_league_sources(league)
    print(f"[DEBUG] Main: Retrieved league sources for {league}: {league_sources}")
    
    # Specific matchup predictions for the specified teams
    specific_matchup = ["Milwaukee Bucks", "New Orleans Pelicans"]
    print(f"[DEBUG] Main: Will predict matchup between {specific_matchup[0]} and {specific_matchup[1]}")
    
    results_output = {
        "specific_matchup": None,
    }
    
    try:
        print("=" * 50)
        print(f"[DEBUG] Main: Predicting specific {league} matchup: {' vs '.join(specific_matchup)}")
        print("=" * 50)
        
        # Call predict_games with the specific teams
        specific_results = await predict_games(league, teams=specific_matchup, provided_links=league_sources)
        print(f"[DEBUG] Main: Received prediction results with status: {specific_results.get('status')}")
        
        if specific_results.get("status") == "success":
            predictions = specific_results.get("predictions", [])
            print(f"[DEBUG] Main: Successfully extracted {len(predictions)} predictions")
            
            # Convert predictions to dictionaries for serialization
            formatted_predictions = [convert_to_dict(pred) for pred in predictions]
            
            # Store the results in the output dictionary
            results_output["specific_matchup"] = {
                "status": "success",
                "count": len(formatted_predictions),
                "predictions": formatted_predictions
            }
        else:
            # Handle error cases
            print(f"[WARNING] Main: Prediction failed with status: {specific_results.get('status')}")
            results_output["specific_matchup"] = {
                "status": specific_results.get("status", "unknown"),
                "message": specific_results.get("message", ""),
                "reason": specific_results.get("reason", "")
            }
            
        # Print the results
        print(json.dumps(results_output["specific_matchup"], indent=2, default=str))
        
    except Exception as e:
        print(f"[ERROR] Main: Exception occurred during prediction: {str(e)}")
        results_output["specific_matchup"] = {
            "status": "error",
            "message": f"Failed to predict specific {league} matchup: {str(e)}"
        }
        print(json.dumps(results_output["specific_matchup"], indent=2))
    
    print("\n" + "=" * 50)
    print("[DEBUG] Main: COMPLETE JSON OUTPUT")
    print("=" * 50)
    print(json.dumps(results_output, indent=2, default=str))
    
    # Save the results to a file
    output_filename = f'{league.lower()}_predictions_output.json'
    with open(output_filename, 'w') as f:
        json.dump(results_output, f, indent=2, default=str)
    print(f"[DEBUG] Main: Complete results saved to {output_filename}")

if __name__ == "__main__":
    asyncio.run(main())