from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from typing import Dict, Any, List
import json

class SlackService:
    def __init__(self):
        """Initialize Slack client with bot token from environment variables"""
        self.client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
        self.default_channel = os.getenv('SLACK_DEFAULT_CHANNEL', '#facebook-ads-reports')
        
    def send_message(self, text: str, channel: str = None, blocks: List[Dict] = None) -> bool:
        """Send a message to Slack channel"""
        try:
            self.client.chat_postMessage(
                channel=channel or self.default_channel,
                text=text,
                blocks=blocks
            )
            return True
        except SlackApiError as e:
            print(f"Error sending message to Slack: {e.response['error']}")
            return False
            
    def send_report(self, report_data: Dict[str, Any], report_type: str, channel: str = None) -> bool:
        """Format and send a report to Slack"""
        try:
            blocks = self._format_report_blocks(report_data, report_type)
            return self.send_message(
                text=f"New {report_type} Report",
                channel=channel or self.default_channel,
                blocks=blocks
            )
        except Exception as e:
            print(f"Error formatting and sending report: {str(e)}")
            return False
            
    def _format_report_blocks(self, report_data: Dict[str, Any], report_type: str) -> List[Dict]:
        """Format report data into Slack blocks"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📊 {report_type} Report"
                }
            },
            {
                "type": "divider"
            }
        ]
        
        if report_type == "Campaign Performance":
            blocks.extend(self._format_campaign_performance(report_data))
        elif report_type == "Optimization Recommendations":
            blocks.extend(self._format_optimization_recommendations(report_data))
        elif report_type == "Campaign Strategy":
            blocks.extend(self._format_campaign_strategy(report_data))
        
        return blocks
        
    def _format_campaign_performance(self, data: Dict[str, Any]) -> List[Dict]:
        """Format campaign performance data into Slack blocks"""
        blocks = []
        
        # Add overall metrics section
        if 'overall_metrics' in data:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Overall Performance Metrics:*"
                }
            })
            
            metrics_text = "\n".join([
                f"• {metric}: {value:,.2f}"
                for metric, value in data['overall_metrics'].items()
            ])
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": metrics_text
                }
            })
        
        # Add campaign-specific metrics
        if 'campaign_metrics' in data:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Campaign-Specific Metrics:*"
                }
            })
            
            for campaign_id, metrics in data['campaign_metrics'].items():
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Campaign {campaign_id}:*\n" + "\n".join([
                            f"• {metric}: {value:,.2f}"
                            for metric, value in metrics.items()
                        ])
                    }
                })
        
        return blocks
        
    def _format_optimization_recommendations(self, data: Dict[str, Any]) -> List[Dict]:
        """Format optimization recommendations into Slack blocks"""
        blocks = []
        
        if 'recommendations' in data:
            for rec in data['recommendations']:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{rec.get('type', 'Recommendation')}*\n{rec.get('description', '')}"
                    }
                })
                
                if 'actions' in rec:
                    blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Suggested Actions:*\n" + "\n".join([
                                f"• {action}" for action in rec['actions']
                            ])
                        }
                    })
                    
                blocks.append({"type": "divider"})
        
        return blocks
        
    def _format_campaign_strategy(self, data: Dict[str, Any]) -> List[Dict]:
        """Format campaign strategy recommendations into Slack blocks"""
        blocks = []
        
        if 'audience_insights' in data:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Audience Insights:*\n" + json.dumps(data['audience_insights'], indent=2)
                }
            })
            
        if 'targeting_recommendations' in data:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Targeting Recommendations:*"
                }
            })
            
            targeting = data['targeting_recommendations']
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*Suggested Interests:*\n" + 
                        "\n".join([f"• {interest}" for interest in targeting.get('suggested_interests', [])])
                    )
                }
            })
            
            if 'age_range_adjustment' in targeting:
                age_range = targeting['age_range_adjustment']
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Optimized Age Range:* {age_range.get('age_min')} - {age_range.get('age_max')}"
                    }
                })
                
            if 'placement_recommendations' in targeting:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"*Recommended Placements:*\n" + 
                            "\n".join([f"• {placement}" for placement in targeting['placement_recommendations']])
                        )
                    }
                })
        
        return blocks
