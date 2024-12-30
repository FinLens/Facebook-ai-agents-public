from typing import Dict, Any, List, Optional
from datetime import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
import os

class FacebookService:
    def __init__(self):
        """Initialize Facebook Ads API client"""
        self.api = FacebookAdsApi.init(
            access_token=os.getenv('FB_ACCESS_TOKEN'),
            app_secret=os.getenv('FB_APP_SECRET'),
            app_id=os.getenv('FB_APP_ID')
        )
        self.account = AdAccount(os.getenv('FB_AD_ACCOUNT_ID'))
        
    def get_campaign_data(self,
                         campaign_id: str,
                         start_date: datetime,
                         end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Fetch campaign performance data from Facebook Ads API
        """
        try:
            campaign = Campaign(campaign_id)
            end_date = end_date or datetime.now()
            
            # Define metrics to fetch
            fields = [
                'spend',
                'impressions',
                'clicks',
                'actions',
                'action_values',
                'cost_per_action_type',
                'conversion_values'
            ]
            
            # Define date range parameters
            params = {
                'time_range': {
                    'since': start_date.strftime('%Y-%m-%d'),
                    'until': end_date.strftime('%Y-%m-%d')
                },
                'level': 'campaign'
            }
            
            # Fetch insights
            insights = campaign.get_insights(
                fields=fields,
                params=params
            )
            
            if not insights:
                return {}
                
            # Process insights data
            data = insights[0]
            
            # Calculate conversions and revenue from actions
            conversions = 0
            revenue = 0
            if 'actions' in data:
                for action in data['actions']:
                    if action['action_type'] in ['purchase', 'complete_registration']:
                        conversions += action['value']
                        
            if 'action_values' in data:
                for value in data['action_values']:
                    if value['action_type'] in ['purchase', 'complete_registration']:
                        revenue += value['value']
                        
            return {
                'spend': float(data.get('spend', 0)),
                'impressions': int(data.get('impressions', 0)),
                'clicks': int(data.get('clicks', 0)),
                'conversions': int(conversions),
                'revenue': float(revenue)
            }
            
        except Exception as e:
            print(f"Error fetching campaign data: {str(e)}")
            return {}
            
    def get_account_data(self,
                        start_date: datetime,
                        end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Fetch account-level performance data
        """
        try:
            end_date = end_date or datetime.now()
            
            # Define metrics to fetch
            fields = [
                'spend',
                'impressions',
                'clicks',
                'actions',
                'action_values',
                'cost_per_action_type'
            ]
            
            # Define date range parameters
            params = {
                'time_range': {
                    'since': start_date.strftime('%Y-%m-%d'),
                    'until': end_date.strftime('%Y-%m-%d')
                },
                'level': 'account'
            }
            
            # Fetch insights
            insights = self.account.get_insights(
                fields=fields,
                params=params
            )
            
            if not insights:
                return {}
                
            # Process insights data
            data = insights[0]
            
            # Calculate conversions and revenue from actions
            conversions = 0
            revenue = 0
            if 'actions' in data:
                for action in data['actions']:
                    if action['action_type'] in ['purchase', 'complete_registration']:
                        conversions += action['value']
                        
            if 'action_values' in data:
                for value in data['action_values']:
                    if value['action_type'] in ['purchase', 'complete_registration']:
                        revenue += value['value']
                        
            return {
                'spend': float(data.get('spend', 0)),
                'impressions': int(data.get('impressions', 0)),
                'clicks': int(data.get('clicks', 0)),
                'conversions': int(conversions),
                'revenue': float(revenue)
            }
            
        except Exception as e:
            print(f"Error fetching account data: {str(e)}")
            return {}
            
    def get_account_campaigns(self) -> List[str]:
        """
        Get all active campaign IDs for the account
        """
        try:
            campaigns = self.account.get_campaigns(
                fields=['id', 'name'],
                params={'effective_status': ['ACTIVE']}
            )
            return [campaign['id'] for campaign in campaigns]
            
        except Exception as e:
            print(f"Error fetching campaign list: {str(e)}")
            return []
            
    def get_campaign_targeting(self, campaign_id: str) -> Dict[str, Any]:
        """
        Get targeting settings for a campaign
        """
        try:
            campaign = Campaign(campaign_id)
            adsets = campaign.get_ad_sets(
                fields=['targeting']
            )
            
            if not adsets:
                return {}
                
            # Return targeting from first adset
            return adsets[0].get('targeting', {})
            
        except Exception as e:
            print(f"Error fetching campaign targeting: {str(e)}")
            return {}
            
    def get_campaign_creatives(self, campaign_id: str) -> List[Dict[str, Any]]:
        """
        Get creative information for a campaign
        """
        try:
            campaign = Campaign(campaign_id)
            ads = campaign.get_ads(
                fields=['creative', 'effective_status']
            )
            
            creatives = []
            for ad in ads:
                if ad.get('effective_status') == 'ACTIVE':
                    creative = ad.get('creative', {})
                    if creative:
                        creatives.append(creative)
                        
            return creatives
            
        except Exception as e:
            print(f"Error fetching campaign creatives: {str(e)}")
            return []
            
    def update_campaign_budget(self,
                             campaign_id: str,
                             budget_amount: float) -> bool:
        """
        Update campaign budget
        """
        try:
            campaign = Campaign(campaign_id)
            campaign.api_update(
                fields=[],
                params={'daily_budget': int(budget_amount * 100)}  # Convert to cents
            )
            return True
            
        except Exception as e:
            print(f"Error updating campaign budget: {str(e)}")
            return False
            
    def update_campaign_status(self,
                             campaign_id: str,
                             status: str) -> bool:
        """
        Update campaign status (ACTIVE, PAUSED)
        """
        try:
            campaign = Campaign(campaign_id)
            campaign.api_update(
                fields=[],
                params={'status': status}
            )
            return True
            
        except Exception as e:
            print(f"Error updating campaign status: {str(e)}")
            return False
