from typing import Dict, Any, List
from .base_agent import BaseAgent
import pandas as pd
from datetime import datetime, timedelta

class CreativeManagementAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agent = self.create_crew_agent(
            name="Creative Manager",
            role="Facebook Ads Creative Optimization Expert",
            goal="Optimize ad creative performance and prevent creative fatigue",
            backstory="Specialist in creative performance analysis and optimization "
                     "with expertise in A/B testing and creative element analysis"
        )
        
    def analyze_creative_performance(self, 
                                   creative_data: pd.DataFrame,
                                   time_window: int = 30) -> Dict[str, Any]:
        """
        Analyze performance of current creative assets
        """
        try:
            analysis = {
                'overall_metrics': {},
                'performance_by_creative': {},
                'trends': {},
                'recommendations': []
            }
            
            # Filter data for time window
            end_date = pd.Timestamp.now()
            start_date = end_date - pd.Timedelta(days=time_window)
            filtered_data = creative_data[
                (creative_data['date'] >= start_date) & 
                (creative_data['date'] <= end_date)
            ]
            
            # Calculate overall metrics
            analysis['overall_metrics'] = {
                'average_ctr': filtered_data['ctr'].mean(),
                'average_engagement_rate': filtered_data['engagement_rate'].mean(),
                'average_conversion_rate': filtered_data['conversion_rate'].mean()
            }
            
            # Analyze performance by creative
            for creative_id in filtered_data['creative_id'].unique():
                creative_metrics = filtered_data[filtered_data['creative_id'] == creative_id]
                analysis['performance_by_creative'][creative_id] = {
                    'ctr': creative_metrics['ctr'].mean(),
                    'engagement_rate': creative_metrics['engagement_rate'].mean(),
                    'conversion_rate': creative_metrics['conversion_rate'].mean(),
                    'impressions': creative_metrics['impressions'].sum()
                }
            
            # Calculate trends
            analysis['trends'] = self._calculate_performance_trends(filtered_data)
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_creative_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            self.handle_error(e, {'method': 'analyze_creative_performance'})
            return {}
            
    def detect_creative_fatigue(self,
                              creative_id: str,
                              performance_metrics: Dict[str, List[float]],
                              threshold: float = 0.15) -> Dict[str, Any]:
        """
        Detect creative fatigue based on performance trends
        """
        try:
            fatigue_analysis = {
                'creative_id': creative_id,
                'fatigue_detected': False,
                'metrics': {},
                'recommendation': None
            }
            
            # Calculate fatigue metrics for each KPI
            for metric, values in performance_metrics.items():
                if len(values) < 2:
                    continue
                    
                # Calculate rolling average
                rolling_avg = pd.Series(values).rolling(window=7).mean()
                
                # Calculate decline rate
                initial_performance = rolling_avg.iloc[7:14].mean()  # Second week average
                current_performance = rolling_avg.iloc[-7:].mean()  # Last week average
                
                if initial_performance > 0:
                    decline_rate = (initial_performance - current_performance) / initial_performance
                    fatigue_analysis['metrics'][metric] = {
                        'decline_rate': decline_rate,
                        'is_fatigued': decline_rate > threshold
                    }
                    
                    if decline_rate > threshold:
                        fatigue_analysis['fatigue_detected'] = True
            
            # Generate recommendation if fatigue detected
            if fatigue_analysis['fatigue_detected']:
                fatigue_analysis['recommendation'] = self._get_fatigue_recommendation(
                    fatigue_analysis['metrics']
                )
            
            return fatigue_analysis
            
        except Exception as e:
            self.handle_error(e, {'method': 'detect_creative_fatigue'})
            return {}
            
    def generate_ab_test_plan(self,
                             current_creative: Dict[str, Any],
                             performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate A/B testing plan for creative optimization
        """
        try:
            test_plan = {
                'test_name': f"Creative_Test_{datetime.now().strftime('%Y%m%d')}",
                'variants': [],
                'test_duration': 14,  # days
                'budget_allocation': {},
                'success_metrics': []
            }
            
            # Define variants based on current performance
            base_performance = performance_data.get('metrics', {})
            
            # Generate test variants
            test_plan['variants'] = self._generate_test_variants(current_creative)
            
            # Set budget allocation
            total_budget = current_creative.get('daily_budget', 100)
            test_plan['budget_allocation'] = {
                'control': total_budget * 0.5,  # 50% to control
                'variants': {  # Split remaining 50% among variants
                    f"variant_{i+1}": total_budget * 0.5 / len(test_plan['variants'])
                    for i in range(len(test_plan['variants']))
                }
            }
            
            # Define success metrics
            test_plan['success_metrics'] = [
                {
                    'metric': 'ctr',
                    'minimum_improvement': 0.1,  # 10% improvement
                    'confidence_level': 0.95
                },
                {
                    'metric': 'conversion_rate',
                    'minimum_improvement': 0.15,  # 15% improvement
                    'confidence_level': 0.95
                }
            ]
            
            return test_plan
            
        except Exception as e:
            self.handle_error(e, {'method': 'generate_ab_test_plan'})
            return {}
            
    def recommend_creative_rotation(self,
                                  creative_pool: List[Dict[str, Any]],
                                  fatigue_data: Dict[str, Any],
                                  performance_history: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend creative rotation schedule
        """
        try:
            rotation_plan = {
                'immediate_rotations': [],
                'scheduled_rotations': [],
                'new_creative_recommendations': []
            }
            
            # Handle immediate rotations for fatigued creatives
            for creative in creative_pool:
                creative_id = creative['id']
                if fatigue_data.get(creative_id, {}).get('fatigue_detected', False):
                    rotation_plan['immediate_rotations'].append({
                        'creative_id': creative_id,
                        'reason': 'Creative fatigue detected',
                        'recommended_action': 'pause'
                    })
            
            # Schedule future rotations based on performance trends
            for creative in creative_pool:
                if creative['id'] not in [r['creative_id'] for r in rotation_plan['immediate_rotations']]:
                    rotation_schedule = self._calculate_rotation_schedule(
                        creative,
                        performance_history.get(creative['id'], {})
                    )
                    if rotation_schedule:
                        rotation_plan['scheduled_rotations'].append(rotation_schedule)
            
            # Generate new creative recommendations
            rotation_plan['new_creative_recommendations'] = self._generate_new_creative_recommendations(
                creative_pool,
                performance_history
            )
            
            return rotation_plan
            
        except Exception as e:
            self.handle_error(e, {'method': 'recommend_creative_rotation'})
            return {}
            
    def _calculate_performance_trends(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Helper method to calculate performance trends"""
        trends = {}
        metrics = ['ctr', 'engagement_rate', 'conversion_rate']
        
        for metric in metrics:
            daily_avg = data.groupby('date')[metric].mean()
            trends[metric] = {
                'trend_direction': 'up' if daily_avg.iloc[-1] > daily_avg.iloc[0] else 'down',
                'change_rate': ((daily_avg.iloc[-1] - daily_avg.iloc[0]) / daily_avg.iloc[0])
                if daily_avg.iloc[0] != 0 else 0
            }
            
        return trends
        
    def _generate_creative_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Helper method to generate creative recommendations"""
        recommendations = []
        
        # Check overall performance
        if analysis['overall_metrics']['average_ctr'] < 1.0:
            recommendations.append("Consider refreshing ad copy to improve CTR")
        if analysis['overall_metrics']['average_engagement_rate'] < 2.0:
            recommendations.append("Test new visual elements to boost engagement")
            
        # Check individual creative performance
        for creative_id, metrics in analysis['performance_by_creative'].items():
            if metrics['ctr'] < analysis['overall_metrics']['average_ctr'] * 0.8:
                recommendations.append(f"Creative {creative_id} is underperforming in CTR - consider revision")
                
        return recommendations
        
    def _get_fatigue_recommendation(self, metrics: Dict[str, Any]) -> str:
        """Helper method to generate fatigue recommendations"""
        most_declined_metric = max(metrics.items(), key=lambda x: x[1]['decline_rate'])
        
        if most_declined_metric[0] == 'ctr':
            return "Refresh ad copy and visual elements to combat click fatigue"
        elif most_declined_metric[0] == 'conversion_rate':
            return "Update offer or call-to-action to improve conversion rate"
        else:
            return "Rotate creative to combat general performance decline"
            
    def _generate_test_variants(self, current_creative: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Helper method to generate A/B test variants"""
        variants = []
        
        # Generate copy variants
        if 'ad_copy' in current_creative:
            variants.append({
                'type': 'copy',
                'changes': {
                    'headline': self._generate_copy_variant(current_creative['ad_copy'].get('headline', '')),
                    'body': self._generate_copy_variant(current_creative['ad_copy'].get('body', ''))
                }
            })
            
        # Generate visual variants
        if 'visual_elements' in current_creative:
            variants.append({
                'type': 'visual',
                'changes': {
                    'image_layout': self._generate_visual_variant(current_creative['visual_elements'])
                }
            })
            
        return variants
        
    def _calculate_rotation_schedule(self, 
                                   creative: Dict[str, Any],
                                   performance_history: Dict[str, Any]) -> Dict[str, Any]:
        """Helper method to calculate rotation schedule"""
        if not performance_history:
            return None
            
        # Calculate optimal rotation time based on performance decay
        avg_decay_rate = self._calculate_decay_rate(performance_history)
        days_to_rotation = max(7, min(30, int(14 / avg_decay_rate))) if avg_decay_rate > 0 else 14
        
        return {
            'creative_id': creative['id'],
            'rotation_date': (datetime.now() + timedelta(days=days_to_rotation)).strftime('%Y-%m-%d'),
            'reason': 'Preventive rotation based on performance patterns'
        }
        
    def _calculate_decay_rate(self, performance_history: Dict[str, Any]) -> float:
        """Helper method to calculate performance decay rate"""
        if 'daily_ctr' not in performance_history:
            return 0.0
            
        ctr_values = performance_history['daily_ctr']
        if len(ctr_values) < 7:
            return 0.0
            
        # Calculate average daily decay
        daily_changes = [(ctr_values[i] - ctr_values[i-1]) / ctr_values[i-1] 
                        for i in range(1, len(ctr_values))
                        if ctr_values[i-1] != 0]
                        
        return abs(sum(daily_changes) / len(daily_changes)) if daily_changes else 0.0
        
    def _generate_new_creative_recommendations(self,
                                            creative_pool: List[Dict[str, Any]],
                                            performance_history: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Helper method to generate new creative recommendations"""
        recommendations = []
        
        # Analyze top performing elements
        top_elements = self._identify_top_performing_elements(creative_pool, performance_history)
        
        # Generate recommendations based on top elements
        if 'copy_elements' in top_elements:
            recommendations.append({
                'type': 'copy',
                'elements': top_elements['copy_elements'],
                'suggestion': 'Incorporate these high-performing copy elements into new creatives'
            })
            
        if 'visual_elements' in top_elements:
            recommendations.append({
                'type': 'visual',
                'elements': top_elements['visual_elements'],
                'suggestion': 'Use these visual elements as inspiration for new creatives'
            })
            
        return recommendations
        
    def _identify_top_performing_elements(self,
                                        creative_pool: List[Dict[str, Any]],
                                        performance_history: Dict[str, Any]) -> Dict[str, List[str]]:
        """Helper method to identify top performing creative elements"""
        elements = {
            'copy_elements': [],
            'visual_elements': []
        }
        
        # Sort creatives by performance
        sorted_creatives = sorted(
            creative_pool,
            key=lambda x: performance_history.get(x['id'], {}).get('ctr', 0),
            reverse=True
        )
        
        # Extract elements from top performers
        top_performers = sorted_creatives[:3]
        for creative in top_performers:
            if 'ad_copy' in creative:
                elements['copy_elements'].extend(creative['ad_copy'].get('key_elements', []))
            if 'visual_elements' in creative:
                elements['visual_elements'].extend(creative['visual_elements'].get('key_elements', []))
                
        # Remove duplicates
        elements['copy_elements'] = list(set(elements['copy_elements']))
        elements['visual_elements'] = list(set(elements['visual_elements']))
        
        return elements
        
    def _generate_copy_variant(self, copy: str) -> str:
        """Helper method to generate copy variant"""
        # Simple implementation: just append "New" to the copy
        return copy + " New"
        
    def _generate_visual_variant(self, visual_elements: Dict[str, Any]) -> str:
        """Helper method to generate visual variant"""
        # Simple implementation: just change the image layout
        return "New Layout"
