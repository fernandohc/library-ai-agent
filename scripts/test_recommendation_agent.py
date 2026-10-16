from src.agents.recommendation_agent import recommendation_agent


def main():
    question = "Recommend 5 books for user user-001 based on their loan history."

    response = recommendation_agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )

    for message in response["messages"]:
        print(f"\n--- {type(message).__name__} ---")

        if getattr(message, "tool_calls", None):
            for tool_call in message.tool_calls:
                print("Tool:", tool_call["name"])
                print("Arguments:", tool_call["args"])

        if message.content:
            print(message.content)


if __name__ == "__main__":
    main()
