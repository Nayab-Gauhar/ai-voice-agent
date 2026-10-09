import os
from dotenv import load_dotenv
from sarvamai import SarvamAI
from sarvamai.play import save,play

load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")

if not api_key:
    raise ValueError("SARVAM_API_KEY is missing from .env")

# Connect to Sarvam
client = SarvamAI(api_subscription_key=api_key)

# Convert text into speech
response = client.text_to_speech.convert(
    text="Hello! I am your AI voice assistant.",
    model="bulbul:v4-flash",
    language_code="en-IN",
    speaker="simran_en_customer",
    output_audio_codec="wav",
)

# Save the generated audio
play(response)
save(response, "output.wav")
print(f"Audio length: {os.path.getsize('output.wav')} bytes")
print("Speech saved to output.wav")