from apscheduler.schedulers.background import BackgroundScheduler
from backend.database import SessionLocal
from backend.models import Campaign
from backend.queue_worker import run_campaign


def resume_paused_campaigns():

    db = SessionLocal()

    campaigns = db.query(Campaign).filter(Campaign.status == "paused").all()

    for c in campaigns:

        print(f"Resuming campaign {c.id}")

        run_campaign(
            c.id,
            c.sender_email,
            c.app_password,
            c.subject,
            c.body
        )

    db.close()


scheduler = BackgroundScheduler()

scheduler.add_job(
    resume_paused_campaigns,
    "cron",
    hour=9,
    minute=0
)

scheduler.start()