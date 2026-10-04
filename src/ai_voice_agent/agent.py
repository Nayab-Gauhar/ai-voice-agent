from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
# import time
from langchain_core.tools import tool
from langchain.agents import create_agent

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
    tools=[],
    system_prompt="""You are very helpful AI voice agent 
    Keep your responses to the point and natural because your responses will be spoken on the phone call"""
)



# result = llm.invoke("hey this is nayab")
# print(result.content)
# print(time.time()- start)