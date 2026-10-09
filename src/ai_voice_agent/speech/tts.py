import os

from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

client = SarvamAI(
    api_subscription_key=os.environ["SARVAM_API_KEY"]
)


def text_to_speech(text: str) -> bytes:
    chunks = client.text_to_speech.convert_stream(
        text=text,
        model="bulbul:v4-flash",
        language_code="en-IN",
        speaker="simran_en_customer",
        output_audio_codec="mp3",
    )

    return b"".join(chunks)