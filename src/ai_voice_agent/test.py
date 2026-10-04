from ai_voice_agent.agent import get_ai_message

responses = get_ai_message("kjdshkd")

print(responses["messages"][-1].content)