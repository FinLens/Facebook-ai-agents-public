from typing import Dict, Any, List
from .base_agent import BaseAgent
import pandas as pd
from crewai import Agent

class CampaignStrategyAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agent = self.create_crew_agent(
            name="Campaign Strategist",
            role="Facebook Ads Campaign Strategy Expert",
            goal="Develop and optimize Facebook ad campaign strategies for maximum ROI",
            backstory="Expert in Facebook advertising with deep knowledge of campaign "
                     "structure, audience targeting, and budget optimization"
        )
        
    def analyze_historical_data(self, campaign_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze historical campaign performance data
        
        Args:
            campaign_data: DataFrame containing historical campaign data
            
        Returns:
            Dict containing analysis results and recommendations
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
            
            # Analyze trends
            analysis['trends'] = {
                'ctr_trend': campaign_data.groupby('date')['ctr'].mean().to_dict(),
                'cpc_trend': campaign_data.groupby('date')['cpc'].mean().to_dict(),
                'conversion_trend': campaign_data.groupby('date')['conversion_rate'].mean().to_dict()
            }
            
            # Generate recommendations
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
        Generate campaign structure recommendations
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
                'initial_test_budget': daily_budget * 0.2,
                'main_campaign_budget': daily_budget * 0.8
            }
            
            # Generate ad set recommendations
            structure['ad_sets'] = [
                {
                    'name': 'Core Audience',
                    'budget_share': 0.6,
                    'targeting': target_audience
                },
                {
                    'name': 'Lookalike Audience',
                    'budget_share': 0.3,
                    'targeting': {
                        'source': 'website_visitors',
                        'percentage': 1
                    }
                },
                {
                    'name': 'Retargeting',
                    'budget_share': 0.1,
                    'targeting': {
                        'source': 'website_visitors',
                        'days': 30
                    }
                }
            ]
            
            # Add targeting recommendations
            structure['targeting_recommendations'] = {
                'suggested_interests': self._get_relevant_interests(target_audience),
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
        Set performance targets for the campaign
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
                targets['ctr'] *= 1.2
                targets['cpc'] *= 0.8
            elif campaign_type == 'CONVERSIONS':
                targets['conversion_rate'] *= 1.2
                targets['roas'] *= 1.15
                
            return targets
            
        except Exception as e:
            self.handle_error(e, {'method': 'set_performance_targets'})
            return {}
            
    def optimize_budget_allocation(self,
                                 total_budget: float,
                                 campaign_structure: Dict[str, Any],
                                 performance_history: Dict[str, Any]) -> Dict[str, float]:
        """
        Optimize budget allocation across campaign components
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
        """Helper method to calculate performance score"""
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
        
    def _get_relevant_interests(self, target_audience: Dict[str, Any]) -> List[str]:
        """Helper method to suggest relevant interests"""
        # This would typically involve API calls to Facebook's targeting API
        base_interests = target_audience.get('interests', [])
        related_interests = []
        
        # Add related interests based on base interests
        interest_mapping = {
            'technology': ['software', 'gadgets', 'innovation'],
            'digital marketing': ['social media', 'content marketing', 'SEO'],
            # Add more mappings as needed
        }
        
        for interest in base_interests:
            related_interests.extend(interest_mapping.get(interest, []))
            
        return list(set(related_interests))
        
    def _optimize_age_range(self, target_audience: Dict[str, Any]) -> Dict[str, int]:
        """Helper method to optimize age range"""
        current_min = target_audience.get('age_min', 18)
        current_max = target_audience.get('age_max', 65)
        
        # Apply optimization logic
        optimized = {
            'age_min': max(18, current_min - 2),  # Slightly expand age range
            'age_max': min(65, current_max + 2)
        }
        
        return optimized
        
    def _get_placement_recommendations(self, business_objective: str) -> List[str]:
        """Helper method to get placement recommendations"""
        base_placements = ['facebook_feed', 'instagram_feed']
        
        if business_objective == 'AWARENESS':
            base_placements.extend(['facebook_stories', 'instagram_stories'])
        elif business_objective == 'CONVERSIONS':
            base_placements.extend(['facebook_marketplace', 'facebook_search_results'])
            
        return base_placements
