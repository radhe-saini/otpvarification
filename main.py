from typing import Optional

from fastapi import FastAPI
import math
import random
import smtplib

import requests

app = FastAPI()

app.secret_key = "pefpejfoej++*jfojefjeofjkdnihpopjsjohfoijidjs155+-*"

otp = ""
client_mail = ""
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/otp_email/{email}")
def otp_email(email: str, q: Optional[str] = None):
    client_mail = email
    OTP = ""
    length = len(string)
    for i in range(6):
        OTP += string[math.floor(random.random() * length)]
    receiver = f"{client_mail}"
    email = 'yourmail'
    passw = "youpassword"
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(email, passw)
    message = 'Subject: {}\n\n{}'.format('otp from myapp', OTP)
    server.sendmail(email, receiver, message)
    server.quit()
    # print("Success: Email sent!")
    global otp
    otp = OTP
    return {"item_id": "sent mail..!", "q": q}


@app.get("/otp_sms/{mob_no}")
def otp_sms(mob_no: str, q: Optional[str] = None):
    msg=f"you varification code is :{random.randint(1,99999)}"
    url = "https://www.fast2sms.com/dev/bulk"
    params = {
    "authorization": "N7EXYK2FtuWACcMQ0mJk6H1g8nqsPLiho5x3SpVwBejbv9DORrhGveNqykBnj9MJYHoiu1f7T4SbVrCt",
    "sender_id": "Saleassist",
    "message": msg,
    "language": "english",
    "route": "p",
    "numbers": mob_no
    }
    rs = requests.get(url, params=params)
    return {"item_id":"sms sent..!", "q": q}

@app.get("/verify_otp/{receive_code}")
def vrify_otp(receive_code: int, q: Optional[str] = None):
    if receive_code == otp:
        return {"item_id": receive_code, "q": q}
    else:
        return {"item_id": receive_code, "q": q}


