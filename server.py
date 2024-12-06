from fastapi import FastAPI
from last_three import get_last_three_from_lastfm_page
import os
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class EmailRequest(BaseModel):
    email: EmailStr

def send_email(to_email: str, subject: str, body: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = os.environ.get("MAIL_USERNAME")
    smtp_password = os.environ.get("MAIL_PASSWORD")

    try:
        msg = EmailMessage()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

@app.post("/send-email/{user}")
def send_email_to_user(user: str = Path(..., title="Username"), email_req: EmailRequest = None):
    if not email_req:
        raise HTTPException(status_code=400, detail="Email is required in the body.")

    last_three = get_last_three_from_lastfm_page(user)
    email_address = email_req.email
    subject = f"Last three"
    body = f"Songs\n{last_three}"
    send_email(email_address, subject, body)


    return {"message": f"email sent to {email_address}."}
