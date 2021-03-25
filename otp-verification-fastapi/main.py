from typing import Optional
import boto3
import math
import random
import smtplib
from fastapi import FastAPI
import requests
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = FastAPI()

app.secret_key = "pefpejfoej++*jfojefjeofjkdnihpopjsjohfoijidjs155+-*"

otp = ""
client_mail = ""
@app.get("/")
def read_root():
    return {"Hello": "World"}

#turn on first less secure app with your account for using smtp
# @app.get("/otp_email/{email}")
# def otp_email(email: str, q: Optional[str] = None):
#     client_mail = email
#     OTP = ""
#     string="0123456789"
#     length = len(string)
#     for i in range(6):
#         OTP += string[math.floor(random.random() * length)]
#     receiver = f"{client_mail}"
#     email = 'radhesaini288@gmail.com' #your mail
#     passw = "8209989587"              #your password
#     server = smtplib.SMTP('smtp.gmail.com:587')
#     message = f'Subject:SAFEMEET VARIFICATION \n\nyour otp for safemeet verification: {OTP} do not share with anyone'
#     server.ehlo()
#     server.starttls()
#     server.login(email, passw)
#     server.sendmail(email, receiver, message)
#     server.quit()
#     print(message)
#     global otp
#     otp = OTP
#     return {"item_id": "sent mail..!", "q": q}

    
@app.get("/otp_email/{email}")
def otp_email(email: str, q: Optional[str] = None):
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    CLIENT_SECRET_FILE = 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    OTP=random.randint(1,999999)
    emailMsg =f"your otp for safemeet varification: {OTP} do not with anyone"
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = email
    mimeMessage['subject'] = 'SAFEMEET VERIFICATION PROCESS'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    global otp
    otp = OTP
    return {"item_id": "sent mail..!", "q": q}



@app.get("/otp_sms/{mob_no}")
def otp_sms(mob_no: str, q: Optional[str] = None):
    OTP=random.randint(1,999999)
    # Create an SNS client
    client = boto3.client(
        "sns",
        aws_access_key_id="AKIASVSS3SAMY44LQ2FE",
        aws_secret_access_key="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",
        region_name="us-east-1"
    )

     # Create the topic if it doesn't exist (this is idempotent)
     # topic = client.create_topic(Name="notifications")
    global otp
    otp=OTP
    if len(mob_no)==10:
        mob_no = "+91"+mob_no
    response = client.publish(
    PhoneNumber=f"{mob_no}",
    Message=f"your otp for safemeet varification: {OTP} do not with anyone",
    )
    return {"item_id":"sms sent..!", "q": q}

@app.get("/verify_otp/{receive_code}")
def vrify_otp(receive_code: int, q: Optional[str] = None):
    if receive_code == otp:
        return {"item_id": "varification successfull...!", "q": q}
    else:
        return {"item_id": "incorrect otp...!", "q": q}


