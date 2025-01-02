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

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

Required packages:
- facebook-business
- python-dotenv
- slack-sdk
- openai
- crewai

3. Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

### Setup Instructions

### Facebook App Setup
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click "My Apps" and then "Create App"
3. Select "Business" as your app type
4. Fill in your app name and contact email
5. Once created, navigate to the app dashboard
6. Under "Add Products", find and set up "Facebook Login" and "Marketing API"
7. In Settings > Basic:
   - Copy your App ID (`FB_APP_ID`)
   - Copy your App Secret (`FB_APP_SECRET`)
8. To get your Access Token:
   - Go to [Facebook Business Settings](https://business.facebook.com/settings)
   - Navigate to "System Users"
   - Create a new system user or select existing
   - Assign necessary permissions:
     - ads_management
     - ads_read
     - read_insights
   - Generate a token and copy it (`FB_ACCESS_TOKEN`)

### Slack Bot Setup
1. Go to [Slack API](https://api.slack.com/apps)
2. Click "Create New App"
3. Choose "From scratch" and fill in:
   - App Name: "Facebook Ads AI"
   - Pick your workspace
4. Under "Basic Information":
   - Copy "Signing Secret" for verification
   - Note your Client ID and Client Secret
5. Under "OAuth & Permissions":
   - Add the following Bot Token Scopes:
     - `chat:write`
     - `commands`
     - `files:write`
     - `channels:read`
     - `channels:join`
   - Install app to workspace
   - Copy the Bot User OAuth Token (`SLACK_BOT_TOKEN`)
6. Under "Socket Mode":
   - Enable Socket Mode
   - Generate and copy App-Level Token (`SLACK_APP_TOKEN`)
7. Under "Slash Commands", create the following commands:
   ```
   /campaign-report
   /optimize
   /strategy
   /kickoff-crew
   ```
   - For each command:
     - Set Request URL to your app's endpoint
     - Add description
     - Set usage hint (e.g., "[campaign_id] [time_window]")

8. Under "App Home":
   - Enable messages tab
   - Allow users to send DMs to your app

### Slack Bot Configuration

To configure the Slack bot for reporting and notifications:

1. **Create a Slack App**:
   - Go to [Slack API Apps](https://api.slack.com/apps)
   - Click "Create New App"
   - Choose "From scratch"
   - Name your app (e.g., "Facebook Ads AI Bot")
   - Select your workspace

2. **Configure Bot Permissions**:
   - In your app settings, go to "OAuth & Permissions"
   - Under "Scopes" > "Bot Token Scopes", add these permissions:
     - `chat:write` (Send messages as your app)
     - `chat:write.public` (Send messages to channels)
     - `channels:read` (View channels)
     - `groups:read` (View private channels)

3. **Install the App**:
   - Go to "Install App" in the sidebar
   - Click "Install to Workspace"
   - Authorize the app
   - Copy the "Bot User OAuth Token" (starts with `xoxb-`)

4. **Enable Socket Mode**:
   - Go to "Socket Mode" in the sidebar
   - Enable Socket Mode
   - Generate an App-Level Token
   - Copy the App-Level Token (starts with `xapp-`)

5. **Update Environment Variables**:
   ```bash
   # In your .env file
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_APP_TOKEN=xapp-your-app-token
   SLACK_DEFAULT_CHANNEL=#your-channel-name
   ```

6. **Add Bot to Channels**:
   - In Slack, go to the channel where you want to receive reports
   - Type `/invite @YourBotName`

7. **Test the Integration**:
   ```python
   python -c "from services.slack_service import SlackService; slack = SlackService(); slack.send_message('Test message')"
   ```

#### Troubleshooting Slack Integration

- **Error: not_authed**
  - Verify your bot token is correct
  - Check if the bot has been added to the channel
  - Try reinstalling the app to get new tokens

- **Error: channel_not_found**
  - Make sure the channel exists
  - Verify the channel name starts with `#`
  - Ensure the bot is a member of the channel

- **Error: missing_scope**
  - Go to your app's OAuth settings
  - Add any missing permissions
  - Reinstall the app to update permissions

### Environment Variables
After setting up both apps, update your `.env` file with the following credentials:

1. **Facebook API Credentials**:
   ```bash
   # Your Facebook App credentials from developers.facebook.com
   FB_APP_ID=your_app_id
   FB_APP_SECRET=your_app_secret
   
   # Generate a long-lived access token from Business Settings > System Users
   FB_ACCESS_TOKEN=your_access_token
   
   # Your Ad Account ID from Business Manager (format: act_XXXXXXXXXX)
   FB_AD_ACCOUNT_ID=act_your_ad_account_id
   
   # Comma-separated list of campaign IDs to monitor
   FB_CAMPAIGN_IDS=123456789,987654321
   ```

   To find your Ad Account ID:
   1. Go to [Business Manager](https://business.facebook.com)
   2. Click "Business Settings" > "Accounts" > "Ad Accounts"
   3. Select your ad account
   4. The ID will be in the format "act_XXXXXXXXXX"

2. **OpenAI API Key** (for CrewAI):
   ```bash
   # Get this from platform.openai.com/api-keys
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Slack Configuration**:
   ```bash
   # Get these from api.slack.com/apps > Your App > OAuth & Permissions
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_APP_TOKEN=xapp-your-app-token
   
   # Channel where the bot will post reports (include the #)
   SLACK_DEFAULT_CHANNEL=#your-channel-name
   ```

4. **Performance Thresholds**:
   ```bash
   # Minimum Return on Ad Spend target
   MIN_ROAS=2.0
   
   # Maximum Cost Per Acquisition target
   MAX_CPA=50.0
   
   # Threshold for detecting creative fatigue (0.0 to 1.0)
   CREATIVE_FATIGUE_THRESHOLD=0.15
   ```

5. **Reporting Configuration**:
   ```bash
   # Email for receiving alerts
   ALERT_EMAIL=your@email.com
   
   # Time for daily reports (24-hour format)
   DAILY_REPORT_TIME=08:00
   
   # Day of week for weekly reports (0=Sunday, 1=Monday, etc.)
   WEEKLY_REPORT_DAY=1
   ```

### Docker Deployment
To run the Facebook AI Agent System using Docker:

1. Build and start the container:
```bash
docker-compose up --build -d
```

2. View logs:
```bash
docker-compose logs -f
```

3. Stop the container:
```bash
docker-compose down
```

For manual Docker deployment without docker-compose:
```bash
# Build the image
docker build -t facebook-ai-agent .

# Run the container
docker run -d \
  --name facebook-ai-agent \
  --env-file .env \
  -v $(pwd):/app \
  -p 8000:8000 \
  facebook-ai-agent
```

### Testing Environment Variables

After setting up your environment variables, you can verify them with these commands:

1. Test environment variables are loaded:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('FB_ACCESS_TOKEN:', bool(os.getenv('FB_ACCESS_TOKEN')), '\nFB_APP_SECRET:', bool(os.getenv('FB_APP_SECRET')), '\nFB_APP_ID:', bool(os.getenv('FB_APP_ID')), '\nFB_AD_ACCOUNT_ID:', os.getenv('FB_AD_ACCOUNT_ID'))"
```

2. Test Facebook API connection:
```bash
python -c "from services.facebook_service import FacebookService; from datetime import datetime; fb = FacebookService(); print(fb.get_campaign_data('YOUR_CAMPAIGN_ID', start_date=datetime(2024, 1, 1)))"
```

Example successful output:
```python
{
    'spend': 80725.51,          # Total amount spent
    'impressions': 3985684,     # Number of times ads were shown
    'clicks': 62353,            # Number of clicks received
    'conversions': 6015,        # Number of conversions (purchases/registrations)
    'revenue': 72549.65         # Total revenue from conversions
}
```

3. Test Slack connection:
```bash
python -c "from services.slack_service import SlackService; slack = SlackService(); slack.send_message('Test message')"
```

If you encounter any errors:
- For Facebook API errors:
  - Verify your access token is valid and has the necessary permissions
  - Check that your Ad Account ID is in the correct format (act_XXXXXXXXXX)
  - Ensure the campaign ID exists and is accessible
  - Make sure all environment variables are loaded (use test command #1)
  
- For Slack errors:
  - Verify both bot and app tokens are correct
  - Check that the bot is invited to the specified channel
  - Ensure the channel name includes the # prefix

### Slack Channel Setup
1. Create a new channel in your Slack workspace (e.g., #fb-ai-reporting)
2. Invite your bot to the channel:
   ```
   /invite @Facebook Ads AI
   ```
3. Update `SLACK_DEFAULT_CHANNEL` in your `.env` file with the channel name

### Testing the Setup
1. Test Facebook API connection:
```bash
python -c "from services.facebook_service import FacebookService; from datetime import datetime; fb = FacebookService(); print(fb.get_campaign_data('YOUR_CAMPAIGN_ID', start_date=datetime(2024, 1, 1)))"
```

2. Test Slack connection:
```bash
python -c "from services.slack_service import SlackService; slack = SlackService(); slack.send_message('Test message')"
```

3. Test Report Generation:
```bash
python -c "from agents.reporting_agent import ReportingAgent; from datetime import datetime; agent = ReportingAgent(); print(agent.generate_campaign_report('YOUR_CAMPAIGN_ID', start_date=datetime(2024, 1, 1)))"
```

### Test Facebook Crew
To test the Facebook Crew with a sample campaign configuration:
```python
python -c "from main import FacebookAdsCrew; from crewai import Task; crew = FacebookAdsCrew(); config = {'target_audience': 'US-based professionals 25-45', 'objective': 'conversions', 'creative_requirements': 'Video ads highlighting product benefits', 'optimization_goals': ['ROAS', 'CPA'], 'budget': 5000}; tasks = [Task(description=f'Analyze target audience and develop campaign strategy for {config[\"target_audience\"]}', agent=crew.campaign_strategy_agent.agent, expected_output='Detailed campaign strategy with audience insights and targeting recommendations'), Task(description=f'Design creative assets: {config[\"creative_requirements\"]}', agent=crew.creative_management_agent.agent, expected_output='Creative asset specifications and A/B testing plan'), Task(description=f'Optimize for {config[\"optimization_goals\"]} with budget ${config[\"budget\"]}', agent=crew.optimization_agent.agent, expected_output='Campaign optimization strategy with budget allocation plan'), Task(description='Generate performance projections', agent=crew.reporting_agent.agent, expected_output='Performance projections and KPI targets')]; print(crew.run_crew({'tasks': tasks}))"
```

### Troubleshooting
- **Facebook API Issues**:
  - Verify your app has the necessary permissions
  - Check if your access token is valid and has required scopes
  - Ensure your ad account ID is correct
  
- **Slack API Issues**:
  - Verify bot is invited to the channel
  - Check if all required scopes are granted
  - Ensure socket mode is enabled
  - Verify slash commands are properly configured

- **General Issues**:
  - Check your `.env` file for correct values
  - Verify network connectivity
  - Check application logs for errors

For additional help:
- [Facebook Marketing API Documentation](https://developers.facebook.com/docs/marketing-apis/)
- [Slack API Documentation](https://api.slack.com/docs)

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
