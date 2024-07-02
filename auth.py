import smtplib
from email.mime.text import MIMEText
from azure.cosmos import exceptions
import random
from dotenv import load_dotenv
import os
import hashlib
from db import user_container, admin_container

# Load environment variables from .env file
load_dotenv()

# Email setup
email_host = os.getenv("EMAIL_HOST")
email_port = os.getenv("EMAIL_PORT")
email_user = os.getenv("EMAIL_HOST_USER")
email_password = os.getenv("EMAIL_HOST_PASSWORD")

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = to_email
    
    with smtplib.SMTP(email_host, email_port) as server:
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, to_email, msg.as_string())

def send_verification_code(email):
    code = str(random.randint(100000, 999999))
    user_container.upsert_item({
        'id': email,
        'email': email,
        'code': code,
        'verified': False
    })
    send_email(email, "Your Verification Code", f"Your verification code is {code}")

def verify_code(email, code):
    try:
        user = user_container.read_item(item=email, partition_key=email)
        if user['code'] == code:
            user['verified'] = True
            user_container.upsert_item(user)
            return True
        return False
    except exceptions.CosmosResourceNotFoundError:
        return False

def notify_unregistered_email(email):
    send_email(email, "Unregistered Email Notification", "This email address is not registered in our system. Please sign up first.")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin(username, password):
    hashed_password = hash_password(password)
    admin_container.upsert_item({
        'id': username,
        'username': username,
        'password': hashed_password
    })

def get_admins():
    query = "SELECT * FROM c"
    items = list(admin_container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    return items

def admin_login(username, password):
    hashed_password = hash_password(password)
    try:
        admin = admin_container.read_item(item=username, partition_key=username)
        return admin['password'] == hashed_password
    except exceptions.CosmosResourceNotFoundError:
        return False

def delete_admin(username):
    admin_container.delete_item(item=username, partition_key=username)
