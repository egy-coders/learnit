import requests
from django.conf import settings

def verify_recaptcha(recaptcha_response):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": settings.RECAPTCHA_SECRET_KEY,
        "response": recaptcha_response
    }
    response = requests.post(url, data=data)
    result = response.json()
    return result.get("success", False)  # Returns True if verification is successful
