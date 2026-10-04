from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import(
    build_gmail_service,
    get_gmail_credentials,
)

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]
def get_gmail_tools():  
    credentials = get_gmail_credentials(
        token_file="token.json",
        client_sercret_file="credentials.json",
        scopes=SCOPES,
    )

    api_resource = build_gmail_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)

    tools = toolkit.get_tools()

    #only the exposed tools readonly tools 
    allowed_tools = {
        "search_gmail",
        "get_gmail_message",
        "get_gmail_thread",
    }
    return [
        tool
        for tool in tools
        if tool.name in allowed_tools
    ]

