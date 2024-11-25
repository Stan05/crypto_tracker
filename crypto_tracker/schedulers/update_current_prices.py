from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from ..services.service_manager import ServiceManager

# Define your job function
def job():
    print(f"Updating current prices...")
    service_manager = ServiceManager()
    service_manager.price_service.fetch_and_store_current_prices()
    print(f"Job executed at {datetime.now()}")

# Initialize the scheduler
scheduler = BlockingScheduler()

# Schedule the job to run every 10 minutes
scheduler.add_job(job, trigger=CronTrigger(minute='*/1'))

try:
    # Start the scheduler
    print("Scheduler started...")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    # Shut down the scheduler gracefully on exit
    scheduler.shutdown()
    print("Scheduler shut down.")
