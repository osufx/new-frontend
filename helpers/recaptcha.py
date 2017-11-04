import json
import requests

is_enabled = True
VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

with open("recaptcha.json", "r") as f:
    rconfig = json.load(f)

def verify(request):

    if is_enabled:

        data = {
            "secret": rconfig['secret_key'],
            "response": request.form.get('g-recaptcha-response'),
            "remoteip": request.environ.get('REMOTE_ADDR')
        }

        r = requests.get(VERIFY_URL, params=data)

        return r.json()["success"] if r.status_code == 200 else False
    return True