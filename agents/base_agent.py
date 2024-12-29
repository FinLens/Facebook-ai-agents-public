from crewai import Agent
from facebook_business.api import FacebookAdsApi
import os
from typing import Dict, Any

class BaseAgent:
    def __init__(self, fb_api: FacebookAdsApi = None):
        """
        Initialize base agent with Facebook API connection
        
        Args:
            fb_api: FacebookAdsApi instance, if None will attempt to create from env vars
        """
        self.fb_api = fb_api or FacebookAdsApi.init(
            access_token=os.getenv('FB_ACCESS_TOKEN'),
            app_secret=os.getenv('FB_APP_SECRET'),
            app_id=os.getenv('FB_APP_ID')
        )
        
    def create_crew_agent(self, name: str, role: str, goal: str, backstory: str) -> Agent:
        """
        Create a CrewAI agent with the given parameters
        
        Args:
            name: Agent name
            role: Agent role description
            goal: Agent's primary goal
            backstory: Agent's backstory and context
            
        Returns:
            Agent: CrewAI Agent instance
        """
        return Agent(
            name=name,
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=True,
            allow_delegation=True
        )
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> None:
        """
        Handle errors in agent operations
        
        Args:
            error: The exception that occurred
            context: Additional context about the error
        """
        # TODO: Implement proper error handling and logging
        print(f"Error occurred: {str(error)}")
        if context:
            print(f"Context: {context}")
            
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate input data for agent operations
        
        Args:
            data: Data to validate
            
        Returns:
            bool: True if data is valid, False otherwise
        """
        # TODO: Implement data validation logic
        return True
