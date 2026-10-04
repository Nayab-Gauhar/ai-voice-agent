from ai_voice_agent.agent import get_ai_message
from ai_voice_agent.agent import agent

result = agent.invoke({
    "messages" : [
        {
            "role":"user",
            "content":"Can u please check my latest mails"
        }
    ]
})
for message in result["messages"]:
    print("\n" + "=" * 80)
    print(type(message).__name__)
    print(message)
# questions = [
    # # "Can you check my latest email?",
    # # "Find emails from the last few days.",
#     # "Can you tell me what my latest email is about?",
# # ]
# 

# # for question in questions:

    # # print("\n" + "=" * 80)
    # # print(f"USER: {question}")

    # # response = get_ai_message(question)

    # print(f"AI: {response}")