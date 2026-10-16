from src.agents.book_search_agent import book_search_agent


def ask_agent(question: str):
    response = book_search_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
    )

    return response


def print_message(message):
    print("\n--- MESSAGE ---")
    print(f"Type: {type(message).__name__}")

    if hasattr(message, "content") and message.content:
        print(f"Content: {message.content}")

    if hasattr(message, "tool_calls") and message.tool_calls:
        print("Tool calls:")

        for tool_call in message.tool_calls:
            print(f"  Tool: {tool_call['name']}")
            print(f"  Arguments: {tool_call['args']}")


def main():

    question = "Which horror books are currently available?"

    print("=" * 60)
    print(f"USER: {question}")
    print("=" * 60)

    response = ask_agent(question)

    print("\n=== AGENT EXECUTION ===")

    for message in response["messages"]:
        print_message(message)

    print("\n=== FINAL ANSWER ===")

    print(response["messages"][-1].content)


if __name__ == "__main__":
    main()
