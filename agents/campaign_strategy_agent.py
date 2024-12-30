from typing import Dict, Any, List
from .base_agent import BaseAgent
import pandas as pd
from crewai import Agent
import os

class CampaignStrategyAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agent = self.create_crew_agent(
            name="Campaign Strategist",
            role="Facebook Ads Campaign Strategy Expert",
            goal="Optimize campaign structure and targeting strategy",
            backstory="Expert in Facebook advertising with deep knowledge of campaign "
                     "structure, audience targeting, and budget optimization"
        )
        
    def analyze_historical_data(self, campaign_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze historical campaign performance data to identify patterns and insights.
        
        This method:
        1. Calculates key performance metrics
        2. Identifies performance trends over time
        3. Generates data-driven recommendations
        
        Args:
            campaign_data: DataFrame containing historical campaign performance data
            
        Returns:
            Dict containing analysis results and strategic recommendations
        """
        try:
            analysis = {
                'performance_metrics': {},
                'trends': {},
                'recommendations': []
            }
            
            # Calculate key performance metrics
            analysis['performance_metrics'] = {
                'average_ctr': campaign_data['ctr'].mean(),
                'average_cpc': campaign_data['cpc'].mean(),
                'average_conversion_rate': campaign_data['conversion_rate'].mean(),
                'average_roas': campaign_data['roas'].mean()
            }
            
            # Analyze trends over time
            analysis['trends'] = {
                'ctr_trend': campaign_data.groupby('date')['ctr'].mean().to_dict(),
                'cpc_trend': campaign_data.groupby('date')['cpc'].mean().to_dict(),
                'conversion_trend': campaign_data.groupby('date')['conversion_rate'].mean().to_dict()
            }
            
            # Generate data-driven recommendations
            recommendations = []
            if analysis['performance_metrics']['average_ctr'] < 1.0:
                recommendations.append("Consider refreshing ad creatives to improve CTR")
            if analysis['performance_metrics']['average_roas'] < 2.0:
                recommendations.append("Optimize targeting to improve ROAS")
                
            analysis['recommendations'] = recommendations
            return analysis
            
        except Exception as e:
            self.handle_error(e, {'method': 'analyze_historical_data'})
            return {}
            
    def recommend_campaign_structure(self, 
                                   business_objective: str,
                                   budget: float,
                                   target_audience: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive campaign structure recommendations.
        
        This method provides recommendations for:
        1. Campaign objective and budget allocation
        2. Ad set structure and targeting
        3. Placement strategies
        4. Audience targeting refinements
        
        Args:
            business_objective: Campaign objective (e.g., CONVERSIONS, AWARENESS)
            budget: Total campaign budget
            target_audience: Target audience specifications
            
        Returns:
            Dict containing campaign structure recommendations
        """
        try:
            structure = {
                'campaign_objective': business_objective,
                'budget_allocation': {},
                'ad_sets': [],
                'targeting_recommendations': {}
            }
            
            # Define budget allocation strategy
            daily_budget = budget / 30  # Assuming monthly budget
            structure['budget_allocation'] = {
                'daily_budget': daily_budget,
                'initial_test_budget': daily_budget * 0.2,  # 20% for testing
                'main_campaign_budget': daily_budget * 0.8   # 80% for main campaign
            }
            
            # Generate ad set recommendations
            structure['ad_sets'] = [
                {
                    'name': 'Core Audience',
                    'budget_share': 0.6,  # 60% of budget
                    'targeting': target_audience
                },
                {
                    'name': 'Lookalike Audience',
                    'budget_share': 0.3,  # 30% of budget
                    'targeting': {
                        'source': 'website_visitors',
                        'percentage': 1
                    }
                },
                {
                    'name': 'Retargeting',
                    'budget_share': 0.1,  # 10% of budget
                    'targeting': {
                        'source': 'website_visitors',
                        'days': 30
                    }
                }
            ]
            
            # Add targeting recommendations
            structure['targeting_recommendations'] = {
                'suggested_interests': self._get_relevant_interests(target_audience.get('interests', [])),
                'age_range_adjustment': self._optimize_age_range(target_audience),
                'placement_recommendations': self._get_placement_recommendations(business_objective)
            }
            
            return structure
            
        except Exception as e:
            self.handle_error(e, {'method': 'recommend_campaign_structure'})
            return {}
            
    def set_performance_targets(self,
                              campaign_type: str,
                              historical_performance: Dict[str, float],
                              budget: float) -> Dict[str, float]:
        """
        Set realistic performance targets based on historical data and campaign type.
        
        This method:
        1. Analyzes historical performance
        2. Adjusts targets based on campaign type
        3. Sets improvement goals
        4. Considers budget constraints
        
        Args:
            campaign_type: Type of campaign (e.g., AWARENESS, CONVERSIONS)
            historical_performance: Historical performance metrics
            budget: Campaign budget
            
        Returns:
            Dict containing performance targets for key metrics
        """
        try:
            # Base targets on historical performance with improvement goals
            improvement_factor = 1.1  # 10% improvement target
            
            targets = {
                'ctr': max(historical_performance.get('ctr', 0) * improvement_factor, 1.0),
                'cpc': min(historical_performance.get('cpc', 0) / improvement_factor, budget * 0.1),
                'conversion_rate': max(historical_performance.get('conversion_rate', 0) * improvement_factor, 2.0),
                'roas': max(historical_performance.get('roas', 0) * improvement_factor, 2.0)
            }
            
            # Adjust targets based on campaign type
            if campaign_type == 'AWARENESS':
                targets['ctr'] *= 1.2  # Higher CTR target for awareness
                targets['cpc'] *= 0.8  # Lower CPC target for awareness
            elif campaign_type == 'CONVERSIONS':
                targets['conversion_rate'] *= 1.2  # Higher conversion target
                targets['roas'] *= 1.15  # Higher ROAS target
                
            return targets
            
        except Exception as e:
            self.handle_error(e, {'method': 'set_performance_targets'})
            return {}
            
    def optimize_budget_allocation(self,
                                 total_budget: float,
                                 campaign_structure: Dict[str, Any],
                                 performance_history: Dict[str, Any]) -> Dict[str, float]:
        """
        Optimize budget allocation across campaign components.
        
        This method:
        1. Analyzes performance history
        2. Calculates performance scores for each ad set
        3. Allocates budget based on performance scores
        
        Args:
            total_budget: Total campaign budget
            campaign_structure: Campaign structure recommendations
            performance_history: Performance history for each ad set
            
        Returns:
            Dict containing optimized budget allocation for each ad set
        """
        try:
            allocation = {}
            
            # Calculate performance scores for each ad set
            performance_scores = {}
            for ad_set in campaign_structure['ad_sets']:
                ad_set_history = performance_history.get(ad_set['name'], {})
                score = self._calculate_performance_score(ad_set_history)
                performance_scores[ad_set['name']] = score
                
            # Normalize scores and allocate budget
            total_score = sum(performance_scores.values())
            for ad_set_name, score in performance_scores.items():
                allocation[ad_set_name] = (score / total_score) * total_budget
                
            return allocation
            
        except Exception as e:
            self.handle_error(e, {'method': 'optimize_budget_allocation'})
            return {}
            
    def _calculate_performance_score(self, performance_data: Dict[str, Any]) -> float:
        """
        Calculate performance score based on key metrics.
        
        This method:
        1. Weights different metrics
        2. Calculates score based on weighted metrics
        
        Args:
            performance_data: Performance data for an ad set
            
        Returns:
            Float representing performance score
        """
        if not performance_data:
            return 1.0  # Default score for new ad sets
            
        # Weight different metrics
        weights = {
            'roas': 0.4,
            'conversion_rate': 0.3,
            'ctr': 0.2,
            'cpc': 0.1
        }
        
        score = 0
        for metric, weight in weights.items():
            if metric in performance_data:
                if metric == 'cpc':
                    # Lower CPC is better
                    score += weight * (1 / max(performance_data[metric], 0.1))
                else:
                    score += weight * performance_data[metric]
                    
        return max(score, 0.1)  # Ensure minimum score
        
    def _get_relevant_interests(self, interests: List[str]) -> List[str]:
        """
        Get relevant interests using Facebook's Targeting API.
        
        Args:
            interests: List of interests
            
        Returns:
            List of relevant interests
        """
        return self.fb_service.get_relevant_interests(interests)

    def _optimize_age_range(self, targeting_spec: Dict[str, Any]) -> Dict[str, int]:
        """
        Optimize age range based on audience insights.
        
        Args:
            targeting_spec: Targeting specifications
            
        Returns:
            Dict containing optimized age range
        """
        return self.fb_service.optimize_age_range(targeting_spec)

    def _get_placement_recommendations(self, business_objective: str) -> List[str]:
        """
        Get placement recommendations using Facebook's API.
        
        Args:
            business_objective: Business objective
            
        Returns:
            List of placement recommendations
        """
        return self.fb_service.get_placement_recommendations(business_objective)
