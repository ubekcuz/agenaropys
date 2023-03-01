from .objects import *
import requests
import string
import random

class SecMail:
    def __init__(self):
        self.email = None
        self.domain = None

    def generate_email(self):
        yep = ''.join(
            [random.choice(
                string.ascii_lowercase + ''.join([str(i) for i in range(10)])
            ) for _ in range(random.randint(8,12))]
        )
        end = random.choice(["1secmail.com", "1secmail.org", "1secmail.net", "bheps.com", "dcctb.com", "kzccv.com", "qiott.com", "wuuvo.com"])
        return f'sshell-{yep}@{end}' 

    def get_messages(self, email: str):
        """
                Get Email Messages!

                **Parameters**
                    - **email** : The Email You Want To See His Messages

                **Returns**
                    - **Success** : :meth:`Messages Object <secmail.objects.Messages>`
         """
        email = email.split("@")
        req = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={email[0]}&domain={email[1]}").json()
        return Messages(req).Messages

    def read_message(self, email: str, id: str):
        """
                Get Message Info by Id!

                **Parameters**
                    - **email** : The Email You Want To See His Message
                    - **id** : Id of The Message

                **Returns**
                    - **Success** : :meth:`MessageRead Object <secmail.objects.MessageRead>`
        """
        email = email.split("@")
        req = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={email[0]}&domain={email[1]}&id={id}").json()
        return MessageRead(req)
