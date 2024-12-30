from agents.reporting_agent import ReportingAgent
from agents.optimization_agent import OptimizationAgent
from agents.campaign_strategy_agent import CampaignStrategyAgent
from agents.creative_management_agent import CreativeManagementAgent
from services.slack_bot import SlackBot
from services.slack_service import SlackService
from services.scheduler_service import SchedulerService
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class FacebookAdsCrew:
    def __init__(self):
        self.reporting_agent = ReportingAgent()
        self.optimization_agent = OptimizationAgent()
        self.campaign_strategy_agent = CampaignStrategyAgent()
        self.creative_management_agent = CreativeManagementAgent()
        
    def run_crew(self, campaign_config: dict) -> dict:
        """Run the Facebook Ads crew with the given configuration"""
        from crewai import Crew
        
        # Create crew tasks
        tasks = [
            {
                "agent": self.campaign_strategy_agent.agent,
                "task": f"Analyze the target audience and develop a campaign strategy. Target audience: {campaign_config['target_audience']}, Objective: {campaign_config['objective']}"
            },
            {
                "agent": self.creative_management_agent.agent,
                "task": f"Design creative assets based on the campaign strategy and requirements: {campaign_config['creative_requirements']}"
            },
            {
                "agent": self.optimization_agent.agent,
                "task": f"Optimize the campaign for {', '.join(campaign_config['optimization_goals'])} with budget {campaign_config['budget']}"
            },
            {
                "agent": self.reporting_agent.agent,
                "task": "Generate initial campaign performance projections and reporting framework"
            }
        ]
        
        # Create and run the crew
        crew = Crew(
            agents=[task["agent"] for task in tasks],
            tasks=[task["task"] for task in tasks],
            verbose=True
        )
        
        result = crew.kickoff()
        return result

def main():
    # Initialize Facebook Ads Crew
    fb_crew = FacebookAdsCrew()
    
    # Initialize services
    slack_service = SlackService()
    scheduler = SchedulerService()
    
    # Initialize Slack bot with all agents and crew
    slack_bot = SlackBot(
        reporting_agent=fb_crew.reporting_agent,
        optimization_agent=fb_crew.optimization_agent,
        campaign_strategy_agent=fb_crew.campaign_strategy_agent,
        fb_crew=fb_crew
    )
    
    # Schedule daily performance report
    def send_daily_report():
        campaign_ids = os.getenv('FB_CAMPAIGN_IDS', '').split(',')
        for campaign_id in campaign_ids:
            report = fb_crew.reporting_agent.generate_campaign_report(
                campaign_id=campaign_id,
                start_date=datetime.now() - timedelta(days=1)
            )
            slack_service.send_report(report, "Campaign Performance")
            
    scheduler.schedule_daily_report(send_daily_report, hour=9, minute=0)
    
    # Schedule weekly optimization report
    def send_weekly_optimization():
        campaign_ids = os.getenv('FB_CAMPAIGN_IDS', '').split(',')
        for campaign_id in campaign_ids:
            recommendations = fb_crew.optimization_agent.generate_recommendations(
                campaign_id=campaign_id
            )
            slack_service.send_report(recommendations, "Optimization Recommendations")
            
    scheduler.schedule_weekly_report(send_weekly_optimization, day_of_week='mon', hour=10, minute=0)
    
    # Schedule monthly strategy review
    def send_monthly_strategy():
        campaign_ids = os.getenv('FB_CAMPAIGN_IDS', '').split(',')
        for campaign_id in campaign_ids:
            strategy = fb_crew.campaign_strategy_agent.analyze_historical_data(
                campaign_id=campaign_id
            )
            slack_service.send_report(strategy, "Campaign Strategy")
            
    scheduler.schedule_monthly_report(send_monthly_strategy, day=1, hour=11, minute=0)
    
    # Start the Slack bot
    slack_bot.start()

if __name__ == "__main__":
    main()
