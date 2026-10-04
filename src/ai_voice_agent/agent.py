from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
# import time
from langchain_core.tools import tool
from langchain.agents import create_agent
from ai_voice_agent.integrations.gmail_tools import get_gmail_tools

#defining the tools
gmail_tools = get_gmail_tools()

load_dotenv()
def get_ai_message(user_message : str) -> str:
    result = agent.invoke({
        "messages":[
            {
                "role":"user",
                "content":user_message,
            }
        ]
    })
    return result["messages"][-1].content

llm = ChatGroq(model="openai/gpt-oss-120b")
# start = time.time()
agent = create_agent(
    model=llm,
    tools=gmail_tools,
    system_prompt="""
You are a helpful AI voice assistant.

You have access to Gmail tools.

Use Gmail tools when the user asks about their emails.

Important rules:
- Never invent an email or email content.
- Use Gmail tools when actual Gmail information is needed.
- Keep responses concise because responses are spoken over a phone call.
- Never claim to have sent or modified an email.
- You currently have read-only Gmail access.
- If the user asks you to send, delete, or modify an email, explain that this capability is not enabled yet.
"""
)



# result = llm.invoke("hey this is nayab")
# print(result.content)
# print(time.time()- start)