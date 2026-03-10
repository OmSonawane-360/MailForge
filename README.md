# 🚀 MailForge — Automated HR Outreach Platform

MailForge is a full-stack automation tool designed to solve a real problem faced by job seekers: **sending personalized cold emails to hundreds or thousands of HR contacts efficiently**.

Instead of manually copying emails from a PDF and sending messages one-by-one, MailForge automates the entire outreach workflow.

Users can upload a directory of HR emails, create campaigns, attach their resume, and automatically send personalized emails while respecting Gmail safety limits.

---

# 🌍 Live Demo

Frontend (UI)  
https://mailforge-ui.onrender.com

Backend API  
https://mailforge.onrender.com/docs

---

# 🧠 The Real Problem

While searching for jobs, I obtained a **PDF directory containing around 1800 HR contacts** with details such as:

- HR Name
- Email Address
- Title
- Company

Sending cold emails manually required:

1. Opening the PDF
2. Copying the email
3. Opening Gmail
4. Writing or pasting the message
5. Attaching resume
6. Personalizing the email
7. Sending it

Repeating this **1800 times** would take **days of manual work**.

So I asked myself:

> “Why not build a system that automates this entire process?”

That idea led to the creation of **MailForge**.

---

# 💡 Solution

MailForge automates the entire cold-outreach process.

Users simply:

1️⃣ Upload a PDF containing HR contacts  
2️⃣ Create a campaign  
3️⃣ Upload their resume  
4️⃣ Write an email template  
5️⃣ Start the campaign

The system automatically:

- Extracts contacts from the PDF
- Validates email addresses
- Stores campaign data
- Sends emails one-by-one safely
- Tracks progress in real time

---

# ✨ Key Features

### 📄 PDF Contact Extraction
Extracts structured contact data from HR directories.

### 📧 Automated Email Campaigns
Send hundreds of cold emails automatically.

### 📎 Resume Attachment
Automatically attaches the user’s resume to each email.

### ⏱ Gmail Safety Limits
Implements delays and daily limits to avoid Gmail spam detection.

### 📊 Campaign Dashboard
Track:

- Total Emails
- Sent
- Pending
- Failed

### ⏸ Pause / Resume Campaign
Users can stop campaigns anytime.

### 📬 Personalized Email Templates
Users can write custom email messages.

### 🔍 Email Validation
Invalid emails are filtered automatically.

### 🌐 Fully Deployed SaaS
Accessible online via browser.

---

# 🏗 System Architecture
