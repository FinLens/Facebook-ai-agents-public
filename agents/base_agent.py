from crewai import Agent
from services.facebook_service import FacebookService
from typing import Dict, Any
import os

class BaseAgent:
    def __init__(self):
        """Initialize base agent with common services"""
        self.fb_service = FacebookService()
        
    def create_crew_agent(self, name: str, role: str, goal: str, backstory: str) -> Agent:
        """Create a CrewAI agent with specified parameters"""
        return Agent(
            name=name,
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=True,
            allow_delegation=False
        )
        
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> None:
        """Handle and log errors with context"""
        error_msg = f"Error in {context.get('method', 'unknown method')}: {str(error)}"
        print(error_msg)  # In production, this should use proper logging
        
    def format_currency(self, amount: float) -> str:
        """Format amount as currency"""
        return f"${amount:,.2f}"
        
    def format_percentage(self, value: float) -> str:
        """Format value as percentage"""
        return f"{value:.1f}%"
        
    def calculate_change(self, current: float, previous: float) -> Dict[str, Any]:
        """Calculate change between two values"""
        if previous == 0:
            return {
                'change': 0.0,
                'percentage': 0.0,
                'direction': 'no_change'
            }
            
        change = current - previous
        percentage = (change / previous) * 100
        direction = 'increase' if change > 0 else 'decrease' if change < 0 else 'no_change'
        
        return {
            'change': change,
            'percentage': percentage,
            'direction': direction
        }
        
    def format_change(self, change_data: Dict[str, Any], include_value: bool = True) -> str:
        """Format change data into readable string"""
        if change_data['direction'] == 'no_change':
            return "No change"
            
        direction = '📈' if change_data['direction'] == 'increase' else '📉'
        change_str = f"{abs(change_data['percentage']):.1f}%"
        
        if include_value:
            value_str = self.format_currency(abs(change_data['change']))
            return f"{direction} {change_str} ({value_str})"
        
        return f"{direction} {change_str}"
