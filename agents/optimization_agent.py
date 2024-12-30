from typing import Dict, Any, List
from .base_agent import BaseAgent
import pandas as pd
from datetime import datetime, timedelta
import os

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
        Monitor campaign performance metrics and generate alerts.
        
        This method performs several key functions:
        1. Fetches recent performance data for specified metrics
        2. Analyzes performance trends
        3. Generates alerts for significant changes
        4. Provides optimization recommendations
        
        Args:
            campaign_id: Facebook campaign ID to monitor
            metrics: List of metrics to track (e.g., ['ctr', 'cpa', 'roas'])
            time_window: Time period for analysis (e.g., "1d" for 1 day, "7d" for 7 days)
            
        Returns:
            Dict containing monitoring results, alerts, and recommendations
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
            
            # Analyze performance trends
            monitoring_results['trends'] = self._analyze_trends(performance_data, metrics)
            
            # Generate performance alerts
            monitoring_results['alerts'] = self._generate_performance_alerts(
                monitoring_results['metrics'],
                monitoring_results['trends']
            )
            
            # Generate optimization recommendations
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
        Optimize bidding strategy based on performance data.
        
        This method:
        1. Analyzes current bid performance against targets
        2. Calculates optimal bid adjustments
        3. Recommends bid strategy changes
        4. Estimates impact of changes
        
        Args:
            ad_set_id: Facebook ad set ID to optimize
            performance_data: Current performance metrics
            target_metrics: Target values for key metrics (e.g., {'cpa': 50.0, 'roas': 2.0})
            
        Returns:
            Dict containing bid optimization recommendations and expected impact
        """
        try:
            optimization_result = {
                'ad_set_id': ad_set_id,
                'bid_adjustments': [],
                'strategy_changes': [],
                'expected_impact': {}
            }
            
            current_cpa = self._calculate_metric(performance_data, 'cpa')
            current_roas = self._calculate_metric(performance_data, 'roas')
            
            # Check if CPA is too high
            if current_cpa > target_metrics.get('cpa', float('inf')):
                optimization_result['bid_adjustments'].append({
                    'action': 'decrease_bid',
                    'amount': min(0.9, target_metrics['cpa'] / current_cpa),
                    'reason': 'CPA above target'
                })
            
            # Check if ROAS is too low
            if current_roas < target_metrics.get('roas', 0):
                optimization_result['strategy_changes'].append({
                    'action': 'adjust_optimization_goal',
                    'current': 'CONVERSIONS',
                    'recommended': 'VALUE',
                    'reason': 'ROAS below target'
                })
            
            # Estimate impact of changes
            optimization_result['expected_impact'] = {
                'cpa': current_cpa * 0.9 if optimization_result['bid_adjustments'] else current_cpa,
                'roas': current_roas * 1.1 if optimization_result['strategy_changes'] else current_roas
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
        Optimize audience targeting based on performance data and insights.
        
        This method performs several optimizations:
        1. Analyzes audience segment performance
        2. Identifies opportunities for expansion
        3. Recommends segments to exclude
        4. Suggests lookalike audiences
        
        Args:
            ad_set_id: Facebook ad set ID to optimize
            audience_insights: Audience performance data and demographics
            performance_data: Current performance metrics
            
        Returns:
            Dict containing audience optimization recommendations
        """
        try:
            optimization_result = {
                'ad_set_id': ad_set_id,
                'expansion_recommendations': [],
                'exclusion_recommendations': [],
                'lookalike_recommendations': [],
                'expected_impact': {}
            }
            
            # Analyze performance by audience segment
            segment_performance = self._analyze_audience_segments(
                audience_insights,
                performance_data
            )
            
            # Generate expansion recommendations
            optimization_result['expansion_recommendations'] = \
                self._generate_audience_expansion_recommendations(segment_performance)
            
            # Generate exclusion recommendations
            optimization_result['exclusion_recommendations'] = \
                self._generate_exclusion_recommendations(segment_performance)
            
            # Estimate impact
            current_cpa = self._calculate_metric(performance_data, 'cpa')
            current_conversion_rate = self._calculate_metric(performance_data, 'conversion_rate')
            
            optimization_result['expected_impact'] = {
                'audience_size': '+20%' if optimization_result['expansion_recommendations'] else '0%',
                'cpa': f"-{len(optimization_result['exclusion_recommendations']) * 5}%",
                'conversion_rate': f"+{len(optimization_result['expansion_recommendations']) * 2}%"
            }
            
            return optimization_result
            
        except Exception as e:
            self.handle_error(e, {'method': 'optimize_audience'})
            return {}
            
    def optimize_placements(self,
                          ad_set_id: str,
                          placement_performance: Dict[str, Any],
                          budget_constraints: Dict[str, float]) -> Dict[str, Any]:
        """
        Optimize ad placements based on performance data.
        
        This method:
        1. Analyzes performance by placement
        2. Identifies opportunities for budget reallocation
        3. Recommends placement adjustments
        4. Estimates impact of changes
        
        Args:
            ad_set_id: Facebook ad set ID to optimize
            placement_performance: Performance data by placement
            budget_constraints: Budget constraints for optimization
            
        Returns:
            Dict containing placement optimization recommendations and expected impact
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
            
            # Calculate optimal budget allocation
            optimization_result['budget_allocation'] = self._calculate_placement_budget_allocation(
                placement_metrics,
                budget_constraints
            )
            
            # Generate placement adjustments
            for placement, metrics in placement_metrics.items():
                if metrics['cpa'] > placement_performance.get('target_cpa', float('inf')) * 1.2:
                    optimization_result['placement_adjustments'].append({
                        'placement': placement,
                        'action': 'pause',
                        'reason': 'CPA significantly above target'
                    })
                elif metrics['roas'] < float(os.getenv('MIN_ROAS', 2.0)):
                    optimization_result['placement_adjustments'].append({
                        'placement': placement,
                        'action': 'reduce_budget',
                        'amount': -0.3,  # Reduce by 30%
                        'reason': 'ROAS below minimum threshold'
                    })
                elif metrics['roas'] > float(os.getenv('MIN_ROAS', 2.0)) * 1.5:
                    optimization_result['placement_adjustments'].append({
                        'placement': placement,
                        'action': 'increase_budget',
                        'amount': 0.2,  # Increase by 20%
                        'reason': 'Strong ROAS performance'
                    })
            
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
        Adjust budget allocation based on performance.
        
        This method:
        1. Analyzes campaign performance
        2. Checks budget constraints
        3. Recommends budget adjustments
        
        Args:
            campaign_id: Facebook campaign ID to adjust budget for
            performance_data: Current performance metrics
            budget_constraints: Budget constraints for optimization
            
        Returns:
            Dict containing budget adjustment recommendations
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
            
    def _fetch_performance_data(self,
                              campaign_id: str,
                              metrics: List[str],
                              time_window: str) -> Dict[str, Any]:
        """Helper method to fetch performance data from Facebook API"""
        window_value = int(time_window[:-1])
        window_unit = time_window[-1]
        
        if window_unit == 'd':
            start_date = datetime.now() - timedelta(days=window_value)
        elif window_unit == 'w':
            start_date = datetime.now() - timedelta(weeks=window_value)
        else:
            raise ValueError(f"Unsupported time window unit: {window_unit}")
            
        return self.fb_service.get_campaign_data(campaign_id, start_date)
        
    def _calculate_metric(self, data: Dict[str, Any], metric: str) -> float:
        """Helper method to calculate specific metrics"""
        try:
            if metric == 'ctr':
                return (data.get('clicks', 0) / data.get('impressions', 1)) * 100
            elif metric == 'cpc':
                return data.get('spend', 0) / max(data.get('clicks', 1), 1)
            elif metric == 'conversion_rate':
                return (data.get('conversions', 0) / max(data.get('clicks', 1), 1)) * 100
            elif metric == 'cpa':
                return data.get('spend', 0) / max(data.get('conversions', 1), 1)
            elif metric == 'roas':
                return data.get('revenue', 0) / max(data.get('spend', 1), 1)
            else:
                return data.get(metric, 0)
        except Exception:
            return 0
            
    def _analyze_trends(self,
                       performance_data: Dict[str, Any],
                       metrics: List[str]) -> Dict[str, str]:
        """Helper method to analyze metric trends"""
        trends = {}
        for metric in metrics:
            current_value = self._calculate_metric(performance_data, metric)
            previous_value = self._calculate_metric(
                self._get_previous_period_data(performance_data),
                metric
            )
            
            if current_value > previous_value * 1.1:
                trends[metric] = 'increasing'
            elif current_value < previous_value * 0.9:
                trends[metric] = 'decreasing'
            else:
                trends[metric] = 'stable'
                
        return trends
        
    def _get_previous_period_data(self, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Helper method to get previous period data"""
        # This would typically fetch historical data
        # For now, return estimated previous data
        return {
            key: value * 0.9 for key, value in current_data.items()
            if isinstance(value, (int, float))
        }
        
    def _generate_performance_alerts(self,
                                   metrics: Dict[str, float],
                                   trends: Dict[str, str]) -> List[Dict[str, Any]]:
        """Helper method to generate performance alerts"""
        alerts = []
        
        # Define alert thresholds
        thresholds = {
            'ctr': 1.0,  # 1% CTR
            'conversion_rate': 2.0,  # 2% conversion rate
            'roas': 2.0  # 2x ROAS
        }
        
        # Check each metric against threshold
        for metric, value in metrics.items():
            if metric in thresholds and value < thresholds[metric]:
                alerts.append({
                    'metric': metric,
                    'current_value': value,
                    'threshold': thresholds[metric],
                    'trend': trends.get(metric, 'stable'),
                    'severity': 'high' if value < thresholds[metric] * 0.5 else 'medium'
                })
                
        return alerts
        
    def _generate_optimization_recommendations(self,
                                            metrics: Dict[str, float],
                                            trends: Dict[str, str],
                                            alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Helper method to generate optimization recommendations"""
        recommendations = []
        
        # Handle low CTR
        if metrics.get('ctr', 0) < 1.0:
            recommendations.append({
                'type': 'creative',
                'action': 'refresh_creatives',
                'reason': 'Low CTR indicates ad creative fatigue',
                'priority': 'high' if metrics.get('ctr', 0) < 0.5 else 'medium'
            })
            
        # Handle high CPA
        if metrics.get('cpa', 0) > metrics.get('target_cpa', 100):
            recommendations.append({
                'type': 'bidding',
                'action': 'optimize_bidding',
                'reason': 'CPA above target',
                'priority': 'high'
            })
            
        # Handle low ROAS
        if metrics.get('roas', 0) < 2.0:
            recommendations.append({
                'type': 'targeting',
                'action': 'refine_targeting',
                'reason': 'Low ROAS indicates targeting inefficiency',
                'priority': 'high' if metrics.get('roas', 0) < 1.0 else 'medium'
            })
            
        return recommendations
        
    def _analyze_audience_segments(self,
                                 audience_insights: Dict[str, Any],
                                 performance_data: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Helper method to analyze audience segment performance"""
        segments = {}
        
        # This would typically analyze real segment data
        # For now, return sample analysis
        segments['core_audience'] = {
            'ctr': 2.1,
            'conversion_rate': 3.2,
            'cpa': 25.0,
            'roas': 2.5
        }
        
        segments['lookalike_audience'] = {
            'ctr': 1.8,
            'conversion_rate': 2.7,
            'cpa': 30.0,
            'roas': 2.0
        }
        
        return segments
        
    def _generate_audience_expansion_recommendations(self,
                                                   segment_performance: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """Helper method to generate audience expansion recommendations"""
        recommendations = []
        
        for segment, metrics in segment_performance.items():
            if metrics['roas'] > 2.0:
                recommendations.append({
                    'segment': segment,
                    'action': 'expand_audience',
                    'method': 'lookalike',
                    'parameters': {
                        'percentage': 1,
                        'country': 'US'
                    }
                })
                
        return recommendations
        
    def _generate_exclusion_recommendations(self,
                                          segment_performance: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """Helper method to generate audience exclusion recommendations"""
        recommendations = []
        
        for segment, metrics in segment_performance.items():
            if metrics['cpa'] > 50.0:  # Example threshold
                recommendations.append({
                    'segment': segment,
                    'action': 'exclude_audience',
                    'reason': 'High CPA',
                    'expected_impact': {
                        'cpa_reduction': '20%',
                        'spend_efficiency': '15%'
                    }
                })
                
        return recommendations
        
    def _calculate_placement_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Helper method to calculate placement-specific metrics"""
        return {
            'ctr': (data.get('clicks', 0) / max(data.get('impressions', 1), 1)) * 100,
            'cpc': data.get('spend', 0) / max(data.get('clicks', 1), 1),
            'conversion_rate': (data.get('conversions', 0) / max(data.get('clicks', 1), 1)) * 100,
            'cpa': data.get('spend', 0) / max(data.get('conversions', 1), 1),
            'roas': data.get('revenue', 0) / max(data.get('spend', 1), 1),
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
