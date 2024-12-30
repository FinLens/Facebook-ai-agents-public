# Facebook Ads Multi-Agent System

A sophisticated multi-agent system for managing and optimizing Facebook advertising campaigns using CrewAI. The system employs multiple specialized agents working in concert to monitor, analyze, and optimize campaign performance.

## Features

### 1. Agent System
- **Campaign Strategy Agent**: Develops and refines campaign structures and targeting strategies
- **Optimization Agent**: Continuously monitors and optimizes campaign performance
- **Reporting Agent**: Generates comprehensive performance reports
- **Creative Management Agent**: Manages ad creative performance and prevents creative fatigue

### 2. Slack Integration
Available commands:
- `/campaign-report [campaign_id] [time_window]`: Generate campaign performance report
- `/optimize [campaign_id]`: Trigger campaign optimization
- `/strategy [campaign_id]`: Get campaign strategy recommendations
- `/kickoff-crew [config]`: Initialize the full agent crew with configuration

### 3. Automated Reporting
- Daily performance reports (9:00 AM ET)
- Weekly optimization reports (Monday 10:00 AM ET)
- Monthly strategy reviews (1st of month 11:00 AM ET)
- Real-time performance alerts

### 4. Optimization Features
- Budget allocation optimization
- Bid strategy adjustments
- Audience targeting refinement
- Placement optimization
- Creative performance monitoring
- A/B testing management

## Setup

### Prerequisites
- Python 3.8+
- Facebook Business API access
- Slack workspace with bot permissions
- OpenAI API key (for CrewAI)

### Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

### Environment Variables
```bash
# Facebook API Credentials
FB_APP_ID=your_app_id
FB_APP_SECRET=your_app_secret
FB_ACCESS_TOKEN=your_access_token
FB_AD_ACCOUNT_ID=your_account_id

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
SLACK_DEFAULT_CHANNEL=#facebook-ads-reports

# Campaign Configuration
FB_CAMPAIGN_IDS=123,456,789  # Comma-separated campaign IDs

# Performance Thresholds
MIN_ROAS=2.0
MAX_CPA=50.0
CREATIVE_FATIGUE_THRESHOLD=0.15
```

## System Architecture

### Agents
1. **BaseAgent**
   - Common functionality for all agents
   - Error handling and utility methods
   - CrewAI integration

2. **CampaignStrategyAgent**
   - Campaign structure optimization
   - Audience targeting strategy
   - Budget allocation recommendations

3. **OptimizationAgent**
   - Real-time performance monitoring
   - Automated optimization actions
   - Placement and bid optimization
   - Audience refinement

4. **ReportingAgent**
   - Performance report generation
   - Custom report scheduling
   - Alert monitoring and notification

5. **CreativeManagementAgent**
   - Creative performance analysis
   - A/B test management
   - Creative fatigue detection

### Services
1. **FacebookService**
   - Facebook Ads API integration
   - Data fetching and updating
   - Campaign management operations

2. **SlackService**
   - Message formatting and sending
   - Command handling
   - Report distribution

3. **SchedulerService**
   - Automated task scheduling
   - Report timing management
   - Periodic optimization runs

## Usage

### Basic Usage
1. Start the system:
```bash
python main.py
```

2. Use Slack commands to interact with the system:
```
/campaign-report 123456789 7d  # Get 7-day report for campaign
/optimize 123456789           # Optimize campaign
/strategy 123456789          # Get strategy recommendations
```

### Advanced Features
1. **Custom Report Scheduling**
   - Modify `scheduler_service.py` to adjust report timing
   - Add new report types in `reporting_agent.py`

2. **Optimization Rules**
   - Adjust thresholds in `.env` file
   - Modify optimization logic in `optimization_agent.py`

3. **Strategy Customization**
   - Update targeting rules in `campaign_strategy_agent.py`
   - Modify budget allocation strategies

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
MIT License

## Support
For support, please open an issue in the repository or contact the development team.
