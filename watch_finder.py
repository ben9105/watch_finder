import pandas as pd
import datetime as dt
import praw
import re
import password
import smtplib
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

reddit = praw.Reddit(client_id=password.FE_key, client_secret=password.secret_key, user_agent='watch_finder', username=password.reddit_username, password=password.reddit_password)
gmail_password = password.google_password
email = password.google_email

def watches_list():
    subreddit = reddit.subreddit('Watchexchange')
    new_subreddit = subreddit.new(limit=100)
    watch_list = [(w.title.lower(), w.shortlink)  for w in new_subreddit]
    # print(watch_list)

    seiko_watch = []
    for s, seiko in watch_list:
        if 'srp' in s:
            seiko_watch.append(seiko + '/ ' + s + ' <br>')
    return seiko_watch


def html_email():
    html = f'''\
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <p>Here is a list of watches for sale on Reddit:</p>
            <p>{watches_list()}</p>
        </body>
        </html>
    '''
    return html


def send_mail():
    try:
        message = MIMEMultipart()
        message['Subject'] = 'Watches for sale'
        message['From'] = email
        message['To'] = email
        username = email
        password = gmail_password
        body = MIMEText(html_email(), 'html')

        message.attach(body)

        smtp = smtplib.SMTP('smtp.gmail.com', 587, timeout=120)
        smtp.starttls()
        # smtp.ehlo()

        smtp.login(username, password)
        smtp.sendmail(message['From'], message['To'], message.as_string())

        print('Email sent')
    except Exception as e:
        print(e)
    finally:
        smtp.quit()


send_mail()
