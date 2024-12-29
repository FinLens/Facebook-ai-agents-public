from crewai import Crew, Task
from agents.campaign_strategy_agent import CampaignStrategyAgent
from agents.creative_management_agent import CreativeManagementAgent
from agents.optimization_agent import OptimizationAgent
from agents.reporting_agent import ReportingAgent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class FacebookAdsCrew:
    def __init__(self):
        # Initialize agents
        self.strategy_agent = CampaignStrategyAgent()
        self.creative_agent = CreativeManagementAgent()
        self.optimization_agent = OptimizationAgent()
        self.reporting_agent = ReportingAgent()
        
    def create_campaign_tasks(self, campaign_config: dict) -> list:
        """Create tasks for campaign management"""
        tasks = [
            Task(
                description="Analyze historical data and create campaign strategy",
                agent=self.strategy_agent.agent
            ),
            Task(
                description="Monitor and optimize creative performance",
                agent=self.creative_agent.agent
            ),
            Task(
                description="Optimize campaign performance metrics",
                agent=self.optimization_agent.agent
            ),
            Task(
                description="Generate performance reports and insights",
                agent=self.reporting_agent.agent
            )
        ]
        return tasks
        
    def run_crew(self, campaign_config: dict):
        """Run the Facebook Ads management crew"""
        # Create crew with tasks
        tasks = self.create_campaign_tasks(campaign_config)
        crew = Crew(
            agents=[
                self.strategy_agent.agent,
                self.creative_agent.agent,
                self.optimization_agent.agent,
                self.reporting_agent.agent
            ],
            tasks=tasks,
            verbose=True
        )
        
        # Execute crew tasks
        result = crew.kickoff()
        return result

if __name__ == "__main__":
    # Example campaign configuration
    campaign_config = {
        "objective": "CONVERSIONS",
        "budget": 1000.0,
        "target_audience": {
            "age_min": 25,
            "age_max": 45,
            "genders": ["MALE", "FEMALE"],
            "interests": ["technology", "digital marketing"]
        }
    }
    
    # Initialize and run crew
    fb_crew = FacebookAdsCrew()
    result = fb_crew.run_crew(campaign_config)
    print("Crew execution completed:", result)
