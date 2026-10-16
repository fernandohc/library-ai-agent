from src.agents.analytics_agent import analytics_agent


def main():
    questions = [
        "Give me an overview of the library.",
        "Which genres have the most books?",
        "What are the top 5 highest-rated books?",
    ]

    for question in questions:
        print(f"\n{'=' * 60}")
        print(f"QUESTION: {question}")
        print("=" * 60)

        response = analytics_agent.invoke(
            {"messages": [{"role": "user", "content": question}]}
        )

        for message in response["messages"]:
            tool_calls = getattr(message, "tool_calls", [])

            for tool_call in tool_calls:
                print(f"Tool called: {tool_call['name']}")
                print(f"Arguments: {tool_call['args']}")

        print("\nANSWER:")
        print(response["messages"][-1].content)


if __name__ == "__main__":
    main()
