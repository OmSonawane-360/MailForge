from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(String, default="created")
    total_emails = Column(Integer, default=0)

    
class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    email = Column(String)
    name = Column(String)
    company = Column(String)
    title = Column(String)
    status = Column(String, default="pending")