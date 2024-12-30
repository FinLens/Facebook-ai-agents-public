from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from typing import Dict, Any, List
import json
from datetime import datetime, timedelta
import re

class SlackBot:
    def __init__(self, reporting_agent, optimization_agent, campaign_strategy_agent, fb_crew):
        """Initialize Slack bot with agent instances"""
        self.app = App(token=os.getenv("SLACK_BOT_TOKEN"))
        self.reporting_agent = reporting_agent
        self.optimization_agent = optimization_agent
        self.campaign_strategy_agent = campaign_strategy_agent
        self.fb_crew = fb_crew
        
        # Register command handlers
        self._register_commands()
        
    def start(self):
        """Start the Slack bot"""
        handler = SocketModeHandler(
            app=self.app,
            app_token=os.getenv("SLACK_APP_TOKEN")
        )
        handler.start()
        
    def _register_commands(self):
        """Register command handlers"""
        
        @self.app.command("/campaign-report")
        def handle_campaign_report(ack, command, respond):
            ack()
            try:
                # Parse command arguments
                args = self._parse_command_args(command['text'])
                campaign_id = args.get('campaign_id')
                days = int(args.get('days', '30'))
                
                # Generate report
                start_date = datetime.now() - timedelta(days=days)
                report = self.reporting_agent.generate_campaign_report(
                    campaign_id=campaign_id,
                    start_date=start_date
                )
                
                # Send response
                respond(
                    blocks=self._format_campaign_report(report),
                    text="Campaign Performance Report"
                )
                
            except Exception as e:
                respond(f"Error generating report: {str(e)}")
                
        @self.app.command("/optimize-campaign")
        def handle_optimization(ack, command, respond):
            ack()
            try:
                # Parse command arguments
                args = self._parse_command_args(command['text'])
                campaign_id = args.get('campaign_id')
                
                # Get optimization recommendations
                recommendations = self.optimization_agent.generate_recommendations(
                    campaign_id=campaign_id
                )
                
                # Send response
                respond(
                    blocks=self._format_optimization_recommendations(recommendations),
                    text="Campaign Optimization Recommendations"
                )
                
            except Exception as e:
                respond(f"Error generating optimization recommendations: {str(e)}")
                
        @self.app.command("/campaign-strategy")
        def handle_strategy(ack, command, respond):
            ack()
            try:
                # Parse command arguments
                args = self._parse_command_args(command['text'])
                target_audience = json.loads(args.get('target_audience', '{}'))
                business_objective = args.get('objective', 'CONVERSIONS')
                
                # Generate strategy recommendations
                strategy = self.campaign_strategy_agent.generate_campaign_strategy(
                    target_audience=target_audience,
                    business_objective=business_objective
                )
                
                # Send response
                respond(
                    blocks=self._format_strategy_recommendations(strategy),
                    text="Campaign Strategy Recommendations"
                )
                
            except Exception as e:
                respond(f"Error generating strategy recommendations: {str(e)}")
                
        @self.app.command("/kickoff-crew")
        def handle_crew_kickoff(ack, command, respond):
            ack()
            try:
                # Parse command arguments
                args = self._parse_command_args(command['text'])
                
                # Build campaign configuration
                campaign_config = {
                    "objective": args.get('objective', 'CONVERSIONS'),
                    "budget": float(args.get('budget', '1000.0')),
                    "target_audience": json.loads(args.get('target_audience', '{}')),
                    "creative_requirements": json.loads(args.get('creative_requirements', '{}')),
                    "optimization_goals": args.get('optimization_goals', 'ROAS,CPA').split(',')
                }
                
                # Send initial response
                respond("🚀 Starting Facebook Ads Crew execution...")
                
                # Run the crew
                result = self.fb_crew.run_crew(campaign_config)
                
                # Send the results
                blocks = [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "🎯 Facebook Ads Crew Results"
                        }
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Campaign Configuration:*\n" + json.dumps(campaign_config, indent=2)
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Execution Results:*\n" + json.dumps(result, indent=2)
                        }
                    }
                ]
                
                respond(blocks=blocks, text="Facebook Ads Crew Execution Results")
                
            except Exception as e:
                respond(f"Error executing crew: {str(e)}")
                
    def _parse_command_args(self, command_text: str) -> Dict[str, str]:
        """Parse command arguments from text"""
        args = {}
        
        # Match key=value pairs, handling quoted values
        pattern = r'(\w+)=(?:"([^"]+)"|([^\s]+))'
        matches = re.finditer(pattern, command_text)
        
        for match in matches:
            key = match.group(1)
            # Group 2 is quoted value, group 3 is unquoted value
            value = match.group(2) if match.group(2) else match.group(3)
            args[key] = value
            
        return args
        
    def _format_campaign_report(self, report: Dict[str, Any]) -> List[Dict]:
        """Format campaign report for Slack message"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📊 Campaign Performance Report"
                }
            },
            {"type": "divider"}
        ]
        
        # Add metrics
        if 'metrics' in report:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Key Metrics:*\n" + "\n".join([
                        f"• {metric}: {value:,.2f}"
                        for metric, value in report['metrics'].items()
                    ])
                }
            })
            
        return blocks
        
    def _format_optimization_recommendations(self, recommendations: Dict[str, Any]) -> List[Dict]:
        """Format optimization recommendations for Slack message"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🎯 Optimization Recommendations"
                }
            },
            {"type": "divider"}
        ]
        
        if 'recommendations' in recommendations:
            for rec in recommendations['recommendations']:
                blocks.extend([
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{rec['type']}*\n{rec['description']}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Actions:*\n" + "\n".join([
                                f"• {action}" for action in rec['actions']
                            ])
                        }
                    },
                    {"type": "divider"}
                ])
                
        return blocks
        
    def _format_strategy_recommendations(self, strategy: Dict[str, Any]) -> List[Dict]:
        """Format strategy recommendations for Slack message"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📈 Campaign Strategy Recommendations"
                }
            },
            {"type": "divider"}
        ]
        
        if 'targeting_recommendations' in strategy:
            targeting = strategy['targeting_recommendations']
            blocks.extend([
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Targeting Recommendations:*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Suggested Interests:*\n" + "\n".join([
                            f"• {interest}"
                            for interest in targeting.get('suggested_interests', [])
                        ])
                    }
                }
            ])
            
            if 'age_range_adjustment' in targeting:
                age_range = targeting['age_range_adjustment']
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Age Range:* {age_range['age_min']} - {age_range['age_max']}"
                    }
                })
                
        return blocks
