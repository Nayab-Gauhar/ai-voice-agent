from fastapi import FastAPI

app = FastAPI(
    title="Gmail Calling Agent",
    description="AI Agent voice assistant with Gmail Integrations",
    version="0.1.0",
)

@app.get('/')
async def home():
    return {"message":"AI Voice Agent is running!!"}

@app.get('/health')
async def health():
    return{
        "status":"healthy"
    }
