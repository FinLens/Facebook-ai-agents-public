from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from typing import Dict, Any, Callable
import pytz

class SchedulerService:
    def __init__(self):
        """Initialize the scheduler service"""
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        
    def schedule_daily_report(self, job_func: Callable, 
                            hour: int = 9, minute: int = 0,
                            timezone: str = 'America/New_York') -> None:
        """Schedule a daily report job"""
        self.scheduler.add_job(
            job_func,
            trigger=CronTrigger(hour=hour, minute=minute, timezone=pytz.timezone(timezone))
        )
        
    def schedule_weekly_report(self, job_func: Callable,
                             day_of_week: str = 'mon',
                             hour: int = 9, minute: int = 0,
                             timezone: str = 'America/New_York') -> None:
        """Schedule a weekly report job"""
        self.scheduler.add_job(
            job_func,
            trigger=CronTrigger(
                day_of_week=day_of_week,
                hour=hour,
                minute=minute,
                timezone=pytz.timezone(timezone)
            )
        )
        
    def schedule_monthly_report(self, job_func: Callable,
                              day: int = 1,
                              hour: int = 9, minute: int = 0,
                              timezone: str = 'America/New_York') -> None:
        """Schedule a monthly report job"""
        self.scheduler.add_job(
            job_func,
            trigger=CronTrigger(
                day=day,
                hour=hour,
                minute=minute,
                timezone=pytz.timezone(timezone)
            )
        )
        
    def schedule_custom(self, job_func: Callable,
                       trigger: str,
                       **trigger_args) -> None:
        """Schedule a job with custom trigger"""
        self.scheduler.add_job(job_func, trigger=trigger, **trigger_args)
        
    def shutdown(self) -> None:
        """Shutdown the scheduler"""
        self.scheduler.shutdown()
