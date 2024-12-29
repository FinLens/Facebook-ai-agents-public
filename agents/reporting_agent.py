from typing import Dict, Any, List
from .base_agent import BaseAgent
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class ReportingAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agent = self.create_crew_agent(
            name="Performance Reporter",
            role="Facebook Ads Reporting Specialist",
            goal="Generate comprehensive performance reports and insights",
            backstory="Data analysis expert specialized in creating actionable insights "
                     "from Facebook advertising data and communicating results effectively"
        )
        
    def generate_daily_report(self,
                            campaign_ids: List[str],
                            date: datetime = None) -> Dict[str, Any]:
        """
        Generate daily performance report
        """
        try:
            # Use yesterday if date not provided
            report_date = date or datetime.now() - timedelta(days=1)
            
            report = {
                'date': report_date.strftime('%Y-%m-%d'),
                'campaigns': {},
                'overall_metrics': {},
                'significant_changes': [],
                'recommendations': []
            }
            
            # Fetch campaign data
            all_campaign_data = {}
            for campaign_id in campaign_ids:
                campaign_data = self._fetch_campaign_data(campaign_id, report_date)
                all_campaign_data[campaign_id] = campaign_data
                report['campaigns'][campaign_id] = self._calculate_campaign_metrics(campaign_data)
            
            # Calculate overall metrics
            report['overall_metrics'] = self._calculate_overall_metrics(all_campaign_data)
            
            # Identify significant changes
            report['significant_changes'] = self._identify_significant_changes(
                all_campaign_data,
                lookback_days=1
            )
            
            # Generate recommendations
            report['recommendations'] = self._generate_daily_recommendations(
                report['campaigns'],
                report['significant_changes']
            )
            
            return report
            
        except Exception as e:
            self.handle_error(e, {'method': 'generate_daily_report'})
            return {}
            
    def generate_weekly_summary(self,
                              campaign_ids: List[str],
                              end_date: datetime = None) -> Dict[str, Any]:
        """
        Generate weekly optimization summary
        """
        try:
            # Use last Sunday if end_date not provided
            end_date = end_date or datetime.now() - timedelta(days=datetime.now().weekday() + 1)
            start_date = end_date - timedelta(days=7)
            
            summary = {
                'period': {
                    'start': start_date.strftime('%Y-%m-%d'),
                    'end': end_date.strftime('%Y-%m-%d')
                },
                'campaign_performance': {},
                'weekly_trends': {},
                'optimization_actions': [],
                'recommendations': []
            }
            
            # Fetch weekly data
            weekly_data = {}
            for campaign_id in campaign_ids:
                campaign_data = self._fetch_campaign_data(campaign_id, start_date, end_date)
                weekly_data[campaign_id] = campaign_data
                summary['campaign_performance'][campaign_id] = self._calculate_weekly_metrics(campaign_data)
            
            # Calculate weekly trends
            summary['weekly_trends'] = self._calculate_weekly_trends(weekly_data)
            
            # Get optimization actions taken
            summary['optimization_actions'] = self._get_optimization_actions(
                campaign_ids,
                start_date,
                end_date
            )
            
            # Generate recommendations
            summary['recommendations'] = self._generate_weekly_recommendations(
                summary['campaign_performance'],
                summary['weekly_trends'],
                summary['optimization_actions']
            )
            
            return summary
            
        except Exception as e:
            self.handle_error(e, {'method': 'generate_weekly_summary'})
            return {}
            
    def generate_monthly_review(self,
                              account_id: str,
                              month: int,
                              year: int) -> Dict[str, Any]:
        """
        Generate monthly strategic review
        """
        try:
            start_date = datetime(year, month, 1)
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            review = {
                'period': {
                    'month': month,
                    'year': year,
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d')
                },
                'account_performance': {},
                'campaign_performance': {},
                'strategic_insights': [],
                'recommendations': []
            }
            
            # Fetch monthly data
            account_data = self._fetch_account_data(account_id, start_date, end_date)
            review['account_performance'] = self._calculate_monthly_metrics(account_data)
            
            # Get campaign performance
            campaign_ids = self._get_account_campaigns(account_id)
            for campaign_id in campaign_ids:
                campaign_data = self._fetch_campaign_data(campaign_id, start_date, end_date)
                review['campaign_performance'][campaign_id] = self._calculate_monthly_metrics(campaign_data)
            
            # Generate strategic insights
            review['strategic_insights'] = self._generate_strategic_insights(
                review['account_performance'],
                review['campaign_performance']
            )
            
            # Generate recommendations
            review['recommendations'] = self._generate_monthly_recommendations(
                review['account_performance'],
                review['campaign_performance'],
                review['strategic_insights']
            )
            
            return review
            
        except Exception as e:
            self.handle_error(e, {'method': 'generate_monthly_review'})
            return {}
            
    def track_kpis(self,
                   campaign_ids: List[str],
                   kpi_targets: Dict[str, float],
                   time_window: str = "7d") -> Dict[str, Any]:
        """
        Track KPI progress against targets
        """
        try:
            tracking_results = {
                'time_window': time_window,
                'kpi_status': {},
                'alerts': [],
                'recommendations': []
            }
            
            # Calculate current KPIs
            current_kpis = {}
            for campaign_id in campaign_ids:
                campaign_data = self._fetch_campaign_data(
                    campaign_id,
                    datetime.now() - timedelta(days=int(time_window[:-1])),
                    datetime.now()
                )
                current_kpis[campaign_id] = self._calculate_kpis(campaign_data)
            
            # Compare against targets
            for campaign_id, kpis in current_kpis.items():
                tracking_results['kpi_status'][campaign_id] = {}
                for kpi_name, target_value in kpi_targets.items():
                    current_value = kpis.get(kpi_name, 0)
                    status = self._calculate_kpi_status(current_value, target_value)
                    tracking_results['kpi_status'][campaign_id][kpi_name] = {
                        'current_value': current_value,
                        'target_value': target_value,
                        'status': status,
                        'variance': ((current_value - target_value) / target_value) * 100
                    }
            
            # Generate alerts
            tracking_results['alerts'] = self._generate_kpi_alerts(
                tracking_results['kpi_status']
            )
            
            # Generate recommendations
            tracking_results['recommendations'] = self._generate_kpi_recommendations(
                tracking_results['kpi_status']
            )
            
            return tracking_results
            
        except Exception as e:
            self.handle_error(e, {'method': 'track_kpis'})
            return {}
            
    def generate_alerts(self,
                       performance_data: Dict[str, Any],
                       threshold_config: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Generate performance alerts based on thresholds
        """
        try:
            alerts = []
            
            # Check each metric against its threshold
            for metric, current_value in performance_data.items():
                if metric in threshold_config:
                    threshold = threshold_config[metric]
                    if self._should_generate_alert(current_value, threshold):
                        alerts.append({
                            'metric': metric,
                            'current_value': current_value,
                            'threshold': threshold,
                            'severity': self._calculate_alert_severity(current_value, threshold),
                            'timestamp': datetime.now().isoformat()
                        })
            
            return alerts
            
        except Exception as e:
            self.handle_error(e, {'method': 'generate_alerts'})
            return []
            
    def _fetch_campaign_data(self, 
                           campaign_id: str,
                           start_date: datetime,
                           end_date: datetime = None) -> Dict[str, Any]:
        """Helper method to fetch campaign data"""
        # This would typically make API calls to Facebook
        # For now, return dummy data
        return {
            'spend': 1000.0,
            'impressions': 100000,
            'clicks': 2000,
            'conversions': 100,
            'revenue': 5000.0
        }
        
    def _calculate_campaign_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Helper method to calculate campaign metrics"""
        return {
            'ctr': (data.get('clicks', 0) / data.get('impressions', 1)) * 100,
            'cpc': data.get('spend', 0) / max(data.get('clicks', 1), 1),
            'conversion_rate': (data.get('conversions', 0) / max(data.get('clicks', 1), 1)) * 100,
            'cpa': data.get('spend', 0) / max(data.get('conversions', 1), 1),
            'roas': data.get('revenue', 0) / max(data.get('spend', 1), 1)
        }
        
    def _calculate_overall_metrics(self, campaign_data: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        """Helper method to calculate overall metrics"""
        totals = {
            'spend': 0,
            'impressions': 0,
            'clicks': 0,
            'conversions': 0,
            'revenue': 0
        }
        
        # Sum up totals
        for data in campaign_data.values():
            for metric in totals:
                totals[metric] += data.get(metric, 0)
                
        # Calculate aggregate metrics
        return {
            'total_spend': totals['spend'],
            'total_revenue': totals['revenue'],
            'overall_ctr': (totals['clicks'] / max(totals['impressions'], 1)) * 100,
            'overall_conversion_rate': (totals['conversions'] / max(totals['clicks'], 1)) * 100,
            'overall_roas': totals['revenue'] / max(totals['spend'], 1)
        }
        
    def _identify_significant_changes(self,
                                   current_data: Dict[str, Dict[str, Any]],
                                   lookback_days: int) -> List[Dict[str, Any]]:
        """Helper method to identify significant changes"""
        changes = []
        
        # This would typically compare with historical data
        # For now, return a sample change
        changes.append({
            'metric': 'conversion_rate',
            'campaign_id': list(current_data.keys())[0],
            'change_percentage': 15.0,
            'direction': 'increase'
        })
        
        return changes
        
    def _generate_daily_recommendations(self,
                                     campaign_metrics: Dict[str, Dict[str, float]],
                                     changes: List[Dict[str, Any]]) -> List[str]:
        """Helper method to generate daily recommendations"""
        recommendations = []
        
        # Generate recommendations based on metrics and changes
        for campaign_id, metrics in campaign_metrics.items():
            if metrics['ctr'] < 1.0:
                recommendations.append(f"Campaign {campaign_id}: Consider refreshing ad creatives to improve CTR")
            if metrics['roas'] < 2.0:
                recommendations.append(f"Campaign {campaign_id}: Optimize targeting to improve ROAS")
                
        return recommendations
        
    def _calculate_weekly_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Helper method to calculate weekly metrics"""
        return {
            'weekly_spend': data.get('spend', 0),
            'weekly_conversions': data.get('conversions', 0),
            'weekly_revenue': data.get('revenue', 0),
            'weekly_roas': data.get('revenue', 0) / max(data.get('spend', 1), 1)
        }
        
    def _calculate_weekly_trends(self, data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Helper method to calculate weekly trends"""
        trends = {}
        
        # This would typically calculate week-over-week changes
        # For now, return sample trends
        trends['spend_trend'] = 'increasing'
        trends['conversion_trend'] = 'stable'
        trends['roas_trend'] = 'increasing'
        
        return trends
        
    def _get_optimization_actions(self,
                                campaign_ids: List[str],
                                start_date: datetime,
                                end_date: datetime) -> List[Dict[str, Any]]:
        """Helper method to get optimization actions"""
        actions = []
        
        # This would typically fetch from an optimization log
        # For now, return sample actions
        actions.append({
            'campaign_id': campaign_ids[0],
            'action_type': 'bid_adjustment',
            'timestamp': start_date + timedelta(days=2),
            'details': 'Increased bid by 10% due to strong ROAS'
        })
        
        return actions
        
    def _generate_weekly_recommendations(self,
                                      performance: Dict[str, Dict[str, float]],
                                      trends: Dict[str, Any],
                                      actions: List[Dict[str, Any]]) -> List[str]:
        """Helper method to generate weekly recommendations"""
        recommendations = []
        
        # Generate recommendations based on performance and trends
        if trends.get('roas_trend') == 'decreasing':
            recommendations.append("Review and optimize targeting settings across campaigns")
        if trends.get('conversion_trend') == 'decreasing':
            recommendations.append("Analyze and refresh underperforming ad creatives")
            
        return recommendations
        
    def _calculate_monthly_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Helper method to calculate monthly metrics"""
        return {
            'monthly_spend': data.get('spend', 0),
            'monthly_revenue': data.get('revenue', 0),
            'monthly_roas': data.get('revenue', 0) / max(data.get('spend', 1), 1),
            'monthly_conversions': data.get('conversions', 0),
            'average_cpa': data.get('spend', 0) / max(data.get('conversions', 1), 1)
        }
        
    def _generate_strategic_insights(self,
                                  account_metrics: Dict[str, float],
                                  campaign_metrics: Dict[str, Dict[str, float]]) -> List[Dict[str, Any]]:
        """Helper method to generate strategic insights"""
        insights = []
        
        # Analyze account-level performance
        if account_metrics.get('monthly_roas', 0) > 3.0:
            insights.append({
                'type': 'opportunity',
                'description': 'Strong ROAS indicates opportunity for scaling',
                'recommendation': 'Consider increasing budget allocation'
            })
            
        # Analyze campaign-level performance
        for campaign_id, metrics in campaign_metrics.items():
            if metrics.get('monthly_roas', 0) < 1.0:
                insights.append({
                    'type': 'warning',
                    'campaign_id': campaign_id,
                    'description': 'Campaign showing negative ROI',
                    'recommendation': 'Review and optimize or consider pausing'
                })
                
        return insights
        
    def _generate_monthly_recommendations(self,
                                       account_metrics: Dict[str, float],
                                       campaign_metrics: Dict[str, Dict[str, float]],
                                       insights: List[Dict[str, Any]]) -> List[str]:
        """Helper method to generate monthly recommendations"""
        recommendations = []
        
        # Generate high-level strategic recommendations
        if account_metrics.get('monthly_roas', 0) > 2.0:
            recommendations.append("Explore opportunities for scaling successful campaigns")
            
        # Add recommendations based on insights
        for insight in insights:
            if insight['type'] == 'warning':
                recommendations.append(
                    f"Review and optimize campaign {insight['campaign_id']}: {insight['recommendation']}"
                )
                
        return recommendations
        
    def _calculate_kpis(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Helper method to calculate KPIs"""
        return {
            'roas': data.get('revenue', 0) / max(data.get('spend', 1), 1),
            'cpa': data.get('spend', 0) / max(data.get('conversions', 1), 1),
            'conversion_rate': (data.get('conversions', 0) / max(data.get('clicks', 1), 1)) * 100
        }
        
    def _calculate_kpi_status(self, current_value: float, target_value: float) -> str:
        """Helper method to calculate KPI status"""
        variance = ((current_value - target_value) / target_value) * 100
        
        if variance >= 10:
            return 'exceeding'
        elif variance >= -10:
            return 'on_track'
        else:
            return 'below_target'
            
    def _generate_kpi_alerts(self, kpi_status: Dict[str, Dict[str, Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Helper method to generate KPI alerts"""
        alerts = []
        
        for campaign_id, kpis in kpi_status.items():
            for kpi_name, status in kpis.items():
                if status['status'] == 'below_target' and status['variance'] < -20:
                    alerts.append({
                        'campaign_id': campaign_id,
                        'kpi': kpi_name,
                        'severity': 'high',
                        'message': f"KPI significantly below target: {status['variance']:.1f}% variance"
                    })
                    
        return alerts
        
    def _generate_kpi_recommendations(self, kpi_status: Dict[str, Dict[str, Dict[str, Any]]]) -> List[str]:
        """Helper method to generate KPI recommendations"""
        recommendations = []
        
        for campaign_id, kpis in kpi_status.items():
            if kpis.get('roas', {}).get('status') == 'below_target':
                recommendations.append(f"Review and optimize targeting for campaign {campaign_id}")
            if kpis.get('conversion_rate', {}).get('status') == 'below_target':
                recommendations.append(f"Analyze and improve conversion funnel for campaign {campaign_id}")
                
        return recommendations
        
    def _should_generate_alert(self, current_value: float, threshold: float) -> bool:
        """Helper method to determine if alert should be generated"""
        return abs((current_value - threshold) / threshold) > 0.2  # 20% deviation
        
    def _calculate_alert_severity(self, current_value: float, threshold: float) -> str:
        """Helper method to calculate alert severity"""
        deviation = abs((current_value - threshold) / threshold)
        
        if deviation > 0.5:
            return 'high'
        elif deviation > 0.3:
            return 'medium'
        else:
            return 'low'
