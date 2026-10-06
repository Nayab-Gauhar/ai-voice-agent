import os
from pprint import pprint

from dotenv import load_dotenv
from vonage import Auth, Vonage
from vonage_voice import CreateCallRequest, Phone, ToPhone

load_dotenv()

APPLICATION_ID = os.environ["VONAGE_APPLICATION_ID"]
PRIVATE_KEY = os.environ["VONAGE_PRIVATE_KEY"]
TO_NUMBER = os.environ["VONAGE_TO_NUMBER"]
NGROK_URL = os.environ["NGROK_URL"]
FROM_NUMBER = os.environ["VONAGE_FROM_NUMBER"]
client = Vonage(
    Auth(
        application_id=APPLICATION_ID,
        private_key=PRIVATE_KEY,
    )
)

response = client.voice.create_call(
    CreateCallRequest(
        answer_url=[f"{NGROK_URL}/answer"],
        to=[ToPhone(number=TO_NUMBER)],
        from_=Phone(number=FROM_NUMBER),
    )
)

pprint(response)