import time
import threading
import shutil
import os  


from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware

os.makedirs("uploads", exist_ok=True)   
from sqlalchemy.orm import Session


from backend.scheduler import scheduler
from backend.queue_worker import run_campaign
from backend.pdf_parser import extract_contacts_from_pdf
from backend.database import engine, get_db
from backend.models import Base, Campaign, Email
from backend.email_sender import send_email


# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MailForge API")

# ✅ CORS FIX (FINAL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for now
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to MailForge 🚀"}


# Upload PDF and preview contacts
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    contacts = extract_contacts_from_pdf(file_path)

    return {
        "contacts_found": len(contacts),
        "sample": contacts[:5]
    }


# Create campaign
@app.post("/create-campaign")
async def create_campaign(
    name: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    contacts = extract_contacts_from_pdf(file_path)

    campaign = Campaign(
        name=name,
        total_emails=len(contacts)
    )

    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    for contact in contacts:
        email_record = Email(
            campaign_id=campaign.id,
            email=contact["email"],
            name=contact["name"],
            company=contact["company"],
            title=contact["title"]
        )
        db.add(email_record)

    db.commit()

    return {
        "campaign_id": campaign.id,
        "campaign_name": name,
        "total_contacts": len(contacts)
    }


# Send campaign emails sequentially
@app.post("/send-campaign/{campaign_id}")
def send_campaign(
    campaign_id: int,
    sender_email: str,
    app_password: str,
    subject: str,
    body: str,
    db: Session = Depends(get_db)
):

    emails = db.query(Email).filter(
        Email.campaign_id == campaign_id,
        Email.status == "pending"
    ).all()

    sent_count = 0

    for email in emails:

        success = send_email(
            sender_email,
            app_password,
            email.email,
            subject,
            body
        )

        if success:
            email.status = "sent"
            sent_count += 1
        else:
            email.status = "failed"

        db.commit()
        time.sleep(60)

    return {
        "campaign_id": campaign_id,
        "emails_sent": sent_count
    }


# Start campaign background
@app.post("/start-campaign/{campaign_id}")
def start_campaign(
    campaign_id: int,
    sender_email: str,
    app_password: str,
    subject: str,
    body: str
):

    thread = threading.Thread(
        target=run_campaign,
        args=(campaign_id, sender_email, app_password, subject, body)
    )

    thread.start()

    return {"message": "Campaign started in background"}


# Pause campaign
@app.post("/pause-campaign/{campaign_id}")
def pause_campaign(campaign_id: int, db: Session = Depends(get_db)):

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    campaign.status = "paused"
    db.commit()

    return {"message": "Campaign paused"}


# Campaign statistics
@app.get("/campaign-stats/{campaign_id}")
def campaign_stats(campaign_id: int, db: Session = Depends(get_db)):

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    total = db.query(Email).filter(Email.campaign_id == campaign_id).count()
    sent = db.query(Email).filter(
        Email.campaign_id == campaign_id,
        Email.status == "sent"
    ).count()
    failed = db.query(Email).filter(
        Email.campaign_id == campaign_id,
        Email.status == "failed"
    ).count()
    pending = db.query(Email).filter(
        Email.campaign_id == campaign_id,
        Email.status == "pending"
    ).count()

    return {
        "campaign_id": campaign_id,
        "status": campaign.status,
        "total": total,
        "sent": sent,
        "failed": failed,
        "pending": pending
    }


# Upload resume
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    file_path = "uploads/resume.pdf"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "Resume uploaded successfully"}


# List campaigns
@app.get("/campaigns")
def list_campaigns(db: Session = Depends(get_db)):

    campaigns = db.query(Campaign).all()

    result = []

    for c in campaigns:
        result.append({
            "id": c.id,
            "name": c.name,
            "status": c.status,
            "total_emails": c.total_emails
        })

    return result


