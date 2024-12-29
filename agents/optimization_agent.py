from typing import Dict, Any, List
from .base_agent import BaseAgent
import pandas as pd
from datetime import datetime

class OptimizationAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agent = self.create_crew_agent(
            name="Campaign Optimizer",
            role="Facebook Ads Optimization Specialist",
            goal="Optimize campaign performance through real-time monitoring and adjustments",
            backstory="Expert in Facebook ads optimization with deep understanding of "
                     "bidding strategies, audience targeting, and performance metrics"
        )
        
    def monitor_performance(self,
                          campaign_id: str,
                          metrics: List[str],
                          time_window: str = "1d") -> Dict[str, Any]:
        """
        Monitor campaign performance metrics
        """
        try:
            monitoring_results = {
                'campaign_id': campaign_id,
                'time_window': time_window,
                'metrics': {},
                'alerts': [],
                'trends': {},
                'recommendations': []
            }
            
            # Fetch performance data from Facebook API
            performance_data = self._fetch_performance_data(campaign_id, metrics, time_window)
            
            # Calculate current metrics
            monitoring_results['metrics'] = {
                metric: self._calculate_metric(performance_data, metric)
                for metric in metrics
            }
            
            # Analyze trends
            monitoring_results['trends'] = self._analyze_trends(performance_data, metrics)
            
            # Generate alerts
            monitoring_results['alerts'] = self._generate_performance_alerts(
                monitoring_results['metrics'],
                monitoring_results['trends']
            )
            
            # Generate recommendations
            monitoring_results['recommendations'] = self._generate_optimization_recommendations(
                monitoring_results['metrics'],
                monitoring_results['trends'],
                monitoring_results['alerts']
            )
            
            return monitoring_results
            
        except Exception as e:
            self.handle_error(e, {'method': 'monitor_performance'})
            return {}
            
    def optimize_bids(self,
                     ad_set_id: str,
                     performance_data: Dict[str, Any],
                     target_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Optimize bidding strategy based on performance
        """
        try:
            optimization_result = {
                'ad_set_id': ad_set_id,
                'current_performance': performance_data,
                'bid_adjustments': {},
                'strategy_changes': [],
                'expected_impact': {}
            }
            
            # Calculate bid adjustments
            current_cpa = performance_data.get('cpa', 0)
            target_cpa = target_metrics.get('cpa', 0)
            
            if current_cpa > 0 and target_cpa > 0:
                bid_multiplier = target_cpa / current_cpa
                
                # Apply reasonable limits to bid changes
                bid_multiplier = max(0.7, min(1.3, bid_multiplier))
                
                optimization_result['bid_adjustments'] = {
                    'multiplier': bid_multiplier,
                    'reason': f"Adjusting bid to achieve target CPA of {target_cpa}"
                }
            
            # Recommend strategy changes
            if performance_data.get('conversion_rate', 0) < target_metrics.get('conversion_rate', 0):
                optimization_result['strategy_changes'].append({
                    'type': 'bidding_strategy',
                    'change': 'switch_to_value_optimization',
                    'reason': 'Low conversion rate relative to target'
                })
            
            # Calculate expected impact
            optimization_result['expected_impact'] = {
                'cpa': current_cpa * (optimization_result['bid_adjustments'].get('multiplier', 1)),
                'spend': performance_data.get('daily_spend', 0) * (optimization_result['bid_adjustments'].get('multiplier', 1))
            }
            
            return optimization_result
            
        except Exception as e:
            self.handle_error(e, {'method': 'optimize_bids'})
            return {}
            
    def optimize_audience(self,
                        ad_set_id: str,
                        audience_insights: Dict[str, Any],
                        performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize audience targeting
        """
        try:
            optimization_result = {
                'ad_set_id': ad_set_id,
                'targeting_adjustments': [],
                'expansion_recommendations': [],
                'exclusion_recommendations': []
            }
            
            # Analyze audience performance
            performance_by_segment = self._analyze_audience_segments(audience_insights, performance_data)
            
            # Generate targeting adjustments
            for segment, metrics in performance_by_segment.items():
                if metrics['cpa'] > performance_data.get('target_cpa', float('inf')) * 1.2:
                    optimization_result['targeting_adjustments'].append({
                        'segment': segment,
                        'action': 'exclude',
                        'reason': 'High CPA relative to target'
                    })
                elif metrics['conversion_rate'] > performance_data.get('average_conversion_rate', 0) * 1.2:
                    optimization_result['targeting_adjustments'].append({
                        'segment': segment,
                        'action': 'increase_bid',
                        'reason': 'High conversion rate relative to average'
                    })
            
            # Generate expansion recommendations
            if len(optimization_result['targeting_adjustments']) > 0:
                optimization_result['expansion_recommendations'] = self._generate_audience_expansion_recommendations(
                    performance_by_segment
                )
            
            # Generate exclusion recommendations
            optimization_result['exclusion_recommendations'] = self._generate_exclusion_recommendations(
                performance_by_segment
            )
            
            return optimization_result
            
        except Exception as e:
            self.handle_error(e, {'method': 'optimize_audience'})
            return {}
            
    def optimize_placements(self,
                          ad_set_id: str,
                          placement_performance: Dict[str, Any],
                          budget_constraints: Dict[str, float]) -> Dict[str, Any]:
        """
        Optimize ad placements
        """
        try:
            optimization_result = {
                'ad_set_id': ad_set_id,
                'placement_adjustments': [],
                'budget_allocation': {},
                'expected_impact': {}
            }
            
            # Calculate performance metrics by placement
            placement_metrics = {}
            for placement, data in placement_performance.items():
                metrics = self._calculate_placement_metrics(data)
                placement_metrics[placement] = metrics
            
            # Generate placement adjustments
            total_spend = sum(metrics['spend'] for metrics in placement_metrics.values())
            for placement, metrics in placement_metrics.items():
                if metrics['cpa'] > placement_performance.get('target_cpa', float('inf')) * 1.2:
                    optimization_result['placement_adjustments'].append({
                        'placement': placement,
                        'action': 'decrease_bid',
                        'adjustment_factor': 0.8,
                        'reason': 'High CPA relative to target'
                    })
                elif metrics['roas'] > placement_performance.get('target_roas', 0) * 1.2:
                    optimization_result['placement_adjustments'].append({
                        'placement': placement,
                        'action': 'increase_bid',
                        'adjustment_factor': 1.2,
                        'reason': 'High ROAS relative to target'
                    })
            
            # Calculate budget allocation
            optimization_result['budget_allocation'] = self._calculate_placement_budget_allocation(
                placement_metrics,
                budget_constraints
            )
            
            # Calculate expected impact
            optimization_result['expected_impact'] = self._calculate_placement_optimization_impact(
                placement_metrics,
                optimization_result['placement_adjustments'],
                optimization_result['budget_allocation']
            )
            
            return optimization_result
            
        except Exception as e:
            self.handle_error(e, {'method': 'optimize_placements'})
            return {}
            
    def adjust_budget(self,
                     campaign_id: str,
                     performance_data: Dict[str, Any],
                     budget_constraints: Dict[str, float]) -> Dict[str, float]:
        """
        Adjust budget allocation based on performance
        """
        try:
            budget_adjustments = {
                'campaign_id': campaign_id,
                'adjustments': {},
                'reasons': {},
                'constraints_check': True
            }
            
            # Calculate performance metrics
            campaign_metrics = self._calculate_campaign_metrics(performance_data)
            
            # Check if we're meeting ROAS targets
            if campaign_metrics['roas'] < budget_constraints.get('target_roas', 0):
                # Reduce budget if ROAS is below target
                adjustment_factor = 0.9
                budget_adjustments['reasons']['decrease'] = 'ROAS below target'
            elif campaign_metrics['roas'] > budget_constraints.get('target_roas', 0) * 1.2:
                # Increase budget if ROAS is significantly above target
                adjustment_factor = 1.1
                budget_adjustments['reasons']['increase'] = 'ROAS significantly above target'
            else:
                adjustment_factor = 1.0
            
            # Calculate new budget
            current_budget = performance_data.get('daily_budget', 0)
            new_budget = current_budget * adjustment_factor
            
            # Check budget constraints
            min_budget = budget_constraints.get('min_daily_budget', 0)
            max_budget = budget_constraints.get('max_daily_budget', float('inf'))
            
            new_budget = max(min_budget, min(max_budget, new_budget))
            
            budget_adjustments['adjustments'] = {
                'current_budget': current_budget,
                'new_budget': new_budget,
                'adjustment_factor': adjustment_factor
            }
            
            # Verify constraints are met
            budget_adjustments['constraints_check'] = (
                new_budget >= min_budget and 
                new_budget <= max_budget
            )
            
            return budget_adjustments
            
        except Exception as e:
            self.handle_error(e, {'method': 'adjust_budget'})
            return {}
            
    def _fetch_performance_data(self, campaign_id: str, metrics: List[str], time_window: str) -> Dict[str, Any]:
        """Helper method to fetch performance data"""
        # This would typically make API calls to Facebook
        # For now, return dummy data
        return {
            'spend': 100.0,
            'impressions': 10000,
            'clicks': 200,
            'conversions': 10,
            'revenue': 500.0
        }
        
    def _calculate_metric(self, data: Dict[str, Any], metric: str) -> float:
        """Helper method to calculate individual metrics"""
        if metric == 'ctr':
            return (data.get('clicks', 0) / data.get('impressions', 1)) * 100
        elif metric == 'cpa':
            return data.get('spend', 0) / max(data.get('conversions', 1), 1)
        elif metric == 'roas':
            return data.get('revenue', 0) / max(data.get('spend', 1), 1)
        return 0.0
        
    def _analyze_trends(self, data: Dict[str, Any], metrics: List[str]) -> Dict[str, Any]:
        """Helper method to analyze performance trends"""
        trends = {}
        for metric in metrics:
            metric_value = self._calculate_metric(data, metric)
            trends[metric] = {
                'current_value': metric_value,
                'trend_direction': 'stable',  # This would be calculated from historical data
                'change_rate': 0.0  # This would be calculated from historical data
            }
        return trends
        
    def _generate_performance_alerts(self, 
                                   metrics: Dict[str, float],
                                   trends: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Helper method to generate performance alerts"""
        alerts = []
        
        # Check for significant performance changes
        for metric, data in trends.items():
            if abs(data.get('change_rate', 0)) > 0.2:  # 20% change threshold
                alerts.append({
                    'metric': metric,
                    'type': 'significant_change',
                    'direction': 'increase' if data.get('change_rate', 0) > 0 else 'decrease',
                    'magnitude': abs(data.get('change_rate', 0))
                })
                
        return alerts
        
    def _generate_optimization_recommendations(self,
                                            metrics: Dict[str, float],
                                            trends: Dict[str, Any],
                                            alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Helper method to generate optimization recommendations"""
        recommendations = []
        
        # Generate recommendations based on alerts
        for alert in alerts:
            if alert['type'] == 'significant_change' and alert['direction'] == 'decrease':
                recommendations.append({
                    'type': 'optimization',
                    'metric': alert['metric'],
                    'action': 'investigate_decline',
                    'priority': 'high'
                })
                
        return recommendations
        
    def _analyze_audience_segments(self,
                                 audience_insights: Dict[str, Any],
                                 performance_data: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Helper method to analyze audience segment performance"""
        segment_performance = {}
        
        # Calculate metrics for each segment
        for segment, data in audience_insights.items():
            segment_performance[segment] = {
                'cpa': data.get('spend', 0) / max(data.get('conversions', 1), 1),
                'conversion_rate': data.get('conversions', 0) / max(data.get('clicks', 1), 1),
                'spend': data.get('spend', 0)
            }
            
        return segment_performance
        
    def _generate_audience_expansion_recommendations(self,
                                                   performance_by_segment: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """Helper method to generate audience expansion recommendations"""
        recommendations = []
        
        # Find top performing segments
        top_segments = sorted(
            performance_by_segment.items(),
            key=lambda x: x[1]['conversion_rate'],
            reverse=True
        )[:3]
        
        # Generate recommendations for each top segment
        for segment, metrics in top_segments:
            recommendations.append({
                'segment': segment,
                'type': 'lookalike_audience',
                'percentage': 1,
                'reason': f"High conversion rate in {segment} segment"
            })
            
        return recommendations
        
    def _generate_exclusion_recommendations(self,
                                          performance_by_segment: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """Helper method to generate exclusion recommendations"""
        recommendations = []
        
        # Find underperforming segments
        for segment, metrics in performance_by_segment.items():
            if metrics['conversion_rate'] < 0.01:  # 1% conversion rate threshold
                recommendations.append({
                    'segment': segment,
                    'reason': 'Low conversion rate',
                    'metrics': metrics
                })
                
        return recommendations
        
    def _calculate_placement_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Helper method to calculate placement-specific metrics"""
        return {
            'cpa': data.get('spend', 0) / max(data.get('conversions', 1), 1),
            'roas': data.get('revenue', 0) / max(data.get('spend', 1), 1),
            'ctr': (data.get('clicks', 0) / max(data.get('impressions', 1), 1)) * 100,
            'spend': data.get('spend', 0)
        }
        
    def _calculate_placement_budget_allocation(self,
                                            placement_metrics: Dict[str, Dict[str, float]],
                                            budget_constraints: Dict[str, float]) -> Dict[str, float]:
        """Helper method to calculate budget allocation by placement"""
        total_budget = budget_constraints.get('total_budget', 0)
        allocations = {}
        
        # Calculate performance score for each placement
        total_score = 0
        scores = {}
        for placement, metrics in placement_metrics.items():
            score = metrics['roas'] * (1 / max(metrics['cpa'], 0.1))
            scores[placement] = score
            total_score += score
            
        # Allocate budget based on scores
        for placement, score in scores.items():
            allocations[placement] = (score / total_score) * total_budget
            
        return allocations
        
    def _calculate_placement_optimization_impact(self,
                                              placement_metrics: Dict[str, Dict[str, float]],
                                              adjustments: List[Dict[str, Any]],
                                              budget_allocation: Dict[str, float]) -> Dict[str, float]:
        """Helper method to calculate expected impact of placement optimizations"""
        impact = {
            'expected_cpa': 0,
            'expected_roas': 0,
            'expected_spend': 0
        }
        
        # Calculate weighted metrics based on new budget allocation
        total_budget = sum(budget_allocation.values())
        for placement, metrics in placement_metrics.items():
            budget_share = budget_allocation.get(placement, 0) / total_budget
            
            # Apply adjustment factors
            adjustment_factor = 1.0
            for adj in adjustments:
                if adj['placement'] == placement:
                    adjustment_factor = adj['adjustment_factor']
                    break
                    
            impact['expected_cpa'] += metrics['cpa'] * budget_share * adjustment_factor
            impact['expected_roas'] += metrics['roas'] * budget_share * adjustment_factor
            impact['expected_spend'] += budget_allocation.get(placement, 0)
            
        return impact
        
    def _calculate_campaign_metrics(self, performance_data: Dict[str, Any]) -> Dict[str, float]:
        """Helper method to calculate campaign-level metrics"""
        return {
            'roas': performance_data.get('revenue', 0) / max(performance_data.get('spend', 1), 1),
            'cpa': performance_data.get('spend', 0) / max(performance_data.get('conversions', 1), 1),
            'conversion_rate': performance_data.get('conversions', 0) / max(performance_data.get('clicks', 1), 1)
        }
