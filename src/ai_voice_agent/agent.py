from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
# import time
from langchain_core.tools import tool
from langchain.agents import create_agent
from ai_voice_agent.integrations.gmail_tools import get_gmail_tools
from langchain_google_genai import ChatGoogleGenerativeAI

#defining the tools
gmail_tools = get_gmail_tools()

load_dotenv()

# llm = ChatGroq(model="openai/gpt-oss-20b")
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
# print((llm.invoke("jldfjldf")).content)
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

def extract_text(content) -> str:
    """
    Convert LangChain/Gemini response content into plain text.
    """
    if isinstance(content,str):
        return content
    if isinstance(content,list):
        text_block = []

        for block in content:
            if isinstance(block,dict):
                if block.get("type") == "text":
                    text_block.append(block.get("text",""))
        return "".join(text_block)

    return str(content)

def get_ai_message(user_message : str) -> str:
    result = agent.invoke({
        "messages":[
            {
                "role":"user",
                "content":user_message,
            }
        ]
    })
    final_result = result["messages"][-1]
    return extract_text(final_result.content)

# print((get_ai_message("Find the weather")))
# result = llm.invoke("hey this is nayab")
# print(result.content)
# print(time.time()- start)