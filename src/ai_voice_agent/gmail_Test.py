from ai_voice_agent.integrations.gmail_tools import get_gmail_tools

tools = get_gmail_tools()

# print(tools)

for i in tools:
    print(i.name)
    print(i.description)
    # print(i.get_graph)