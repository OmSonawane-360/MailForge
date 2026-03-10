import time
from datetime import datetime

from backend.database import SessionLocal
from backend.models import Campaign, Email
from backend.email_sender import send_email


DAILY_LIMIT = 300


def run_campaign(campaign_id, sender_email, app_password, subject, body):

    db = SessionLocal()

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    campaign.status = "running"
    db.commit()

    emails = db.query(Email).filter(
        Email.campaign_id == campaign_id,
        Email.status == "pending"
    ).all()

    emails_sent_today = 0
    today = datetime.now().date()

    for email in emails:

        # stop if campaign paused manually
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

        if campaign.status == "paused":
            print("Campaign paused by user")
            db.close()
            return

        # check daily limit
        if emails_sent_today >= DAILY_LIMIT:

            print("Daily limit reached (300). Pausing campaign until tomorrow.")

            campaign.status = "paused"
            db.commit()

            db.close()
            return

        # -------- personalization --------
        personalized_body = body

        if email.name:
            personalized_body = personalized_body.replace("{name}", email.name)

        if email.company:
            personalized_body = personalized_body.replace("{company}", email.company)

        if email.title:
            personalized_body = personalized_body.replace("{title}", email.title)
        # ---------------------------------

        success = send_email(
            sender_email,
            app_password,
            email.email,
            subject,
            personalized_body
        )

        if success:
            email.status = "sent"
            emails_sent_today += 1
        else:
            email.status = "failed"

        db.commit()

        # wait 60 seconds between emails
        time.sleep(60)

    campaign.status = "completed"
    db.commit()

    print("Congratulations! All emails have been sent.")

    db.close()