from flask import *
import requests 

def mail_api(email):
    url = "https://emailapi.silverpush.co/mail/"

    payload = {'To': '',
    'Subject': 'Reset Password ',
    'From': 'reports@chocolateplatform.com',
    'Body': 'Please use the link below to reset your password: ',
    'Name': 'Gen AI '}
    payload['To'] = email
    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
